# backend_functions.py

import requests
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForSequenceClassification
import torch
import re

def getReviews(url):
    """
    Scrape reviews from the given URL using BeautifulSoup.
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    regex = re.compile('.*comment.*')
    results = soup.find_all('p', {'class': regex})
    reviews = [result.text for result in results]
    return reviews

def getVerdict(reviews):
    """
    Generate a verdict using a fine-tuned T5 transformer model.
    """
    # Load fine-tuned T5 transformer model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained("t5-small")
    model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
    
    # Preprocess input
    inputs = ["summarize: " + review for review in reviews]
    tokenized_inputs = tokenizer(inputs, max_length=1024, padding=True, truncation=True, return_tensors="pt")
    
    # Generate verdicts
    with torch.no_grad():
        outputs = model.generate(tokenized_inputs['input_ids'], max_length=128, num_beams=2, early_stopping=True)
    
    # Decode generated summaries
    decoded_verdicts = tokenizer.batch_decode(outputs, skip_special_tokens=True)

    concatenated_verdicts = ". ".join(decoded_verdicts)
    
    return concatenated_verdicts

def getRating(reviews):
    """
    Rate the product using a BERT sentiment analysis model.
    """
    # Load BERT model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

    # Tokenize input
    tokens = tokenizer(reviews, return_tensors='pt', truncation=True, padding=True)

    # Perform sentiment analysis
    with torch.no_grad():
        result = model(**tokens)

    # Convert sentiment scores to ratings
    ratings = [int(torch.argmax(score).item()) + 1 for score in result.logits]

    overall_rating = sum(ratings) / len(ratings) if ratings else 0
    return overall_rating
