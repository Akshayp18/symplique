# Durable Function: Archive Old Billing Records

import datetime
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient
import json
import logging
import os

# Cosmos DB configuration
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
DATABASE_NAME = os.getenv("COSMOS_DATABASE")
CONTAINER_NAME = os.getenv("COSMOS_CONTAINER")

# Blob Storage configuration
BLOB_CONN_STR = os.getenv("BLOB_CONN_STR")
BLOB_CONTAINER = os.getenv("BLOB_CONTAINER", "billing-archive")

# Clients
cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
db = cosmos_client.get_database_client(DATABASE_NAME)
container = db.get_container_client(CONTAINER_NAME)
blob_service = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
blob_container = blob_service.get_container_client(BLOB_CONTAINER)

def main(mytimer: func.TimerRequest) -> None:
    logging.info("Starting billing archive function.")
    cutoff_date = (datetime.datetime.utcnow() - datetime.timedelta(days=90)).isoformat()

    query = f"SELECT * FROM c WHERE c.timestamp < '{cutoff_date}'"
    old_records = container.query_items(query, enable_cross_partition_query=True)

    for record in old_records:
        record_id = record['id']
        partition_key = record.get('partitionKey', record_id)
        date_str = record['timestamp'][:10]  # e.g., '2025-04-05'
        blob_name = f"{date_str}/{record_id}.json"

        try:
            blob_container.upload_blob(name=blob_name, data=json.dumps(record), overwrite=True)
            container.delete_item(item=record_id, partition_key=partition_key)
            logging.info(f"Archived and deleted record ID: {record_id}")
        except Exception as e:
            logging.error(f"Failed to archive record ID: {record_id} - {str(e)}")

    logging.info("Billing archive function completed.")
