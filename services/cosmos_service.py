import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from azure.cosmos import CosmosClient, PartitionKey

load_dotenv()

COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")

DATABASE_NAME = "construction_kms_db"
DOCUMENTS_CONTAINER = "documents"
CHAT_CONTAINER = "chat_history"

client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)

database = client.create_database_if_not_exists(id=DATABASE_NAME)

documents_container = database.create_container_if_not_exists(
    id=DOCUMENTS_CONTAINER,
    partition_key=PartitionKey(path="/category")
)

chat_container = database.create_container_if_not_exists(
    id=CHAT_CONTAINER,
    partition_key=PartitionKey(path="/type")
)


def save_document(data):
    document_id = str(uuid.uuid4())

    data["id"] = document_id
    data["upload_date"] = datetime.utcnow().isoformat()
    data["status"] = "active"

    if not data.get("category"):
        data["category"] = "general"

    documents_container.create_item(body=data)

    return document_id


def get_document(document_id):
    query = "SELECT * FROM c WHERE c.id = @id"

    items = list(documents_container.query_items(
        query=query,
        parameters=[{"name": "@id", "value": document_id}],
        enable_cross_partition_query=True
    ))

    if not items:
        return None

    return items[0]


def search_documents(keyword="", category=""):
    query = "SELECT * FROM c WHERE c.status = 'active'"
    parameters = []

    if category:
        query += " AND c.category = @category"
        parameters.append({"name": "@category", "value": category})

    items = list(documents_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))

    results = []
    keyword_lower = keyword.lower()

    for data in items:
        title = data.get("title", "").lower()
        description = data.get("description", "").lower()
        extracted_text = data.get("extracted_text", "").lower()
        tags = " ".join(data.get("tags", [])).lower()

        if (
            keyword == ""
            or keyword_lower in title
            or keyword_lower in description
            or keyword_lower in extracted_text
            or keyword_lower in tags
        ):
            results.append(data)

    return results


def save_chat(question, answer):
    chat_id = str(uuid.uuid4())

    chat_data = {
        "id": chat_id,
        "type": "chat",
        "question": question,
        "answer": answer,
        "created_at": datetime.utcnow().isoformat()
    }

    chat_container.create_item(body=chat_data)

    return chat_id


def get_chat_history():
    query = "SELECT * FROM c WHERE c.type = 'chat'"

    items = list(chat_container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))

    items.sort(
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )

    return items[:20]


def delete_document(document_id):
    document = get_document(document_id)

    if not document:
        return False

    documents_container.delete_item(
        item=document["id"],
        partition_key=document["category"]
    )

    return True