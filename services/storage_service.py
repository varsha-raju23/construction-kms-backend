from azure.storage.blob import BlobServiceClient
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os

load_dotenv()

CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")

blob_service_client = BlobServiceClient.from_connection_string(
    CONNECTION_STRING
)

def upload_file(file):
    filename = secure_filename(file.filename)

    blob_client = blob_service_client.get_blob_client(
        container=CONTAINER_NAME,
        blob=f"uploads/{filename}"
    )

    blob_client.upload_blob(file, overwrite=True)

    return {
        "file_name": filename,
        "file_url": blob_client.url
    }

def delete_file(file_name):
    blob_client = blob_service_client.get_blob_client(
        container=CONTAINER_NAME,
        blob=f"uploads/{file_name}"
    )

    blob_client.delete_blob()

    return True