import boto3
import psycopg2
import json
import time

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

# Save order to database
def save_to_db(order_data):
    conn = connect_db()
    if conn is None:
        logging.error("Database connection not available. Skipping order processing.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO orders (order_id, product_name, customer_email)
            VALUES (%s, %s, %s)
            ON CONFLICT (order_id) DO NOTHING;
            """,
            (order_data["order_id"], order_data["product_name"], order_data["customer_email"])
        )
        conn.commit()
        cursor.close()
        conn.close()
        logging.info(f"Order {order_data['order_id']} saved to database.")
    except Exception as e:
        logging.error(f"Failed to save order {order_data['order_id']} to database: {str(e)}")


# Send SNS notification
def send_notification(order_data):
    message = f"Order {order_data['order_id']} for {order_data['product_name']} has been placed."
    sns.publish(TopicArn=SNS_TOPIC_ARN, Message=message, Subject="Order Confirmation")

# Worker to process orders
def process_orders():
    while True:
        response = sqs.receive_message(QueueUrl=SQS_QUEUE_URL, MaxNumberOfMessages=1, WaitTimeSeconds=10)
        if "Messages" in response:
            for message in response["Messages"]:
                order_data = json.loads(message["Body"])
                save_to_db(order_data)
                send_notification(order_data)
                sqs.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=message["ReceiptHandle"])

if __name__ == "__main__":
    process_orders()
