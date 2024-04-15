from cloud_storage import CloudStorage
import os
import joblib
import numpy as np

def download_model(user_id):
    try:
        cloud_storage = CloudStorage('data_sense_dev')
        # If the folder does not exist, create it
        folder_path = 'downloads'
        os.makedirs(folder_path, exist_ok=True)
        # Download the Naive Bayes model
        file_path = f'users/{user_id}/models/NB_model.pkl'
        cloud_storage.download_file(file_path, os.path.join(folder_path, 'NB_model.pkl'))
    except Exception as e:
        print(f'Error: {e}')
        return

def get_classification_vector(vector, user_id):
    try:
        download_model(user_id)
        model_path = 'downloads/NB_model.pkl'
        nb_model = joblib.load(model_path)
        tfidf_vector = np.array(vector)
        pred_vector = nb_model.predict_proba(tfidf_vector)
        return pred_vector
    except Exception as e:
        print(f'Error: {e}')
        return None