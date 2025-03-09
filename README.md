Order Management System on AWS
===================================

Project Overview:
-----------------
This project is an **Order Management System** built using AWS services such as:
- **Amazon SQS** (for queuing order messages)
- **Amazon SNS** (for sending notifications)
- **Amazon RDS (PostgreSQL)** (for storing order details)
- **EC2** (for running the worker process)

The system processes orders by:
1. Receiving messages from an SQS queue.
2. Storing the order details in an RDS PostgreSQL database.
3. Sending a confirmation notification via SNS.

Project Components:
-------------------
1. **worker.py** – The main script that:
   - Listens for messages in the SQS queue.
   - Saves valid orders into the PostgreSQL database.
   - Sends an SNS notification upon successful order placement.

2. **AWS Services Used**:
   - **Amazon SQS**: Stores incoming order requests.
   - **Amazon SNS**: Sends notifications upon successful order processing.
   - **Amazon RDS**: PostgreSQL database to store orders.
   - **Amazon EC2**: Hosts the worker process.

Installation & Setup:
---------------------
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/JH-605-702/project1-wchen4521.git
   cd project1-wchen4521
   
Install Dependencies:
---------------------
pip install boto3 psycopg2


Environment Configuration:
---------------------
Update worker.py with your AWS credentials, database details, and queue/topic ARNs.


Run the Worker:
---------------------
python3 worker.py


Testing:
---------------------
Check if the Worker is Running:
ps aux | grep worker.py


Manually Send a Test Message to SQS:
---------------------
aws sqs send-message --queue-url https://sqs.us-east-1.amazonaws.com/692859919740/OrderQueue \
    --message-body '{"order_id": 999, "product_name": "Test Item", "customer_email": "test@example.com"}'
    
    
Verify the Database:
---------------------
psql -h mydb.cr8gyec4g2bj.us-east-1.rds.amazonaws.com -U admindb -d mydb -c "SELECT * FROM orders;"


Check SNS Notification:
---------------------
Ensure the recipient email is subscribed to the SNS topic.
Check your inbox for an order confirmation.


Troubleshooting:
---------------------
If SQS messages are not processed, restart the worker:

pkill -f worker.py
python3 worker.py

---------------------
If unable to connect to RDS, check security group rules:
	Ensure EC2 can access the RDS database on port 5432.
If SNS notifications are not received:
	Confirm that the email subscription to the SNS topic is confirmed.


Author: Chen (Anson) Wang
Course: EN.605.702.8VL.SP25 Cloud-native Architecture and Microservices




