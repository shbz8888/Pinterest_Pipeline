# Pinterest_Pipeline
A clone of the pipeline used at pinterest. Utilising tools such as APIs, Kafka, Apache Spark, Apache Airflow

Developed an end-to-end data processing pipeline in Python based on Pinterests experiment processing pipeline. 
Implemented based on Lambda architecture to take advantage of both batch and stream-processing.
Created an API and used Kafka to distribute the data between S3 for batch processing and Spark streaming for stream-processing.
Stream processing data was processed using Spark Streaming and saved to a PostgresSQL database for real-time analysis and monitoring. 
Batch data was extracted from S3 and transformed in Spark using Airflow to orchestrate the transformations.

**Navigation**:

**Project_pin_API**: An API that Receives requests from a user emulation script - with an integrated Kafka producer that sends data to a Kafka topic

**batch_consumer**: Consumes data from the Kafka topic and sends it to AWS S3

**Spark_job**: Reads data from S3 bucket and applies transformations cleaning it, replacing missing values and calculating features

**streaming_consumer**: Subscribes to a Kafka topic, cleans data, displays real-time features, sends cleaned structured data to a PostgreSQL database for post-processing
