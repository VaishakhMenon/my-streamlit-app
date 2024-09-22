import openai
import streamlit as st

# Function to generate inferences from OpenAI API with a business-friendly perspective
def generate_inference(data_summary, analysis_type):
    # Debug statement to inspect passed parameters
    st.write(f"data_summary: {data_summary}, analysis_type: {analysis_type}")
    
    openai.api_key = st.secrets["openai"]["api_key"]

    # Prepare a business-friendly prompt for the OpenAI API
    prompt = f"As a business expert, please review the following {analysis_type} data summary: {data_summary}. Explain the key takeaways and insights in a clear, simple way that can help a business owner make decisions."

    # Call the OpenAI ChatCompletion API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful business advisor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )

        # Return the generated business-friendly inference
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        st.error(f"Error generating inference: {e}")
        return None
