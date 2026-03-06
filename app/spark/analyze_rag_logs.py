from pyspark.sql import SparkSession
from pyspark.sql.functions import col, length, avg

spark = SparkSession.builder \
    .appName("RAG Logs Analysis") \
    .getOrCreate()

df = spark.read.json("../backend/rag_logs.json")

print("Schema:")
df.printSchema()

print("Total queries:")
print(df.count())

df = df.withColumn("answer_length", length(col("answer")))

print("Average answer length:")
df.select(avg("answer_length")).show()

empty_answers = df.filter(col("answer_length") < 5)

print("Possible hallucinations / empty answers:")
empty_answers.show()

df.groupBy("question").count().orderBy(col("count").desc()).show(10)

spark.stop()