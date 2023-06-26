"""This File will be imported to main. It includes all text formatting 
functionlity to form a list of keywords in german and english
that can be compared against each other"""

# Import Packages

# Translation
from deep_translator import GoogleTranslator
from langdetect import detect

# Type Hinting
from typing import Dict, List, Tuple
from pathlib import Path

# String formatting
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Stemmer or Lemmatizer
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer

# Data Analysis Tools
# from nltk import FreqDist

# NLTK Downloads
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("punkt")

# Stop words in German DE
stop_words_de = set(stopwords.words("german"))
# Stop words in English EN
stop_words_en = set(stopwords.words("english"))


def detect_language(text: str) -> str:
    """
    Detect the language of a given text

    Args:
        text (str): The text to analyze

    Returns:
        str: The detected language code - 'de' for German and 'en' for
        English
    """
    try:
        language_code = detect(text)
    except TypeError as e:
        print(f"Type error has occurred {e}")
    finally:
        return language_code


def split_list_by_size(lst: List, chunk_size: int = 500) -> List[List[str]]:
    """
    Split a list into multiple parts based on the given chunk size.

    Args:
        lst (list): The input list.
        chunk_size (int): The maximum number of items in each part.

    Returns:
        list: A list of lists, each representing a part of the split list.
    """
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def translate_text_in_list_by_500_to_en(text_list: List[str]) -> List[List[str]]:
    """_summary_

    Args:
        text_list (List[str]): _description_

    Returns:
        List[List[str]]: _description_
    """
    # Detect Language
    # lang = detect_language(lst)
    chunked_text_list = split_list_by_size(text_list)
    translated_text = []
    for chunks in chunked_text_list:
        translated_text += [
            GoogleTranslator(source="auto", target="en").translate(word)
            for word in chunks
        ]
    return translated_text


def translate_text_in_list_by_500_to_de(text_list: List[str]) -> List[List[str]]:
    """_summary_

    Args:
        text_list (List[str]): _description_

    Returns:
        List[List[str]]: _description_
    """
    # Detect Language
    # lang = detect_language(lst)
    chunked_text_list = split_list_by_size(text_list)
    translated_text = []
    for chunks in chunked_text_list:
        translated_text += [
            GoogleTranslator(source="auto", target="des").translate(word)
            for word in chunks
        ]
    return translated_text


def translate_text_to_text(text: str) -> str:
    """_summary_
    Translate whole passages of text from DE to EN or vice versa

    Args:
        text (str): Given text to translate

    Returns:
        str: Return text translated in str
    """
    lang = detect_language(text)
    translation = []
    for i in range(0, len(text), 5000):
        if "de" in lang:
            translated_text = GoogleTranslator(source="auto", target="en").translate(
                text[i : 4999 + i]
            )
        if "en" in lang:
            translated_text = GoogleTranslator(source="auto", target="de").translate(
                text[i : 4999 + i]
            )
        else:
            pass

    return translated_text


def tokenize_text_by_word(content: str, filter_stop_words: bool = True) -> List[str]:
    """_summary_
    Tokenize a passage of text to get back a list of words. Then filter
    out stopwords by its language

    Args:
        text (str): Text to be tokenized
        filter_stop_words (bool, optional): filter stop words.
          Defaults to True.

    Returns:
        List[str]: List of tokenized words in a list
    """
    text = re.sub(r"[()\[\]{}.,;!?<>%]", "", content)

    tokenized_text = word_tokenize(text)

    # Switch for filtering stop words
    if filter_stop_words:
        lang = detect_language(text)
        if "de" in lang:
            filtered_text = [
                token
                for token in tokenized_text
                if token.casefold() not in stop_words_de
            ]
        if "en" in lang:
            filtered_text = [
                token
                for token in tokenized_text
                if token.casefold() not in stop_words_en
            ]
        else:
            pass

    return filtered_text


def find_lemmas_or_stems(text: List[str]) -> Tuple[List[str], List[str]]:
    # Initialize
    stemmer = SnowballStemmer("german")
    lemmatizer = WordNetLemmatizer()

    print(text)

    lemmatized_text = [lemmatizer.lemmatize(text) for i in text]

    stemmed_text = [stemmer.stem(word) for word in text]

    return lemmatized_text, stemmed_text


def filter_pipeline(
    text: str, lemmatize: bool = False, stemize: bool = False
) -> List[str]:
    """_summary_

    Args:
        text (str): _description_
        lemmatize (bool, optional): _description_. Defaults to False.
        stem (bool, optional): _description_. Defaults to False.

    Returns:
        List[str]: _description_
    """
    # Translate Text
    translation = translate_text_to_text(text)

    # Tokenize Text
    # Original
    tokens = tokenize_text_by_word(text)
    # Translation
    tokens_t = tokenize_text_by_word(translation)

    if lemmatize or stemize:
        # Get Lemmas
        # Original
        lemma, stem = find_lemmas_or_stems(tokens)
        lemma_t, stem_t = find_lemmas_or_stems(tokens_t)

        # Append together lists
        combined_list = tokens + lemma + stem + tokens_t + lemma_t + stem_t

        return combined_list
    else:
        return tokens + tokens_t
