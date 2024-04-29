import streamlit as st
import pandas as pd
import json
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate 
from langchain.chains import LLMChain

from system_messages import *

st.set_page_config(page_title='TrueYou Content Generator', page_icon=None, layout="wide")

st.title('TrueYou Content Generation')
st.markdown("## Activities Generator")

# # Assuming the DataFrame 'qs' is loaded as shown
# qs = pd.read_csv('questions.csv')

# sorted_df = qs.sort_values(by=['Cat', 'Scale Name'])
# scale_options = [f"{row['Scale Name']} ({row['Cat']})" for _, row in sorted_df.drop_duplicates(['Scale Name', 'Cat']).iterrows()]

# selected_scale = st.selectbox("Select which scale you'd like to generate activities for:", scale_options, key='activities')
# selected_scale_name = selected_scale.split(" (")[0]
# scale_items_dict = {selected_scale_name: qs[qs['Scale Name'] == selected_scale_name]['Item Text'].tolist()}

# # selected_scale_names = [s.split(" (")[0] for s in selected_scales]
# # scale_items_dict = qs[qs['Scale Name'].isin(selected_scale_names)].groupby('Scale Name')['Item Text'].apply(list).to_dict()

# # prompt = generate_four_activities

# prompt = generate_eight_activities

# Adding a radio button to choose between trait-specific or generic activities

activity_type = st.radio("Choose the type of activities to generate:", ('Trait-Specific', 'Generic'))

# Load DataFrame as before for trait-specific activity generation
qs = pd.read_csv('questions.csv')
sorted_df = qs.sort_values(by=['Cat', 'Scale Name'])
scale_options = [f"{row['Scale Name']} ({row['Cat']})" for _, row in sorted_df.drop_duplicates(['Scale Name', 'Cat']).iterrows()]

if activity_type == 'Trait-Specific':
    prompt = generate_eight_activities
    selected_scale = st.selectbox("Select which scale you'd like to generate activities for:", scale_options, key='activities')
    selected_scale_name = selected_scale.split(" (")[0]
    scale_items_dict = {selected_scale_name: qs[qs['Scale Name'] == selected_scale_name]['Item Text'].tolist()}
else:
    # For generic activity generation, no need for scale selection
    prompt = generate_generic_activities
    input = st.text_input("Enter any additional context you might want to give to generate these generic/univerally applicable activities")
    
if st.button('Submit'):
    with st.spinner('Generating activities...'):
        for_df = []
        ideations = []  # Store ideation texts here
        for scale, items in scale_items_dict.items():
            items_str = ", ".join(items)

            chat_model = ChatOpenAI(openai_api_key=st.secrets['API_KEY'], model_name='gpt-4-1106-preview', temperature=0.2)
            chat_chain = LLMChain(prompt=PromptTemplate.from_template(prompt), llm=chat_model)
            if activity_type == 'Trait-Specific':
                generated_output = chat_chain.run(SCALE=scale, ITEMS=items_str)
            else:
                generated_output = chat_chain.run(INPUT=input)
            # Splitting the generated_output into ideation and activities parts
            ideation_part, activities_json = generated_output.split('ACTIVITIES:')
            ideations.append(ideation_part.strip().removeprefix('IDEATION:').strip())  # Add the ideation text to the list

            for_df.extend(json.loads(activities_json.strip()))  # Strip in case there's leading/trailing whitespace
        
        # Displaying ideations in an expander
        with st.expander("Ideation behind these activities"):
            for ideation in ideations:
                st.write(ideation)
        
        st.write(for_df)
        df = pd.DataFrame(for_df)
        st.write('Generated activities:')
        st.dataframe(df)

        # Convert DataFrame to CSV string
        csv = df.to_csv(index=False)
        
        # Create a download button and offer the CSV string for download
        st.download_button(
            label="Download this as CSV",
            data=csv,
            file_name='generated_activities.csv',
            mime='text/csv',
        )

st.write("---")
st.markdown("## Insights Generator")

selected_scales_insights = st.multiselect("Select which scales you'd like to generate activities for:", scale_options, key='insights')
N = st.number_input("Number of insights to generate for each HIGH and LOW scorer per trait:", min_value=1, max_value=10, value=3)

if st.button('Submit', key='insights_submit'):
    with st.spinner('Generating insights...'):
        chat_model = ChatOpenAI(openai_api_key=st.secrets['API_KEY'], model_name='gpt-4-1106-preview', temperature=0.2)
        chat_chain = LLMChain(prompt=PromptTemplate.from_template(insights_generation), llm=chat_model)
        generated_output = chat_chain.run(SCALES=selected_scales_insights, N=N)
        make_df = json.loads(generated_output)
    # st.write(scale_items_dict)
    df = pd.DataFrame(make_df)
    st.write('Generated insights:')
    st.write(make_df)
    with st.expander('See insights in spreadsheeet view'):
        st.dataframe(df, use_container_width=True)

    # Convert DataFrame to CSV string
    insights_csv = df.to_csv(index=False)
    
    # Create a download button and offer the CSV string for download
    st.download_button(
        label="Download this as CSV",
        data=insights_csv,
        file_name='generated_insights.csv',
        mime='text/csv',
    )
