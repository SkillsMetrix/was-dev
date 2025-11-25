
"""
https://chatgpt.com/c/6925bb4f-c2d8-8320-b833-1f8beb249da9

Lambda: triggered by S3 'ObjectCreated' event for CSV files.
Parses CSV and writes rows to DynamoDB (table: CsvImportedTable).
"""

import os
import csv
import io
import uuid
import boto3
from datetime import datetime
from botocore.exceptions import ClientError

REGION = os.getenv("AWS_REGION", "us-east-1")
DDB_TABLE = os.getenv("DDB_TABLE", "CsvImportedTable")

s3 = boto3.client("s3", region_name=REGION)
dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(DDB_TABLE)

def lambda_handler(event, context):
    """
    Expected event: S3 put event (ObjectCreated).
    """
    records = event.get("Records", [])
    results = {"processed": 0, "errors": []}

    for rec in records:
        try:
            bucket = rec["s3"]["bucket"]["name"]
            key = rec["s3"]["object"]["key"]
        except KeyError:
            results["errors"].append({"error": "Invalid S3 event record", "record": rec})
            continue

        try:
            resp = s3.get_object(Bucket=bucket, Key=key)
            content = resp["Body"].read().decode("utf-8")
        except ClientError as e:
            results["errors"].append({"error": "S3 get_object failed", "detail": str(e), "bucket": bucket, "key": key})
            continue

        # Read CSV from string
        csv_file = io.StringIO(content)
        reader = csv.DictReader(csv_file)

        # Validate header exists
        if reader.fieldnames is None:
            results["errors"].append({"error": "CSV has no header", "bucket": bucket, "key": key})
            continue

        # Batch write to dynamodb
        try:
            with table.batch_writer() as batch:
                for row in reader:
                    # normalize row: strip whitespace
                    row = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}

                    # ensure id exists (primary key)
                    item_id = row.get("id") or str(uuid.uuid4())

                    # add metadata fields
                    now_iso = datetime.utcnow().isoformat() + "Z"
                    item = {
                        "id": item_id,
                        "created_at": now_iso,
                        # store all CSV columns as top-level attributes (avoid empty strings if you prefer)
                        **{k: v for k, v in row.items() if v is not None and v != ""},
                    }

                    # Put item (batch_writer handles buffering / retries)
                    batch.put_item(Item=item)
                    results["processed"] += 1

        except ClientError as e:
            results["errors"].append({"error": "DynamoDB write failed", "detail": str(e)})

    return {
        "statusCode": 200,
        "body": results
    }
