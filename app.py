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

activity_type = st.radio("Choose the type of activities to generate:", ('Trait-Specific', 'Generic'))

# Load DataFrames with new structure
qs = pd.read_csv('Updated App Test 6_5_25 - Items.csv')
scales_df = pd.read_csv('Updated App Test 6_5_25 - Scales.csv')

# Create scale options using Scale column from scales CSV and get corresponding Scale Key from items CSV
scale_options = []
for _, row in scales_df.iterrows():
    trait_key = row['Scale']  # This is actually the trait key
    title = row['Title']
    # Find the corresponding Scale Key from the items CSV
    scale_key_row = qs[qs['Trait Key'] == trait_key].iloc[0] if len(qs[qs['Trait Key'] == trait_key]) > 0 else None
    if scale_key_row is not None:
        scale_key = scale_key_row['Scale Key']
        scale_options.append(f"{row['Scale']} — {row['Title']} ({scale_key})")
    else:
        # Fallback if no matching scale key found
        scale_options.append(f"{row['Scale']} — {row['Title']} ({trait_key})")

# Sort by scale key (the part in parentheses) - alphabetically then numerically
def sort_key(option):
    scale_key = option.split(" (")[-1].rstrip(")")
    # Extract letter and number parts for proper sorting
    letter = ''.join(filter(str.isalpha, scale_key))
    number = ''.join(filter(str.isdigit, scale_key))
    return (letter, int(number) if number else 0)

scale_options.sort(key=sort_key)

if activity_type == 'Trait-Specific':
    prompt = generate_eight_activities
    selected_scale_display = st.selectbox("Select which scale you'd like to generate activities for:", scale_options, key='activities')
    # Extract the scale key from the display format "Title (scale_key)" 
    selected_scale_key = selected_scale_display.split(" (")[-1].rstrip(")")
    # Find the corresponding trait key for this scale key
    trait_key_row = qs[qs['Scale Key'] == selected_scale_key].iloc[0] if len(qs[qs['Scale Key'] == selected_scale_key]) > 0 else None
    if trait_key_row is not None:
        selected_trait_key = trait_key_row['Trait Key']
        scale_items_dict = {selected_trait_key: qs[qs['Trait Key'] == selected_trait_key]['Item Text'].tolist()}
    else:
        # Fallback - shouldn't happen if data is aligned
        scale_items_dict = {selected_scale_key: []}
else:
    # For generic activity generation, no need for scale selection
    prompt = generate_generic_activities
    input = st.text_input("Enter any additional context you might want to give to generate these generic/univerally applicable activities")

if st.button('Submit'):
    with st.spinner('Generating activities...'):
        for_df = []
        ideations = []  # Store ideation texts here

        chat_model = ChatOpenAI(openai_api_key=st.secrets['API_KEY'], model_name='gpt-4o-2024-05-13', temperature=0.2)
        chat_chain = LLMChain(prompt=PromptTemplate.from_template(prompt), llm=chat_model)
        
        if activity_type == 'Trait-Specific':    
            for trait_key, items in scale_items_dict.items():
                items_str = ", ".join(items)
                # Get the trait description for activities too
                trait_info = scales_df[scales_df['Scale'] == trait_key]
                trait_description = trait_info['Description'].values[0] if len(trait_info) > 0 else ""
            
            generated_output = chat_chain.run(SCALE=trait_key, ITEMS=items_str, DESCRIPTION=trait_description)
            
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
        
        # Convert the list of activities into a DataFrame
        df = pd.DataFrame(for_df)

        # Adjust the DataFrame as per the developer's requirements

        # 1. Rename columns to match the required names
        df.rename(columns={
            'Trait Level': 'score',
            'Trait': 'trait',
            'Title': 'title',
            'Description': 'description',
            'Activity': 'activity',
            'Categorization': 'aspect',
            'Domain': 'category',
            'Activity Type': 'type'
        }, inplace=True)

        # 2. Create 'trait_value' column by combining 'trait' and 'score'
        df['trait_value'] = df['trait'].str.lower() + '/' + df['score'].str.lower()

        # 3. Convert 'trait', 'score', and 'trait_value' to lowercase
        df['trait'] = df['trait'].str.lower()
        df['score'] = df['score'].str.lower()
        df['trait_value'] = df['trait_value'].str.lower()

        # 4. Map 'aspect' values to correct wording
        aspect_mapping = {
            'HARNESS ADVANTAGES': 'strength',
            'ADDRESS DISADVANTAGES': 'blindspot'
        }
        df['aspect'] = df['aspect'].map(aspect_mapping)

        # 5. Convert 'category' to lowercase (or title case if needed)
        df['category'] = df['category'].str.lower()  # Use .str.title() if title case is needed

        # 6. Map 'type' values to correct wording
        type_mapping = {
            'TIMED ACTIVITY': 'timed',
            'REFLECTION': 'reflection'
        }
        df['type'] = df['type'].map(type_mapping)

        # 7. Reorder columns to match the desired order
        desired_order = ['trait', 'score', 'trait_value', 'title', 'description', 'activity', 'aspect', 'category', 'type']
        df = df[desired_order]

        # Display the adjusted DataFrame
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

