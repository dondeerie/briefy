import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from app.utils.text_processor import clean_text, get_sentence_scores

nltk.download('punkt')
nltk.download('stopwords')

def generate_summary(text, ratio=0.3):
    # Clean and prepare text
    cleaned_text = clean_text(text)
    sentences = sent_tokenize(cleaned_text)
    
    if not sentences:
        return ""
    
    # Get sentence scores
    sentence_scores = get_sentence_scores(cleaned_text)
    
    # Select top sentences
    num_sentences = max(1, int(len(sentences) * ratio))
    top_sentences = sorted(
        [(score, idx) for idx, score in sentence_scores.items()],
        reverse=True
    )[:num_sentences]
    
    # Reconstruct summary maintaining original order
    summary_sentences = [sentences[idx] for _, idx in sorted(top_sentences)]
    
    return " ".join(summary_sentences)