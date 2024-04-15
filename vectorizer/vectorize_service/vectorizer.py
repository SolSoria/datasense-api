from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pickle
import numpy as np

class Vectorizer:
    def __init__(self, vectorizer, vocabulary_file):
        """
        Initialize the vectorizer with a vectorizer and the vocabulary loaded from a .pkl file.
        """
        self.vocabulary_file = vocabulary_file
        self.vocabulary = self._load_vocabulary()
        self.vectorizer = vectorizer()
        self.fit()

    def _load_vocabulary(self):
        """
        Load the vocabulary from the .pkl file.
        """
        with open(self.vocabulary_file, 'rb') as f:
            vocabulary = pickle.load(f)
        return vocabulary

    def fit(self):
        """
        Fit the vectorizer with the vocabulary.
        """
        self.vectorizer.fit(self.vocabulary)
        
    def get_vector(self, document):
        """
        Get the vectorized representation of the document.
        """
        vectorized = self.vectorizer.transform([document])
        return vectorized

    def get_top_terms(self, document, num_words=10):
        top_terms = []
        if isinstance(self.vectorizer, CountVectorizer):
            counts = np.squeeze(np.asarray(self.vectorizer.transform([document]).todense()))
            sorted_indices = np.argsort(counts)[::-1]
            sorted_indices = [idx for idx in sorted_indices if counts[idx] != 0][:num_words]
            top_terms = [(term, counts[idx]) for term, idx in self.vectorizer.vocabulary_.items() if idx in sorted_indices]
        elif isinstance(self.vectorizer, TfidfVectorizer):
            tfidf_values = self.vectorizer.transform([document]).toarray()[0]
            sorted_indices = np.argsort(tfidf_values)[::-1]
            sorted_indices = [idx for idx in sorted_indices if tfidf_values[idx] != 0][:num_words]
            top_terms = [(term, tfidf_values[idx]) for term, idx in self.vectorizer.vocabulary_.items() if idx in sorted_indices]
        else:
            raise ValueError("Vectorizer type not supported")
        return top_terms