# Use the same scale options for insights
selected_scales_insights = st.multiselect("Select which scales you'd like to generate insights for:", scale_options, key='insights')
N = st.number_input("Number of insights to generate for each HIGH and LOW scorer per trait:", min_value=1, max_value=10, value=3)

horoscopify = st.checkbox('Horoscopify?')

if st.button('Submit', key='insights_submit'):
    with st.spinner('Generating insights...'):
        if horoscopify:
            prompt = insights_generation_horoscopify
        else:
            prompt = insights_generation_standard
            
        chat_model = ChatOpenAI(openai_api_key=st.secrets['API_KEY'], model_name='gpt-4o-2024-08-06', temperature=0.2)
        chat_chain = LLMChain(prompt=PromptTemplate.from_template(prompt), llm=chat_model)
        
        # Extract scale keys from the selected display options and build trait info
        trait_info_list = []
        for display_option in selected_scales_insights:
            scale_key = display_option.split(" (")[-1].rstrip(")")
            # Find the corresponding trait key for this scale key
            trait_key_row = qs[qs['Scale Key'] == scale_key].iloc[0] if len(qs[qs['Scale Key'] == scale_key]) > 0 else None
            if trait_key_row is not None:
                trait_key = trait_key_row['Trait Key']
                # Get the trait info from scales_df
                trait_info = scales_df[scales_df['Scale'] == trait_key]
                if len(trait_info) > 0:
                    trait_info_list.append({
                        'trait_key': trait_key,
                        'title': trait_info['Title'].values[0],
                        'description': trait_info['Description'].values[0],
                        'high_label': trait_info['High Label'].values[0],
                        'low_label': trait_info['Low Label'].values[0]
                    })
        
        # Pass both trait keys and descriptions to the insights generator
        generated_output = chat_chain.run(
            TRAITS_INFO=trait_info_list,
            N=N
        )
        make_df = json.loads(generated_output)
    
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

st.write("---")
st.markdown("## Trait Text Generator")

# Use the same scale options for trait text generator (same format as other dropdowns)
selected_trait_display = st.selectbox("Select a trait:", scale_options)
# Extract the scale key from the display format "Title (scale_key)" 
selected_scale_key = selected_trait_display.split(" (")[-1].rstrip(")")
# Find the corresponding trait key for this scale key
trait_key_row = qs[qs['Scale Key'] == selected_scale_key].iloc[0] if len(qs[qs['Scale Key'] == selected_scale_key]) > 0 else None
if trait_key_row is not None:
    selected_trait = trait_key_row['Trait Key']
else:
    # Fallback - shouldn't happen if data is aligned
    selected_trait = selected_scale_key

selected_levels = st.multiselect("Select levels to generate text for:", ['low', 'medium', 'high'])

