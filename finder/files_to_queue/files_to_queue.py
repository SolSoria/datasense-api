import os
from google.cloud import pubsub_v1
import json
import time
import sys

credentials_file_path = os.environ.get('CREDENTIALS_FILE_PATH') # 'pubsub/credentials.json'
credentials_path = os.path.join(os.path.dirname(__file__), credentials_file_path) 
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

project_id = os.environ.get('PROJECT_ID') # 'dev-gd-classifier-v1'
topic_id = os.environ.get('FILES_TO_DOWNLOAD_TOPIC_ID') # 'files-to-download'

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def files_to_queue(files, user_id, request_id):
    for file in files:
        message = {
            "doc_id": file.get('id'),
            "user_id": user_id,
            "request_id": request_id,
        }
        message = json.dumps(message).encode('utf-8')
        # time.sleep(5)
        future = publisher.publish(topic_path, data=message)
        try:
            future.result()
        except KeyboardInterrupt:
            future.cancel()

    print(f"Published messages to {topic_path}.")
    sys.stdout.flush()
    return