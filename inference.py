import openai
import streamlit as st

# Function to generate inferences from OpenAI API
def generate_inference(data_summary):
    openai.api_key = st.secrets["openai"]["api_key"]

    # Prepare a prompt for the OpenAI API
    prompt = f"Here is the data: {data_summary}. What insights can you derive from it?"

    # Call the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )

    # Return the generated inference
    return response.choices[0].text.strip()
