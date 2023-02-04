from kafka import KafkaConsumer
import json
import pydoop.hdfs as hdfs
import subprocess
from pymongo import MongoClient

mongodb_connection_string = "mongodb://127.0.0.1:27017/energy"
client = MongoClient(mongodb_connection_string)
db_mongodb = client.get_database("energy")
print("Base de datos mongo db nombre: {}".format(client.list_database_names()))
collection_mongodb = db_mongodb.get_collection("energy_1")

consumer = KafkaConsumer(
        "Energy",
        bootstrap_servers='192.168.1.70:9092',
        auto_offset_reset='earliest',
        group_id='section_1'
)

hdfs.mkdir('hdfs://localhost:9000/kafka_stock_data')
file = '/home/datamaking/workarea/data.txt'
args_list = ['hdfs', 'dfs', '-put', file, '/kafka_stock_data']
print("Dato hdfs = {}".format(' '.join(args_list)))
proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
proc.communicate()
hdfs_path = 'hdfs://localhost:9000/kafka_stock_data/data.txt'

print("Starting consumer")

for msg in consumer:
    """json a documento mongo db"""
    document_mongodb = json.loads(msg.value)

    values = msg.value.decode('utf-8')
    with hdfs.open(hdfs_path, 'at') as f:
        f.write(f"{values}\n")
    print("Entry Info = {}".format(json.loads(msg.value)))
    """Insertar valores en la base mongo db"""
    response_mongodb = collection_mongodb.insert_one(document_mongodb)
    last_mongodb_id = response_mongodb.inserted_id
    print("Last inserted id in mongo db was: {}".format(last_mongodb_id))