if st.button('Submit', key='trait_text_submit'):
    with st.spinner('Generating trait text...'):
        chat_model = ChatOpenAI(openai_api_key=st.secrets['API_KEY'], model_name='gpt-4o-2024-05-13', temperature=0.2)
        chat_chain = LLMChain(prompt=PromptTemplate.from_template(trait_text_generation), llm=chat_model)
        
        trait_info = scales_df[scales_df['Scale'] == selected_trait]
        trait_description = trait_info['Description'].values[0]
        high_label = trait_info['High Label'].values[0]
        low_label = trait_info['Low Label'].values[0]
        UI_label = trait_info['Title'].values[0]  # Using 'Title' instead of 'UI Title'
        
        trait_texts = {}
        for level in selected_levels:
            generated_output = chat_chain.run(TRAIT=selected_trait, HI=high_label, LO=low_label, UI=UI_label, LEVEL=level, DESCRIPTION=trait_description)
            trait_texts[level] = generated_output
        
        for level, text in trait_texts.items():
            st.write(f"**{level.capitalize()} Level:**")
            st.write(text)

# import streamlit as st
# import pandas as pd
# import json
# from langchain_community.chat_models import ChatOpenAI
# from langchain.prompts import PromptTemplate 
# from langchain.chains import LLMChain

# from system_messages import *

# st.set_page_config(page_title='TrueYou Content Generator', page_icon=None, layout="wide")

# st.title('TrueYou Content Generation')
# st.markdown("## Activities Generator")

# activity_type = st.radio("Choose the type of activities to generate:", ('Trait-Specific', 'Generic'))

# # Load DataFrames with new structure
# qs = pd.read_csv('Updated App Test 6_5_25 - Items.csv')
# scales_df = pd.read_csv('Updated App Test 6_5_25 - Scales.csv')

# # Create scale options using Scale column from scales CSV and get corresponding Scale Key from items CSV
# scale_options = []
# for _, row in scales_df.iterrows():
#     trait_key = row['Scale']  # This is actually the trait key
#     title = row['Title']
#     # Find the corresponding Scale Key from the items CSV
#     scale_key_row = qs[qs['Trait Key'] == trait_key].iloc[0] if len(qs[qs['Trait Key'] == trait_key]) > 0 else None
#     if scale_key_row is not None:
#         scale_key = scale_key_row['Scale Key']
#         scale_options.append(f"{row['Scale']} — {row['Title']} ({scale_key})")
#         # scale_options.append(f"{title} ({scale_key})")
#     else:
#         # Fallback if no matching scale key found
#         scale_options.append(f"{row['Scale']} — {row['Title']} ({scale_key})")

#         # scale_options.append(f"{title} ({trait_key})")

# # Sort by scale key (the part in parentheses) - alphabetically then numerically
# def sort_key(option):
#     scale_key = option.split(" (")[-1].rstrip(")")
#     # Extract letter and number parts for proper sorting
#     letter = ''.join(filter(str.isalpha, scale_key))
#     number = ''.join(filter(str.isdigit, scale_key))
#     return (letter, int(number) if number else 0)

# scale_options.sort(key=sort_key)

# if activity_type == 'Trait-Specific':
#     prompt = generate_eight_activities
#     selected_scale_display = st.selectbox("Select which scale you'd like to generate activities for:", scale_options, key='activities')
#     # Extract the scale key from the display format "Title (scale_key)" 
#     selected_scale_key = selected_scale_display.split(" (")[-1].rstrip(")")
#     # Find the corresponding trait key for this scale key
#     trait_key_row = qs[qs['Scale Key'] == selected_scale_key].iloc[0] if len(qs[qs['Scale Key'] == selected_scale_key]) > 0 else None
#     if trait_key_row is not None:
#         selected_trait_key = trait_key_row['Trait Key']
#         scale_items_dict = {selected_trait_key: qs[qs['Trait Key'] == selected_trait_key]['Item Text'].tolist()}
#     else:
#         # Fallback - shouldn't happen if data is aligned
#         scale_items_dict = {selected_scale_key: []}
# else:
#     # For generic activity generation, no need for scale selection
#     prompt = generate_generic_activities
#     input = st.text_input("Enter any additional context you might want to give to generate these generic/univerally applicable activities")

