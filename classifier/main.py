from google.cloud import pubsub_v1
from classification_service import get_classification_vector
from logger import create_file_logs
import os
import json

project_id = os.environ.get('PROJECT_ID') # 'dev-gd-classifier-v1'
subscription_id = os.environ.get('SUBSCRIPTION_ID') # 'files-to-classify-sub'
credentials_file_path = os.environ.get('CREDENTIALS_FILE_PATH') # 'cloud_storage/credentials.json'
credentials_path = os.path.join(os.path.dirname(__file__), credentials_file_path)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

def main():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    pass

    def callback(message):
        data = json.loads(message.data.decode('utf-8'))
        print("\nReceived message: \n")
        user_id = data.get('user_id')
        vector = data.get('vector')
        classification_vector = get_classification_vector(vector, user_id)
        print(f"Classification vector: {classification_vector}")
        result = create_file_logs(data, classification_vector[0])
        if(result):
            print(f"File {data.get('doc_id')} was classified successfully")
        # message.ack()

    future = subscriber.subscribe(subscription_path, callback)
    print("Listening for messages".format(subscription_path))
        
    with subscriber as subscriber:
        try:
            future.result()
        except TimeoutError:
            future.cancel()
            print(f"TimeoutError: {future.exception()}")

if __name__ == '__main__':
    main()