from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, FloatType, LongType

def write_row(batch_df , batch_id):
    batch_df.write.format("mongodb").mode("append").save()
    pass

# 1. Define your schema
review_schema = StructType() \
    .add("tenant_id", StringType()) \
    .add("marketplace", StringType())\
    .add("customer_id", LongType()) \
    .add("review_id", StringType()) \
    .add("product_id", StringType()) \
    .add("product_parent", LongType()) \
    .add("product_title", StringType()) \
    .add("product_category", StringType()) \
    .add("star_rating", FloatType()) \
    .add("helpful_votes", FloatType()) \
    .add("total_votes", FloatType()) \
    .add("vine", StringType()) \
    .add("verified_purchase", StringType()) \
    .add("review_headline", StringType()) \
    .add("review_body", StringType()) \
    .add("review_date", StringType()) \

# 2. Create Spark session
spark = SparkSession.builder \
    .appName("KafkaJSONToConsole") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1,org.mongodb.spark:mongo-spark-connector_2.12:10.1.1") \
    .config("spark.mongodb.read.connection.uri", "mongodb+srv:///") \
    .config("spark.mongodb.write.connection.uri", "mongodb+srv:///") \
    .config("spark.mongodb.write.database", "test_streaming") \
    .config("spark.mongodb.write.collection", "test") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
spark.conf.set("spark.sql.adaptive.enabled", "false")
spark.conf.set("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true")

kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "test") \
    .option("startingOffsets", "latest") \
    .load()
    
kafka_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
kafka_df.writeStream.foreachBatch(write_row).start().awaitTermination()