# if st.button('Submit'):
#     with st.spinner('Generating activities...'):
#         for_df = []
#         ideations = []  # Store ideation texts here

#         chat_model = ChatOpenAI(openai_api_key=st.secrets['API_KEY'], model_name='gpt-4o-2024-05-13', temperature=0.2)
#         chat_chain = LLMChain(prompt=PromptTemplate.from_template(prompt), llm=chat_model)
        
#         if activity_type == 'Trait-Specific':    
#             for trait_key, items in scale_items_dict.items():
#                 items_str = ", ".join(items)
            
#             generated_output = chat_chain.run(SCALE=trait_key, ITEMS=items_str)
            
#         else:
#             generated_output = chat_chain.run(INPUT=input)
            
#         # Splitting the generated_output into ideation and activities parts
#         ideation_part, activities_json = generated_output.split('ACTIVITIES:')
#         ideations.append(ideation_part.strip().removeprefix('IDEATION:').strip())  # Add the ideation text to the list
            
#         for_df.extend(json.loads(activities_json.strip()))  # Strip in case there's leading/trailing whitespace
        
#         # Displaying ideations in an expander
#         with st.expander("Ideation behind these activities"):
#             for ideation in ideations:
#                 st.write(ideation)
        
#         # Convert the list of activities into a DataFrame
#         df = pd.DataFrame(for_df)

#         # Adjust the DataFrame as per the developer's requirements

#         # 1. Rename columns to match the required names
#         df.rename(columns={
#             'Trait Level': 'score',
#             'Trait': 'trait',
#             'Title': 'title',
#             'Description': 'description',
#             'Activity': 'activity',
#             'Categorization': 'aspect',
#             'Domain': 'category',
#             'Activity Type': 'type'
#         }, inplace=True)

#         # 2. Create 'trait_value' column by combining 'trait' and 'score'
#         df['trait_value'] = df['trait'].str.lower() + '/' + df['score'].str.lower()

#         # 3. Convert 'trait', 'score', and 'trait_value' to lowercase
#         df['trait'] = df['trait'].str.lower()
#         df['score'] = df['score'].str.lower()
#         df['trait_value'] = df['trait_value'].str.lower()

#         # 4. Map 'aspect' values to correct wording
#         aspect_mapping = {
#             'HARNESS ADVANTAGES': 'strength',
#             'ADDRESS DISADVANTAGES': 'blindspot'
#         }
#         df['aspect'] = df['aspect'].map(aspect_mapping)

#         # 5. Convert 'category' to lowercase (or title case if needed)
#         df['category'] = df['category'].str.lower()  # Use .str.title() if title case is needed

#         # 6. Map 'type' values to correct wording
#         type_mapping = {
#             'TIMED ACTIVITY': 'timed',
#             'REFLECTION': 'reflection'
#         }
#         df['type'] = df['type'].map(type_mapping)

#         # 7. Reorder columns to match the desired order
#         desired_order = ['trait', 'score', 'trait_value', 'title', 'description', 'activity', 'aspect', 'category', 'type']
#         df = df[desired_order]

#         # Display the adjusted DataFrame
#         st.write('Generated activities:')
#         st.dataframe(df)

#         # Convert DataFrame to CSV string
#         csv = df.to_csv(index=False)

#         # Create a download button and offer the CSV string for download
#         st.download_button(
#             label="Download this as CSV",
#             data=csv,
#             file_name='generated_activities.csv',
#             mime='text/csv',
#         )

# st.write("---")
# st.markdown("## Insights Generator")

