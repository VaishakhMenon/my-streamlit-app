import openai
import streamlit as st

# Function to generate inferences from OpenAI API
def generate_inference(data_summary, analysis_type):
    # Debug statement to inspect passed parameters
    st.write(f"data_summary: {data_summary}, analysis_type: {analysis_type}")
    
    openai.api_key = st.secrets["openai"]["api_key"]

    # Prepare a prompt for the OpenAI API
    prompt = f"Here is the data summary for {analysis_type}: {data_summary}. What insights can you derive from it?"

    # Call the OpenAI API
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )

        # Return the generated inference
        return response.choices[0].text.strip()

    except Exception as e:
        st.error(f"Error generating inference: {e}")
        return None
