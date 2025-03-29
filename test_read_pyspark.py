from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, FloatType, LongType

def write_row(batch_df , batch_id):
    batch_df.write.format("mongodb").mode("append").save()
    pass
# 2. Create Spark session
spark = SparkSession.builder \
    .appName("KafkaJSONToConsole") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1,org.mongodb.spark:mongo-spark-connector_2.12:10.4.1") \
    .config("spark.mongodb.read.connection.uri", "mongodb+srv://") \
    .config("spark.mongodb.read.database", "tenant") \
    .config("spark.mongodb.read.collection", "list_tenant") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
spark.read \
  .format("mongodb") \
  .option("uri", "mongodb+srv:///") \
  .option("database", "tenant") \
  .option("collection", "list_tenant") \
  .load() \
  .show()

spark.stop()