# # Use the same scale options for insights
# selected_scales_insights = st.multiselect("Select which scales you'd like to generate insights for:", scale_options, key='insights')
# N = st.number_input("Number of insights to generate for each HIGH and LOW scorer per trait:", min_value=1, max_value=10, value=3)

# horoscopify = st.checkbox('Horoscopify?')

# if st.button('Submit', key='insights_submit'):
#     with st.spinner('Generating insights...'):
#         if horoscopify:
#             prompt = insights_generation_horoscopify
#         else:
#             prompt = insights_generation_standard
            
#         chat_model = ChatOpenAI(openai_api_key=st.secrets['API_KEY'], model_name='gpt-4o-2024-08-06', temperature=0.2)
#         chat_chain = LLMChain(prompt=PromptTemplate.from_template(prompt), llm=chat_model)
        
#         # Extract scale keys from the selected display options
#         selected_trait_keys = []
#         for display_option in selected_scales_insights:
#             scale_key = display_option.split(" (")[-1].rstrip(")")
#             # Find the corresponding trait key for this scale key
#             trait_key_row = qs[qs['Scale Key'] == scale_key].iloc[0] if len(qs[qs['Scale Key'] == scale_key]) > 0 else None
#             if trait_key_row is not None:
#                 selected_trait_keys.append(trait_key_row['Trait Key'])
        
#         generated_output = chat_chain.run(SCALES=selected_trait_keys, N=N)
#         make_df = json.loads(generated_output)
    
#     df = pd.DataFrame(make_df)
#     st.write('Generated insights:')
#     st.write(make_df)
#     with st.expander('See insights in spreadsheeet view'):
#         st.dataframe(df, use_container_width=True)

#     # Convert DataFrame to CSV string
#     insights_csv = df.to_csv(index=False)
    
#     # Create a download button and offer the CSV string for download
#     st.download_button(
#         label="Download this as CSV",
#         data=insights_csv,
#         file_name='generated_insights.csv',
#         mime='text/csv',
#     )

# st.write("---")
# st.markdown("## Trait Text Generator")

# # Use the same scale options for trait text generator (same format as other dropdowns)
# selected_trait_display = st.selectbox("Select a trait:", scale_options)
# # Extract the scale key from the display format "Title (scale_key)" 
# selected_scale_key = selected_trait_display.split(" (")[-1].rstrip(")")
# # Find the corresponding trait key for this scale key
# trait_key_row = qs[qs['Scale Key'] == selected_scale_key].iloc[0] if len(qs[qs['Scale Key'] == selected_scale_key]) > 0 else None
# if trait_key_row is not None:
#     selected_trait = trait_key_row['Trait Key']
# else:
#     # Fallback - shouldn't happen if data is aligned
#     selected_trait = selected_scale_key

# selected_levels = st.multiselect("Select levels to generate text for:", ['low', 'medium', 'high'])

# if st.button('Submit', key='trait_text_submit'):
#     with st.spinner('Generating trait text...'):
#         chat_model = ChatOpenAI(openai_api_key=st.secrets['API_KEY'], model_name='gpt-4o-2024-05-13', temperature=0.2)
#         chat_chain = LLMChain(prompt=PromptTemplate.from_template(trait_text_generation), llm=chat_model)
        
#         trait_info = scales_df[scales_df['Scale'] == selected_trait]
#         trait_description = trait_info['Description'].values[0]
#         high_label = trait_info['High Label'].values[0]
#         low_label = trait_info['Low Label'].values[0]
#         UI_label = trait_info['Title'].values[0]  # Using 'Title' instead of 'UI Title'
        
#         trait_texts = {}
#         for level in selected_levels:
#             generated_output = chat_chain.run(TRAIT=selected_trait, HI=high_label, LO=low_label, UI=UI_label, LEVEL=level, DESCRIPTION=trait_description)
#             trait_texts[level] = generated_output
        
#         for level, text in trait_texts.items():
#             st.write(f"**{level.capitalize()} Level:**")
#             st.write(text)
