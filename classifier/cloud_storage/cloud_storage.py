from google.cloud import storage

class CloudStorage():
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = storage.Client()

    def upload_file(self, file_path):
        try:
            bucket = self.client.get_bucket(self.bucket_name)
            blob = bucket.blob(file_path)
            blob.upload_from_filename(file_path)
        except Exception as e:
            print(f'Error: {e}')
            return

    def download_file(self, blob_name, file_path):
        try: 
            bucket = self.client.get_bucket(self.bucket_name)
            blob = bucket.blob(blob_name)
            blob.download_to_filename(file_path)
        except Exception as e:
            print(f'Error: {e}')
            return