import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from app.utils.text_processor import clean_text, get_sentence_scores

nltk.download('punkt')
nltk.download('stopwords')

def generate_summary(text, ratio=0.3):
    sentences = sent_tokenize(text)
    if len(sentences) <= 2:
        return text
        
    sentence_scores = get_sentence_scores(text)
    num_sentences = max(2, int(len(sentences) * ratio))
    
    # Get important sentences while maintaining context
    top_sentences = sorted(
        [(score, idx) for idx, score in sentence_scores.items()],
        reverse=True
    )[:num_sentences]
    
    # Include first and last sentences if not already included
    selected_indices = {idx for _, idx in top_sentences}
    if 0 not in selected_indices and len(sentences) > 0:
        selected_indices.add(0)
    if len(sentences)-1 not in selected_indices and len(sentences) > 1:
        selected_indices.add(len(sentences)-1)
        
    # Return sentences in original order
    summary = " ".join(sentences[i] for i in sorted(selected_indices))
    return summary