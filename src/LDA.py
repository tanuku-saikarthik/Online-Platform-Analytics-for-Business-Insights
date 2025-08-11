import os
import re
import gensim
import numpy as np
import pandas as pd
from gensim import corpora
from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet, words
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
english_vocab = set(words.words())
GENERIC_WORDS = {"phone", "good", "also", "like", "work", "overall", "everything", "nice", "use",
                 "anyone", "feel", "think", "product", "mobile", "device", "without", "whether",
                 "even", "come", "ever", "day", "want"}

# Define the function to remove emojis from the text
def remove_emojis(text):
    emoji_pattern = re.compile(r"[\U00010000-\U0010FFFF]", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# Define the function to remove all special characters from text
def remove_special_characters(text):
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

# Define the function to tokenize text
def tokenize_text(text):
    return word_tokenize(text)

# Define the function to remove non-English words from tokenized text
def remove_non_english_words(tokenized_text):
    return [word for word in tokenized_text if word.lower() in english_vocab]

# Define the function to remove stopwords
def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    return [word.lower() for word in text if word.lower() not in stop_words and word.isalpha()]

# Define the function to map NLTK POS tags to WordNet POS tags
def get_wordnet_pos(word):
    tag = pos_tag([word])[0][1][0].upper()  # Get first letter of POS tag
    tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)  # Default to noun if not found

# Define the function to lemmatize words and remove duplicates while keeping order
def lemmatize_and_remove_duplicates(text):
    lemmatizer = WordNetLemmatizer()
    seen = set()
    unique_words = []
    for word in text:
        lemma = lemmatizer.lemmatize(word, get_wordnet_pos(word))
        if lemma not in seen:
            seen.add(lemma)
            unique_words.append(lemma)
    return unique_words

# Define the function to combine reviews from Amazon and Flipkart
def combine_reviews(Amazon_file, Flipkart_file, df, all_reviews_file):
    if not os.path.exists(all_reviews_file):
        df1 = pd.read_csv(Amazon_file)
        df2 = pd.read_csv(Flipkart_file)
        df1 = df1[['Review Text']]
        df2 = df2[['Review Text']]
        combined_df = pd.concat([df1, df2, df], ignore_index=True)
        combined_df.to_csv(all_reviews_file, index=False)
        print("AllReviews.csv created successfully!")
    else:
        print("AllReviews.csv already exists. Skipping this step.")

# Define the function to remove emojis from reviews and save to CSV
def remove_emojis_from_reviews(all_reviews_file, reviews_without_emojis_file):
    if not os.path.exists(reviews_without_emojis_file):
        reviews_df = pd.read_csv(all_reviews_file)
        reviews_df['Review Text'] = reviews_df['Review Text'].astype(str).apply(remove_emojis)
        reviews_df.to_csv(reviews_without_emojis_file, index=False)
        print("ReviewsWithoutEmojis.csv created successfully!")
    else:
        print("ReviewsWithoutEmojis.csv already exists. Skipping this step.")

# Define the function to remove special characters from reviews and save to CSV
def remove_special_characters_from_reviews(reviews_without_emojis_file, reviews_without_special_characters_file):
    if not os.path.exists(reviews_without_special_characters_file):
        reviews_df = pd.read_csv(reviews_without_emojis_file)
        reviews_df['Review Text'] = reviews_df['Review Text'].astype(str).apply(remove_special_characters)
        reviews_df.to_csv(reviews_without_special_characters_file, index=False)
        print("ReviewsWithoutSpecialCharacters.csv created successfully!")
    else:
        print("ReviewsWithoutSpecialCharacters.csv already exists. Skipping this step.")

# Define the function to tokenize reviews and save to CSV
def tokenize_reviews(reviews_without_special_characters_file, tokenized_reviews_file):
    if not os.path.exists(tokenized_reviews_file):
        reviews_df = pd.read_csv(reviews_without_special_characters_file)
        reviews_df['Review Text'] = reviews_df['Review Text'].astype(str).apply(tokenize_text)
        reviews_df['Review Text'] = reviews_df['Review Text'].apply(remove_non_english_words)
        reviews_df.to_csv(tokenized_reviews_file, index=False)
        print("TokenizedReviews.csv created successfully!")
    else:
        print("TokenizedReviews.csv already exists. Skipping this step.")

# Define the function to remove stopwords and generic words from reviews and save to CSV
def remove_stopwords_from_reviews(tokenized_reviews_file, reviews_without_stopwords_file):
    if not os.path.exists(reviews_without_stopwords_file):
        reviews_df = pd.read_csv(tokenized_reviews_file)
        reviews_df['Review Text'] = reviews_df['Review Text'].apply(eval).apply(lambda tokens: [
            word for word in remove_stopwords(tokens)
            if (len(word) >= 3) and word not in GENERIC_WORDS
        ])
        reviews_df.to_csv(reviews_without_stopwords_file, index=False)
        print("ReviewsWithoutStopWords.csv created successfully!")
    else:
        print("ReviewsWithoutStopWords.csv already exists. Skipping this step.")

# Define the function to lemmatize reviews and save to CSV
def lemmatize_reviews(reviews_without_stopwords_file, reviews_lemmatized_file):
    if not os.path.exists(reviews_lemmatized_file):
        reviews_df = pd.read_csv(reviews_without_stopwords_file)
        reviews_df['Review Text'] = reviews_df['Review Text'].apply(eval).apply(lemmatize_and_remove_duplicates)
        reviews_df.to_csv(reviews_lemmatized_file, index=False)
        print("ReviewsLemmatized.csv created successfully!")
    else:
        print("ReviewsLemmatized.csv already exists. Skipping this step.")

