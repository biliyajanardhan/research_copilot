import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

class BlobStorageService:
    def __init__(self):
        self.client = BlobServiceClient.from_connection_string(
            os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        )
        self.container_name = "research-papers"

    def upload_pdf(self, file_path, blob_name):
        blob_client = self.client.get_blob_client(
            container=self.container_name,
            blob=blob_name
        )

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        return blob_client.url
