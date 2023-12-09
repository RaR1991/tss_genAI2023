import pandas as pd
import openai
openai.api_type = "azure"
# openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") 
# openai.api_key = os.getenv("AZURE_OPENAI_KEY")

openai.api_key = "524e5269ea524937afde1488f7f9a769"
openai.api_base = 'https://genai23-01.openai.azure.com'
openai.api_version = "2023-05-15"
# Stop words list
stop_words = ["the", "is", "but", "and", "in", "of", "a", "to", "for", "my", "with", "not", "has", "when", "it", "I", "you", "he", "she", "we", "they", "are", "that"]

def preprocess_text(text):
    # Tokenize the text and remove stop words
    tokens = [word.strip().lower() for word in text.split() if word.strip().lower() not in stop_words]
    return " ".join(tokens)

def categorize_review(review):
    # Preprocess the review text
    preprocessed_review = preprocess_text(review)

    # Call the OpenAI API for categorization
    response = openai.ChatCompletion.create(
        engine="gpt-model-01",
        temperature=0.7,
        messages=[
            {"role": "system", "content": "As an AI assistant, your primary task is to meticulously categorize and organize reviews for a food delivery service based on three key criteria: Department (IT, Finance, Logistics), Severity (on a scale from 1 to 10), and Review Type (Bug, Complaint, Suggestion, Praise, Request). Your goal is to generate an output format that adheres to the structure '(Department, Severity, Type)', for instance, 'Finance, 03, Complaint' or 'IT, 08, Bug'. nothing is needed for now just respond by Yes."},
            {"role": "assistant", "content": "Yes."},
            {"role": "system", "content": "the reviews are in this format: user rating review_text, for example kirkteresa 4,7 Efficient delivery service, but the app's interface could use a revamp for a more modern and intuitive feel."},
            {"role": "user", "content": f"categorize this review: {preprocessed_review}"}
        ]
    )

    # Extract and return the result
    result = response['choices'][0]['message']['content']
    return result

def process_reviews(file_path):
    # Load the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path, sheet_name=0)

    # Add new columns for department, severity, and review type
    df["department"] = None
    df["severity"] = None
    df["re_type"] = None

    # Iterate through the dataframe and categorize reviews
    for index, row in df.iterrows():
        review_text = " ".join(str(row[key]) for key in row.keys()[:10])  # Combine the first 10 columns as review text
        preprocessed_review = preprocess_text(review_text)
        ai_result = categorize_review(preprocessed_review)

        # Extract information and update the dataframe
        if len(ai_result.split(",")) == 3:
            try:
                df.at[index, "department"] = ai_result.split(",")[0].strip()
                df.at[index, "severity"] = int(ai_result.split(",")[1].strip())
                df.at[index, "re_type"] = ai_result.split(",")[2].strip()
            except ValueError:
                pass  # Handle the case where severity is not a valid integer

    # Display the updated DataFrame
    return df
