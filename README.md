# Pinterest_Pipeline
A clone of the pipeline used at pinterest. Utilising tools such as APIs, Kafka, Apache Spark, Apache Airflow

Developed an end-to-end data processing pipeline in Python based on Pinterests experiment processing pipeline. 
Implemented based on Lambda architecture to take advantage of both batch and stream-processing.
Created an API and used Kafka to distribute the data between S3 for batch processing and Spark streaming for stream-processing.
Stream processing data was processed using Spark Streaming and saved to a PostgresSQL database for real-time analysis and monitoring. 
Batch data was extracted from S3 and transformed in Spark using Airflow to orchestrate the transformations.

