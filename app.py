import streamlit as st
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sentiment Analyzer", layout="centered")
st.title("🧠 Sentiment Analysis App")
st.divider()

st.subheader("🗣 Analyze a Single Sentence")
st.write("Enter a sentence to analyze its sentiment.")

user_input = st.text_input("Enter your sentence:")

if user_input:
    blob = TextBlob(user_input)
    sentiment = blob.sentiment.polarity

    if sentiment > 0:
        st.success("Sentiment: Positive 😊")
    elif sentiment < 0:
        st.error("Sentiment: Negative 😞")
    else:
        st.info("Sentiment: Neutral 😐")

    st.write(f"Sentiment Score: `{sentiment}`")


st.divider()
st.subheader("📈 Sentiment Timeline from CSV File")

uploaded_file = st.file_uploader(r"C:\Users\Swet Raj\Downloads\sample_reviews_with_timestamps.csv", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if 'timestamp' in df.columns and 'review' in df.columns:
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        df['sentiment'] = df['review'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)

        def label_sentiment(score):
            if score > 0:
                return "Positive"
            elif score < 0:
                return "Negative"
            return "Neutral"

        df['label'] = df['sentiment'].apply(label_sentiment)

        df = df.sort_values('timestamp')

        st.line_chart(data=df, x='timestamp', y='sentiment', use_container_width=True)

        st.bar_chart(df['label'].value_counts())

        st.dataframe(df[['timestamp', 'review', 'sentiment', 'label']])
    else:
        st.warning("Make sure your CSV file has 'timestamp' and 'review' columns.")
