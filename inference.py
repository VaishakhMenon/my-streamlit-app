import openai
import streamlit as st

# Function to generate inferences from OpenAI API
def generate_inference(result_summary, analysis_type):
    openai.api_key = st.secrets["openai"]["api_key"]

    # Prepare a prompt for the OpenAI API based on analysis type and result summary
    prompt = f"Here is the result of {analysis_type}: {result_summary}. What insights can you derive from it?"

    # Call the OpenAI API with the newer `chat.Completion` method
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an analysis assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # Return the generated inference
    return response['choices'][0]['message']['content'].strip()
