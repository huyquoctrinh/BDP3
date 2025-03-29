from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, FloatType, LongType

# 1. Define your schema
review_schema = StructType() \
    .add("tenant_id", StringType()) \
    .add("review", StructType()
        .add("marketplace", StringType())
        .add("customer_id", LongType())
        .add("review_id", StringType())
        .add("product_id", StringType())
        .add("product_parent", LongType())
        .add("product_title", StringType())
        .add("product_category", StringType())
        .add("star_rating", FloatType())
        .add("helpful_votes", FloatType())
        .add("total_votes", FloatType())
        .add("vine", StringType())
        .add("verified_purchase", StringType())
        .add("review_headline", StringType())
        .add("review_body", StringType())
        .add("review_date", StringType())
    )

# 2. Create Spark session
spark = SparkSession.builder \
    .appName("KafkaJSONToConsole") \
    .config("spark.jars.packages", 
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# 3. Read from Kafka topic
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "test") \
    .option("startingOffsets", "latest") \
    .load()

parsed_df = kafka_df.selectExpr("CAST(value AS STRING) as json_string") \
    .withColumn("data", from_json(col("json_string"), review_schema)) \
    .select("data.*")
flattened_df = parsed_df.select(
    "tenant_id",
    "review.marketplace",
    "review.customer_id",
    "review.review_id",
    "review.product_id",
    "review.product_parent",
    "review.product_title",
    "review.product_category",
    "review.star_rating",
    "review.helpful_votes",
    "review.total_votes",
    "review.vine",
    "review.verified_purchase",
    "review.review_headline",
    "review.review_body",
    "review.review_date"
)
print(vars(flattened_df))
query = flattened_df.writeStream \
    .format("console") \
    .option("truncate", False) \
    .option("numRows", 10) \
    .outputMode("append") \
    .start()