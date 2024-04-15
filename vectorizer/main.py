from flask import Flask, request, jsonify
from vectorize_service import get_content_vectors
from preprocess_text import preprocess_text
import http
import os

credentials_file_path = os.environ.get('CREDENTIALS_FILE_PATH') # 'cloud_storage/credentials.json'
credentials_path = os.path.join(os.path.dirname(__file__), credentials_file_path)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

server = Flask(__name__)
# Routes 
@server.route('/health', methods=['GET'])
def health_check():
    return 'OK', http.HTTPStatus.OK
    
@server.route('/vectorize', methods=['POST'])
def vectorize():
    content = request.json.get('content')
    user_id = request.json.get('user_id')
    if not content:
        return 'No content provided', http.HTTPStatus.BAD_REQUEST
    if not user_id:
        return 'No user id provided', http.HTTPStatus.BAD_REQUEST

    preprocessed_content = preprocess_text(content)
    tfidf_vector, top_word_count, top_word_tfidf = get_content_vectors(preprocessed_content, user_id)
    response = {
        "tfidf_vector": tfidf_vector.toarray().tolist(),
        "top": {
            "tfidf": [{"word": word, "value": float(value)} for word, value in top_word_tfidf],
            "count": [{"word": word, "value": int(value)} for word, value in top_word_count]
        }
    }

    return jsonify(response), http.HTTPStatus.OK

if __name__ == '__main__':
    server.run(host='0.0.0.0')