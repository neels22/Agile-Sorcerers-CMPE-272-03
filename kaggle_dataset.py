import pandas as pd
from textblob import TextBlob

# Load the dataset (train.csv)
df_train = pd.read_csv("train.csv", encoding='ISO-8859-1')

# Clean the 'text' column to ensure it's a string
df_train['text'] = df_train['text'].fillna('')  # Fill NaN values with an empty string
df_train['text'] = df_train['text'].astype(str)  # Convert everything to a string

# Define the sentiment analysis function
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Apply sentiment analysis to the 'text' column
df_train["Predicted Sentiment"] = df_train["text"].apply(analyze_sentiment)

# Display the results
print(df_train[["text", "Predicted Sentiment"]].head(10))

# Optionally, save the results to a new CSV
df_train.to_csv("train_sentiment_results.csv", index=False)
