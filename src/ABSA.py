import pandas as pd
from collections import Counter
import ast
import time
start_time = time.time()
df = pd.read_csv(r'C:\PycharmProjects\Practice\Mini-Project ( new )\KeywordsExtracted.csv')
end_time = time.time()
print(f"Time for reading the file: {end_time - start_time:.2f} seconds")
start_time = time.time()
df['Keywords'] = df['Keywords'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
end_time = time.time()
print(f"Time for converting 'Keywords' column: {end_time - start_time:.2f} seconds")
aspects = {
    "battery", "camera", "screen", "price", "quality", "performance", "features",
    "charging", "memory", "storage", "service", "network", "display", "fingerprint", "apps", "warranty",
    "speaker", "bluetooth", "processor", "wifi", "updates", "budget", "resolution", "audio", "cost"
}
start_time = time.time()
def has_top_keyword(keywords):
    return any(kw in aspects for kw in keywords)
df_filtered = df[df['Keywords'].apply(has_top_keyword)]
end_time = time.time()
print(f"Time for filtering reviews: {end_time - start_time:.2f} seconds")
print(f"Number of reviews after filtering: {df_filtered.shape[0]}")
df_filtered.to_csv(r'C:\PycharmProjects\Practice\Mini-Project ( new )\filtered_reviews.csv', index=False)
start_time = time.time()
df_exploded = df_filtered.explode('Keywords')
df_exploded = df_exploded[df_exploded['Keywords'].isin(aspects)]
df_exploded = df_exploded.rename(columns={'Keywords': 'Aspect'})
end_time = time.time()
print(f"Time for exploding and filtering keywords: {end_time - start_time:.2f} seconds")
print(f"Number of rows after exploding: {df_exploded.shape[0]}")
df_exploded.to_csv(r'C:\PycharmProjects\Practice\Mini-Project ( new )\exploded_reviews.csv', index=False)






import pandas as pd
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import time
nltk.download('vader_lexicon')
def remove_emojis(text):
    emoji_pattern = re.compile(r"[\U00010000-\U0010FFFF]", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)
def remove_special_characters(text):
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)
def clean_text(text):
    text = remove_emojis(text)
    text = remove_special_characters(text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text
start_time = time.time()
df_exploded = pd.read_csv(r'C:\PycharmProjects\Practice\Mini-Project ( new )\exploded_reviews.csv')
end_time = time.time()
print(f"Time for loading exploded reviews: {end_time - start_time:.2f} seconds")
start_time = time.time()
df_exploded['Cleaned Review'] = df_exploded['Review Text'].apply(clean_text)  # Assuming the review text column is 'Review_Text'
end_time = time.time()
print(f"Time for cleaning reviews: {end_time - start_time:.2f} seconds")
start_time = time.time()
sid = SentimentIntensityAnalyzer()
df_exploded['Sentiment Score'] = df_exploded['Cleaned Review'].apply(lambda x: sid.polarity_scores(x)['compound'])
def classify_sentiment(score):
    if score >= 0.1:
        return 'Positive'
    elif score <= -0.1:
        return 'Negative'
    else:
        return 'Neutral'
df_exploded['Sentiment Label'] = df_exploded['Sentiment Score'].apply(classify_sentiment)
end_time = time.time()
print(f"Time for sentiment analysis: {end_time - start_time:.2f} seconds")
start_time = time.time()
summary = df_exploded.groupby(['Product Name', 'Aspect']).agg(
    Avg_Sentiment=('Sentiment Score', 'mean'),
    Mentions=('Aspect', 'count'),
    Positive_Percent=('Sentiment Label', lambda x: (x == 'Positive').mean() * 100),
    Negative_Percent=('Sentiment Label', lambda x: (x == 'Negative').mean() * 100),
).reset_index()
summary_sorted = summary.sort_values(by='Mentions', ascending=False)
end_time = time.time()
print(f"Time for aggregating insights: {end_time - start_time:.2f} seconds")
summary_sorted.to_csv(r'C:\PycharmProjects\Practice\Mini-Project ( new )\Aspect_Sentiment_Summary.csv', index=False)
print("Saved the summary to 'Aspect_Sentiment_Summary.csv'")
print(summary_sorted.head())






import pandas as pd
products_to_remove = [
    'Galaxy S6 Screen Protector', 'Samsung Galaxy M35 5G', 'realme NARZO 70 Turbo 5G',
    'realme NARZO 70x 5G', 'OnePlus Nord CE4 Lite 5G', 'Redmi Note 13 5G', 'Motorola G85 5G',
    'realme P1 5G', 'Redmi 13C 5G', 'vivo T3 Pro 5G', 'Redmi A4 5G', 'Samsung Galaxy M15 5G Prime Edition',
    'vivo T3 5G', 'OPPO K12x 5G with 45W SUPERVOOC Charger In-The-Box', 'Motorola Edge 50 Pro 5G with 125W Charger',
    'Moto G PLUS', 'Motorola g45 5G', 'vivo T3 Lite 5G', 'Samsung Galaxy M05', 'Motorola g64 5G',
    'I9220(N9000)', 'Infinix Note 40X 5G', 'Redmi Note 14 5G', 'Moto G', 'OPPO Reno13 5G', 'MOTOROLA g35 5G',
    'Apple iPhone 16', 'Kyocera Vibe', 'SAMSUNG Galaxy F05', 'Unlocked Smart Product', 'RCA Reno', 'Pixel Phone 3',
    'Bold N2', 'DOOGEE X98 PRO', 'Azumi iPhone SE', 'MOTOROLA g05', 'POCO C75 5G', 'CUBOT Note 20 Pro',
    'LG Optimus F7', 'UMIDIGI Mobile One', 'UMIDIGI F3 5G', 'Ulefone Note 12P', 'LG Fiesta', 'DOOGEE N30',
    'IsatPhone 2.1', 'RCA Q1', 'Ulefone Note 6T', 'iRULU Victory 1', 'Jethro SC490', 'LG 800G', 'LG Optimus Extreme',
    'BLU Tank T190i', 'HOTWAV 2022', 'ErnestWoolomd Headphone Earbuds Jack Adapter', 'Blu Studio C Mini', 'Juicebox Battery',
    'SAMSUNG G991U', 'Dell Venue Pro', 'DOOGEE Rugged Smartphone', 'Life One Quad Band', 'Motorola G45 5G',
    'BLU Dash Music 4.0', 'SOYES XS11', 'POSH Titan HD E500a', 'POSH Orion Mini S350a', 'Motorola A630', 'LG Transpyre',
    'AT&T Z221', 'BLU Vivo X5', 'SpinBot IceDot Mag v1 Magnetic Semiconductor Mobile Cooler',
    '4G Android Smartphone', '4G Smart Watch Phone', '5.7 Inch Smartphone', '6.3inch LTE 4G Unlocked Phone'
]

df = pd.read_csv('Aspect_Sentiment_Summary.csv')
df_filtered = df[~df['Product Name'].isin(products_to_remove)]
df_filtered.to_csv('Filtered_Aspect_Sentiment_Summary.csv', index=False)
print(df_filtered)





