from kafka import KafkaConsumer
import json
from json import loads
import boto3
import tempfile
s3_client = boto3.client('s3')
s3 = boto3.resource('s3')

# create our consumer to retrieve the message from the topics
data_stream_consumer = KafkaConsumer(
    bootstrap_servers="localhost:9092",    
    value_deserializer=lambda message: loads(message),
    auto_offset_reset="earliest" # This value ensures the messages are read from the beginning 
)

data_stream_consumer.subscribe(topics=["MyFirstKafkaTopic"])
for msg in data_stream_consumer:
    
    if isinstance(msg.value,dict):

        gamma_dict = msg.value
        print(gamma_dict['unique_id'])
    
        file = json.dumps(msg.value)
        s3_client.put_object(
        Body=file,
        Bucket='pinterestdata7b8c2d40-08c6-4eb4-8c96-2f0080c4653b',
        Key= msg.value['unique_id'] + ".json"
        )