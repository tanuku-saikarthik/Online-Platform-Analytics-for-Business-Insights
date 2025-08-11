import re
import pandas as pd
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT

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

if __name__ == '__main__':
    # List of file names (in the same directory)
    file_names = ['KeybertFile1.csv', 'KeybertFile2.csv', 'KeybertFile3.csv']

    # Load and combine all data
    dfs = [pd.read_csv(file)[['Review Text', 'Product Name']] for file in file_names]
    combined_df = pd.concat(dfs, ignore_index=True)

    # Clean the review text
    combined_df['Cleaned Review Text'] = combined_df['Review Text'].astype(str).apply(clean_text)

    # Load the embedding model and initialize KeyBERT
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")
    kw_model = KeyBERT(model=embedding_model)

    # Extract keywords
    combined_df['Keywords'] = combined_df['Cleaned Review Text'].apply(
        lambda text: [kw[0] for kw in kw_model.extract_keywords(text, top_n=5)]
    )

    # Final output with required columns
    output_df = combined_df[['Review Text', 'Product Name', 'Keywords']]
    output_df.to_csv('KeywordsExtracted.csv', index=False)
    print("Final output saved to KeywordsExtracted.csv")
