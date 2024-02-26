import streamlit as st
import pandas as pd
import json
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate 
from langchain.chains import LLMChain

from system_messages import *

# Assuming the DataFrame 'qs' is loaded as shown
qs = pd.read_csv('questions.csv')

# Sort 'qs' and generate 'scale_options'
sorted_df = qs.sort_values(by=['Cat', 'Scale Name'])
scale_options = [f"{row['Scale Name']} ({row['Cat']})" for _, row in sorted_df.drop_duplicates(['Scale Name', 'Cat']).iterrows()]

# User selects scales
selected_scales = st.multiselect("Select which scales you'd like to generate activities for:", scale_options)

# Extract just the scale names from the selected options
selected_scale_names = [s.split(" (")[0] for s in selected_scales]

# Adjust the filtering step
scale_items_dict = qs[qs['Scale Name'].isin(selected_scale_names)].groupby('Scale Name')['Item Text'].apply(list).to_dict()

# qs = pd.read_csv('questions.csv')
# sorted_df = qs.sort_values(by=['Cat', 'Scale Name'])
# scale_options = [f"{row['Scale Name']} ({row['Cat']})" for _, row in sorted_df.drop_duplicates(['Scale Name', 'Cat']).iterrows()]
# selected_scales = st.multiselect("Select which scales you'd like to generate activities for:", scale_options)

# scale_items_dict = qs[qs['Scale Name'].isin(selected_scales)].groupby('Scale Name')['Item Text'].apply(list).to_dict()

four_or_eight = st.radio(
    "Choose your option:",
    ('Force positive/negative activity for each trait level (generates 8 activities)', 
     'Leave positive/negative assignment to LLM (generates 4 activities)')
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
    st.write(scale_items_dict)
    st.dataframe(pd.DataFrame(for_df))
