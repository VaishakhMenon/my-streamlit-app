import openai
import streamlit as st

# Function to generate inferences from OpenAI API with a business-friendly perspective
def generate_inference(data_summary, analysis_type):
    # Debug statement to inspect passed parameters
    st.write(f"data_summary: {data_summary}, analysis_type: {analysis_type}")
    
    openai.api_key = st.secrets["openai"]["api_key"]

    # Prepare a business-friendly prompt for the OpenAI API
    prompt = f"""
    Here is the data summary for {analysis_type}: {data_summary}. 
    Please provide key insights in simple business terms, including:
    1. Analysis of the sales trends and performance of each strategy.
    2. Recommendations for how the business can optimize or adjust based on this analysis.
    3. Any potential risks or opportunities that the business owner should be aware of.
    """

    # Call the OpenAI ChatCompletion API
    try:
        response = openai.ChatCompletion.create(
            engine="text-davinci-003",
            prompt=prompt,
            messages=[
                {"role": "system", "content": "You are a helpful business advisor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300   # Increase max_tokens for a longer response from 150
            temperature=0.7  # You can also adjust the creativity of the response
        )

        # Return the generated business-friendly inference
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        st.error(f"Error generating inference: {e}")
        return None
