import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.summarization import summarize

# Pastikan untuk mengunduh stopwords NLTK dan tokenizer
nltk.download('punkt')
nltk.download('stopwords')

def get_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Mengambil semua teks dari tag <p> di dalam halaman HTML
    paragraphs = soup.find_all('p')
    return ' '.join([p.get_text() for p in paragraphs])

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d', ' ', text)
    return text

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    return ' '.join([word for word in words if word.lower() not in stop_words])

def text_rank_summarize(text, ratio=0.2):
    return summarize(text, ratio=ratio)

st.title("Article Summarization App")

# Input URL atau teks
url_input = st.text_input("Enter URL")
text_input = st.text_area("Or enter text to summarize", height=200)

if st.button('Lihat Teks'):
    text = ''
    if url_input:
        # Proses URL
        text = get_text_from_url(url_input)
   
    if text_input:
        # Proses teks langsung
        text = text_input

    if text:
        text = clean_text(text)
        text = remove_stopwords(text)
        st.session_state.text = text
        st.write(st.session_state.text)
    else:
        st.error('Silakan masukkan URL atau masukkan teks langsung')

if st.button('Tampilkan Ringkasan'):
    if 'text' in st.session_state:
        summary = text_rank_summarize(st.session_state.text)
        st.write(summary)
    else:
        st.error('Silakan masukkan teks untuk diringkas.')
