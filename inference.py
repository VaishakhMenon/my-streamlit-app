def generate_inference(data_summary, analysis_type):
    openai.api_key = st.secrets["openai"]["api_key"]

    # Modify the prompt to focus on business insights
    prompt = f"As a business strategist, analyze the {analysis_type} data provided here: {data_summary}. Provide key insights and business recommendations based on the analysis."

    # Call the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )

    st.write(f"data_summary: {data_summary}, analysis_type: {analysis_type}")

    # Return the generated inference
    return response.choices[0].text.strip()


