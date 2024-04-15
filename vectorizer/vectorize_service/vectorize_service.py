from cloud_storage import CloudStorage
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from .vectorizer import Vectorizer
import os
import sys

def download_vocabularies(bucket_name, user_id):
    try:
        cloud_storage = CloudStorage(bucket_name)
        file_path = f'users/{user_id}/vocabularies/tfidf.pkl'
        # Construir la ruta de la carpeta
        folder_path = 'downloads'
        # Crear la carpeta si no existe
        os.makedirs(folder_path, exist_ok=True)
        # Descargar el archivo tfidf.pkl
        file_path = f'users/{user_id}/vocabularies/tfidf.pkl'
        cloud_storage.download_file(file_path, os.path.join(folder_path, 'tfidf.pkl'))
        # Descargar el archivo count_vectorizer.pkl
        file_path = f'users/{user_id}/vocabularies/count_vectorizer.pkl'
        cloud_storage.download_file(file_path, os.path.join(folder_path, 'count_vectorizer.pkl'))

    except Exception as e:
        print(f'Error: {e}')
        return

def get_content_vectors(content, user_id):
    try:
        download_vocabularies('data_sense_dev', user_id)
        count_vectorizer = Vectorizer(CountVectorizer, 'downloads/count_vectorizer.pkl')
        tfidf_vectorizer = Vectorizer(TfidfVectorizer, 'downloads/tfidf.pkl')
        tfidf_vector = tfidf_vectorizer.get_vector(content)
        top_word_tfidf = tfidf_vectorizer.get_top_terms(content)
        top_word_count = count_vectorizer.get_top_terms(content)
        return tfidf_vector, top_word_count, top_word_tfidf

    except Exception as e:
        print(f'Error: {e}')
        sys.stdout.flush()
        return None, None, None
    return True