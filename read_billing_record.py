import logging
import azure.functions as func
import os
import json
from azure.cosmos import CosmosClient, exceptions
from azure.storage.blob import BlobServiceClient

COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
DATABASE_NAME = os.getenv("COSMOS_DATABASE")
CONTAINER_NAME = os.getenv("COSMOS_CONTAINER")

BLOB_CONN_STR = os.getenv("BLOB_CONN_STR")
ARCHIVE_CONTAINER = os.getenv("BLOB_CONTAINER", "billing-archive")

cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
container = cosmos_client.get_database_client(DATABASE_NAME).get_container_client(CONTAINER_NAME)

blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
blob_container_client = blob_service_client.get_container_client(ARCHIVE_CONTAINER)

def get_from_cosmos(record_id):
    try:
        response = container.read_item(item=record_id, partition_key=record_id)
        return response
    except exceptions.CosmosResourceNotFoundError:
        return None

def get_from_blob(record_id):
    try:
        blob_path = f"{record_id}.json"
        blob_client = blob_container_client.get_blob_client(blob_path)
        blob_data = blob_client.download_blob().readall()
        return json.loads(blob_data)
    except Exception as e:
        logging.error(f"Blob read failed: {e}")
        return None

def main(req: func.HttpRequest) -> func.HttpResponse:
    record_id = req.route_params.get('record_id')

    if not record_id:
        return func.HttpResponse("Missing record_id", status_code=400)

    record = get_from_cosmos(record_id)
    if record:
        return func.HttpResponse(json.dumps(record), status_code=200, mimetype="application/json")

    record = get_from_blob(record_id)
    if record:
        return func.HttpResponse(json.dumps(record), status_code=200, mimetype="application/json")

    return func.HttpResponse("Record not found", status_code=404)
