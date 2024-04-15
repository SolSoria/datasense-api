from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Descargar los recursos necesarios de NLTK
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def preprocess_text(content):
    """
    Preprocess the text content, tokenizing it and removing stopwords
    """
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(content)
    filtered_tokens = [token.lower() for token in tokens if token.lower() not in stop_words and token.isalpha()]
    return " ".join(filtered_tokens)