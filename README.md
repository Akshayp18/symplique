📦 Azure Billing Records Archival – Serverless & Cost-Optimized
---------------------------------------------------------------------
This project provides a complete serverless solution to reduce storage costs in Azure Cosmos DB by archiving billing records older than 3 months to Azure Blob Storage. It uses:

✅ Azure Durable Function (Timer Trigger)

✅ Blob Storage (Cool/Hot tier)

✅ Azure DevOps Pipeline for CI/CD

✅ Optional fallback-read support

🧱 Architecture Overview
------------------------------

                                +------------------------+
                                |     Cosmos DB (Hot)    |
                                |  Billing Records ≤ 90d |
                                +-----------+------------+
                                            |
                                            | (Timer Triggered)
                                            v
+----------------+     Archive to     +-----+---------------+
| Durable Azure  |------------------->| Azure Blob Storage |
|   Function     |    old records     | (billing-archive/) |
+----------------+                   +---------------------+
                                            ^
                                            | (Fallback Read)
                             +--------------+--------------+
                             | Optional Read Proxy Function|
                             +-----------------------------+
🔧 Project Features
--------------------------
🧊 Tiered Storage: Recent data in Cosmos DB, old data in Blob Storage

⏱ Timer-Triggered Archival: Azure Function moves data older than 90 days

📉 Massive Cost Savings: Blob storage is 10x cheaper than Cosmos DB

🔁 Fallback Reads: Serve old data from Blob if not found in DB

🚀 Automated CI/CD: Azure DevOps pipeline deploys the solution seamlessly

📁 Folder Structure
--------------------
/
├── function-app/
│   ├── archive_old_records.py       # Timer function for archival
│   ├── read_billing_record.py       # Optional read proxy
│   ├── function.json                # Trigger binding config
│   └── requirements.txt            # Python dependencies
├── azure-pipelines.yml              # Azure DevOps deployment pipeline
└── README.md                        # Documentation

🚀 How to Deploy via Azure DevOps
-------------------------------------
1. Requirements
Azure Function App (Linux, Python 3.11+)

Azure Blob Storage

Azure Cosmos DB (Core SQL API)

Azure DevOps Project

Azure Resource Manager Service Connection

 Setup Environment Variables in Function App
 ------------------------------------------------
  COSMOS_ENDPOINT	Cosmos DB endpoint
  COSMOS_KEY	Cosmos DB primary key
  COSMOS_DATABASE	Cosmos DB database name
  COSMOS_CONTAINER	Cosmos DB container name
  BLOB_CONN_STR	Blob Storage connection string
  BLOB_CONTAINER	Blob container name (e.g. billing-archive)

4. Run Pipeline
Commit and push your code to main

Navigate to Azure DevOps → Pipelines → New Pipeline

Use existing YAML file

Trigger it

🧪 Testing the System
After deployment, test via Function App log stream

Read Proxy (read_billing_record.py) can be invoked as:
GET /api/billing/{record_id}
Returns from Cosmos DB if available, or falls back to Blob Storage if not.


📈 Monitoring
-------------------
Enable Application Insights in the Function App

Track logs: record archived, record fallback, record not found

Use Log Analytics for alerts on function failures

🔐 Security Note
------------------------
For production, consider:

Using Managed Identity instead of connection strings

Enabling private endpoint access for Blob and Cosmos DB

