import streamlit as st
import pandas as pd
from openai import OpenAI
import tiktoken
import random

# Initialize session state for token counting
if 'total_session_tokens' not in st.session_state:
    st.session_state.total_session_tokens = 0

st.title("Customer Review Sentiment Analyzer")
st.markdown("This app analyzes the sentiment of customer reviews to gain insights into their opinions.")

# OpenAI API Key input
openai_api_key = st.sidebar.text_input(
    "Enter your OpenAI API Key", 
    type="password", 
    help="You can find your API key at https://platform.openai.com/account/api-keys"
)

def get_token_comment(token_count):
    """Get a creative comment about token usage from OpenAI."""
    client = OpenAI(api_key=openai_api_key)
    prompt = f"""Write a single short, witty sentence about someone who has used {token_count} tokens in their API calls.
    Make it funny and creative, mentioning the specific token count. Keep it under 100 characters.
    Example: "Using 1234 tokens? Someone's been doing their NLP cardio! 💪"
    """
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a witty assistant who makes short, fun comments about API usage."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return completion.choices[0].message.content

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """Count the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def classify_sentiment_openai(review_text):
    """
    Classify the sentiment of a customer review using OpenAI's GPT-3.5-turbo model.
    Parameters:
        review_text (str): The customer review text to be classified.
    Returns:
        str: The sentiment classification of the review as a single word, "Positive", "Negative", or "Neutral".
    """
    client = OpenAI(api_key=openai_api_key)
    prompt = f'''
        Classify the following customer review. 
        State your answer
        as a single word, "positive", 
        "negative" or "neutral":

        {review_text}
        '''

    # Count tokens before making the API call
    system_message = "You are a helpful assistant."
    total_tokens = count_tokens(system_message) + count_tokens(prompt)
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {
                "role": "user",
                "content": prompt
            }
        ]
    ) 

    # Get response tokens
    response_tokens = completion.usage.total_tokens
    
    # Update session total
    st.session_state.total_session_tokens += response_tokens

    # Return both the sentiment and token counts
    return completion.choices[0].message.content.title(), total_tokens, response_tokens

# Single review analysis
st.subheader("Analyze a Single Review")
user_input = st.text_input("Enter a customer review")
if user_input:  # Only analyze if there's input
    sentiment, input_tokens, total_tokens = classify_sentiment_openai(user_input)
    st.write("Sentiment:", sentiment)

# Batch analysis with CSV
st.subheader("Analyze Multiple Reviews from CSV")
uploaded_file = st.file_uploader("Upload a CSV file with restaurant reviews", type="csv")

# Once the user uploads a csv file:
if uploaded_file is not None:
    reviews_df = pd.read_csv(uploaded_file)
    
    # Check if the data has a text column
    text_columns = reviews_df.select_dtypes(include="object").columns

    if len(text_columns) == 0:
        st.error("No text column found in the uploaded file.")
    else:
        # Show a dropdown menu to select the review column
        review_column = st.selectbox("Select the review column with the customer reviews", text_columns)
        
        if st.button("Analyze Reviews"):
            # Add a progress bar
            progress_bar = st.progress(0)
            
            # Initialize counters
            total_tokens_used = 0
            reviews_df["sentiment"] = ""  # Initialize sentiment column
            
            # Analyze the sentiment of the reviews
            total_reviews = len(reviews_df)
            
            for i, review in enumerate(reviews_df[review_column]):
                sentiment, input_tokens, response_tokens = classify_sentiment_openai(review)
                reviews_df.loc[i, "sentiment"] = sentiment
                total_tokens_used += response_tokens
                # Update progress bar
                progress_bar.progress((i + 1) / total_reviews)
            
            # Show results
            st.success("Analysis complete!")
            st.write("Results:")
            st.write(reviews_df)

            # Calculate sentiment counts
            sentiment_counts = reviews_df["sentiment"].value_counts()

            # Display metrics in 3 columns
            st.subheader("Sentiment Distribution")
            col1, col2, col3 = st.columns(3)

            with col1:
                # show the number of positive reviews and the percentage
                positive_count = sentiment_counts.get("Positive", 0)
                st.metric("Positive", positive_count, f"{positive_count / len(reviews_df) * 100:.2f}%")

            with col2:
                # show the number of negative reviews and the percentage
                negative_count = sentiment_counts.get("Negative", 0)
                st.metric("Negative", negative_count, f"{negative_count / len(reviews_df) * 100:.2f}%")

            with col3:
                # show the number of neutral reviews and the percentage
                neutral_count = sentiment_counts.get("Neutral", 0)
                st.metric("Neutral", neutral_count, f"{neutral_count / len(reviews_df) * 100:.2f}%")

# Display consolidated token usage at the bottom
st.markdown("---")  # Add a divider
st.subheader("Token Usage Summary")

# Get a creative comment about the token usage
if st.session_state.total_session_tokens > 0:
    token_comment = get_token_comment(st.session_state.total_session_tokens)
else:
    token_comment = "Waiting for you to start analyzing... The tokens are getting restless! 🎭"

st.info(f"""
📊 Session Statistics:
- Total Tokens: {st.session_state.total_session_tokens:,}
- Approximate Cost: ${st.session_state.total_session_tokens * 0.000002:.4f} USD

{token_comment}
""")
