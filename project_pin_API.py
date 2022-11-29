from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from json import dumps
from kafka import KafkaProducer
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.cluster import ClusterMetadata
import boto3
from kafka import KafkaConsumer
import json
from json import loads

app = FastAPI()

# Create a new Kafka client to adminstrate our Kafka broker
admin_client = KafkaAdminClient(
    bootstrap_servers="localhost:9092", 
    client_id="Kafka Administrator"
)



class Data(BaseModel):
    category: str
    index: int
    unique_id: str
    title: str
    description: str
    follower_count: str
    tag_list: str
    is_image_or_video: str
    image_src: str
    downloaded: int
    save_location: str


@app.post("/pin/")
def get_db_row(item: Data):
    data = dict(item)
    # PRODUCER
    gamma_producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    client_id="12/10 producer",
    value_serializer=lambda data: dumps(data).encode("ascii")
    ) 
    gamma_producer.send(topic="MyFirstKafkaTopic", value=data)

   
    



    return item,data


if __name__ == '__main__':
    uvicorn.run("project_pin_API:app", host="localhost", port=8000)
