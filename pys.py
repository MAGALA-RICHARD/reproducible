from pyspark.sql import SparkSession

# Initialize Spark
spark = SparkSession.builder.appName("APSIM Parallel Simulations").master("local[*]").getOrCreate()

sc = spark.sparkContext

# Example list of APSIM configurations (paths, management sets, etc.)
apsim_configs = [
    {"id": 1, "rotation": "CS", "fert": 150, "cover": "rye"},
    {"id": 2, "rotation": "CC", "fert": 200, "cover": "none"},
    # ...
]


def run_apsim(config):
    from apsimNGpy.core.runner import run_model_externally  # example
    return 0


# Parallelize the list and run across workers
rdd = sc.parallelize(apsim_configs)
results = rdd.map(run_apsim).collect()

# Convert to Spark DataFrame for easy aggregation
df = spark.createDataFrame(results)
df.show()