# Define the function to create dictionary and corpus for LDA
def create_lda_dictionary_and_corpus(reviews_lemmatized_file, lda_dictionary_file, lda_corpus_file):
    if not (os.path.exists(lda_dictionary_file) and os.path.exists(lda_corpus_file)):
        reviews_df = pd.read_csv(reviews_lemmatized_file)
        reviews_df['Review Text'] = reviews_df['Review Text'].apply(eval)
        dictionary = corpora.Dictionary(reviews_df['Review Text'])
        corpus = [dictionary.doc2bow(text) for text in reviews_df['Review Text']]
        dictionary.save(lda_dictionary_file)
        gensim.corpora.MmCorpus.serialize(lda_corpus_file, corpus)
        print("Dictionary and Corpus for LDA created successfully!")
    else:
        dictionary = corpora.Dictionary.load(lda_dictionary_file)
        corpus = gensim.corpora.MmCorpus(lda_corpus_file)
        print("Dictionary and Corpus for LDA loaded successfully.")
    return dictionary, corpus

# Define the function to load or train the LDA model
def train_or_load_lda_model(corpus, dictionary, lda_model_file):
    if not os.path.exists(lda_model_file):
        num_topics = 8
        lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, alpha=0.5, eta=0.5, iterations=400, passes=30)
        lda_model.save(lda_model_file)
        print("LDA model trained and saved successfully!")
    else:
        lda_model = LdaModel.load(lda_model_file)
        print("LDA model loaded successfully!")
    return lda_model

# Define the function to calculate the Coherence Score
def calculate_coherence_score(lda_model, reviews_lemmatized_file, dictionary):
    reviews_df = pd.read_csv(reviews_lemmatized_file)
    reviews_df['Review Text'] = reviews_df['Review Text'].apply(eval)
    coherence_model = CoherenceModel(model=lda_model, texts=reviews_df['Review Text'], dictionary=dictionary, coherence='c_v')
    coherence_score = coherence_model.get_coherence()
    print("\nCoherence Score:", coherence_score)

# Define the function to calculate the perplexity score
def calculate_perplexity(lda_model):
    perplexity = lda_model.log_perplexity(corpus)
    print(f"Perplexity: {perplexity}")
    print(f"Exponentiated Perplexity: {np.exp(perplexity)}")

# Define the function to print top words
def print_top_words(lda_model):
    print("\n--- Top Words for Each Topic ---\n")
    for i, topic in lda_model.print_topics(num_topics=20, num_words=10):
        print(f"Topic {i}: {topic}")

# Main entry point for the script
if __name__ == '__main__':
    Amazon_file = r"C:\Users\Rinchal shete\OneDrive\Desktop\AmazonReviewsFinal.csv"
    Flipkart_file = r"C:\Users\Rinchal shete\OneDrive\Desktop\flipkart_dataset.csv"
    all_reviews_file = r"C:\PycharmProjects\Practice\Mini-Project ( new )\AllReviews.csv"
    reviews_without_emojis_file = r"C:\PycharmProjects\Practice\Mini-Project ( new )\ReviewsWithoutEmojis.csv"
    reviews_without_special_characters_file = r"C:\PycharmProjects\Practice\Mini-Project ( new )\ReviewsWithoutSpecialCharacters.csv"
    tokenized_reviews_file = r"C:\PycharmProjects\Practice\Mini-Project ( new )\TokenizedReviews.csv"
    reviews_without_stopwords_file = r"C:\PycharmProjects\Practice\Mini-Project ( new )\ReviewsWithoutStopWords.csv"
    reviews_lemmatized_file = r"C:\PycharmProjects\Practice\Mini-Project ( new )\ReviewsLemmatized.csv"
    lda_dictionary_file = r"C:\PycharmProjects\Practice\Mini-Project ( new )\lda_dictionary.dict"
    lda_corpus_file = r"C:\PycharmProjects\Practice\Mini-Project ( new )\lda_corpus.mm"
    lda_model_file = r"C:\PycharmProjects\Practice\Mini-Project ( new )\lda_model"
    file = r"C:\Users\Rinchal shete\Downloads\cell_phone_reviews.csv"
    df = pd.read_csv(file)
    df = df[['text']].rename(columns={'text': 'Review Text'})
    combine_reviews(Amazon_file, Flipkart_file, df, all_reviews_file)
    remove_emojis_from_reviews(all_reviews_file, reviews_without_emojis_file)
    remove_special_characters_from_reviews(reviews_without_emojis_file, reviews_without_special_characters_file)
    tokenize_reviews(reviews_without_special_characters_file, tokenized_reviews_file)
    remove_stopwords_from_reviews(tokenized_reviews_file, reviews_without_stopwords_file)
    lemmatize_reviews(reviews_without_stopwords_file, reviews_lemmatized_file)
    dictionary, corpus = create_lda_dictionary_and_corpus(reviews_lemmatized_file, lda_dictionary_file, lda_corpus_file)
    lda_model = train_or_load_lda_model(corpus, dictionary, lda_model_file)
    calculate_coherence_score(lda_model, reviews_lemmatized_file, dictionary)
    calculate_perplexity(lda_model)
    print_top_words(lda_model)
