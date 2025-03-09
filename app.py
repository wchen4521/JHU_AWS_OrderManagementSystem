import boto3
import psycopg2
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# AWS Configuration
AWS_REGION = "us-east-1"
SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/692859919740/OrderQueue"
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:692859919740:OrderNotification"
RDS_HOST = "mydb.cr8gyec4g2bj.us-east-1.rds.amazonaws.com"
RDS_USER = "admindb"
RDS_PASSWORD = "Angel2159!"
RDS_DB = "mydb"

# Initialize AWS clients
sqs = boto3.client("sqs", region_name=AWS_REGION)
sns = boto3.client("sns", region_name=AWS_REGION)

# Database connection function
def connect_db():
    return psycopg2.connect(
        host=RDS_HOST, database=RDS_DB, user=RDS_USER, password=RDS_PASSWORD
    )

@app.route("/order", methods=["POST"])
def place_order():
    data = request.get_json()
    order_id = data.get("order_id")
    product_name = data.get("product_name")
    customer_email = data.get("customer_email")
    
    if not all([order_id, product_name, customer_email]):
        return jsonify({"error": "Missing fields"}), 400
    
    order_data = json.dumps(data)
    
    # Send order to SQS
    sqs.send_message(QueueUrl=SQS_QUEUE_URL, MessageBody=order_data)
    return jsonify({"message": "Order placed successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

