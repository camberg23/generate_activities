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

# Assuming the DataFrame 'qs' is loaded as shown
qs = pd.read_csv('questions.csv')

sorted_df = qs.sort_values(by=['Cat', 'Scale Name'])
scale_options = [f"{row['Scale Name']} ({row['Cat']})" for _, row in sorted_df.drop_duplicates(['Scale Name', 'Cat']).iterrows()]

selected_scales = st.multiselect("Select which scales you'd like to generate activities for:", scale_options, key='activities')

selected_scale_names = [s.split(" (")[0] for s in selected_scales]

scale_items_dict = qs[qs['Scale Name'].isin(selected_scale_names)].groupby('Scale Name')['Item Text'].apply(list).to_dict()

four_or_eight = st.radio(
    "Choose your option:",
    ('Force positive/negative activity for each trait level (generates 8 activities)', 
     'Leave positive/negative assignment to LLM (generates 4 activities)'),
    index=0
)

if four_or_eight == 'Force positive/negative activity for each trait level (generates 8 activities)':
    prompt = generate_eight_activities
else:
    prompt = generate_four_activities

if st.button('Submit'):
    with st.spinner('Generating activities...'):
        for_df = []
        for scale, items in scale_items_dict.items():
            items_str = ", ".join(items)

            chat_model = ChatOpenAI(openai_api_key=st.secrets['API_KEY'], model_name='gpt-4-1106-preview', temperature=0.2)
            chat_chain = LLMChain(prompt=PromptTemplate.from_template(prompt), llm=chat_model)
            generated_output = chat_chain.run(SCALE=scale, ITEMS=items_str)
            for_df.extend(json.loads(generated_output))
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
