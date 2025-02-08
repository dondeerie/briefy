from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import re

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s.]', '', text)
    return text

def get_sentence_scores(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    
    # Enhanced scoring
    stop_words = set(stopwords.words('english'))
    word_freq = FreqDist([w for w in words if w not in stop_words and w.isalnum()])
    
    # Score with position weight
    sentence_scores = {}
    total_sentences = len(sentences)
    
    for idx, sentence in enumerate(sentences):
        words = word_tokenize(sentence.lower())
        score = 0
        
        for word in words:
            if word in word_freq:
                score += word_freq[word]
        
        # Position bias
        position_weight = 1.0
        if idx == 0 or idx == total_sentences - 1:
            position_weight = 1.2
            
        sentence_scores[idx] = (score / max(len(words), 1)) * position_weight
        
    return sentence_scores