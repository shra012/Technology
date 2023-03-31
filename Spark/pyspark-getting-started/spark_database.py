from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext

if __name__ == "__main__":
    spark = SparkSession.builder.appName("Python MySQL reader").config("spark.driver.extraClassPath", "/usr/share/java/mysql-connector-j-8.0.31.jar").getOrCreate()
    jdbcDF = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:mysql://127.0.0.1:3306/rundeck") \
        .option("dbtable", "storage") \
        .option("user", "rundeck") \
        .option("password", "rundeck") \
        .option("driver", 'com.mysql.cj.jdbc.Driver') \
        .load()
    print(jdbcDF.first())