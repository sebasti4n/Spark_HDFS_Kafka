from kafka import KafkaConsumer
import json
import pydoop.hdfs as hdfs
import subprocess
from pymongo import MongoClient
import mysql.connector
import datetime

# Configuracion/Coneccion MySql
mydb_sql = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="admin",
    database="energy_1"
)
cursor = mydb_sql.cursor()

print(mydb_sql)

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
print("Waiting for the producer")

for msg in consumer:

    try:
        print("Carga de datos en  HDFS bd de Hadoop")
        document_mongodb = json.loads(msg.value)
        values = msg.value.decode('utf-8')
        with hdfs.open(hdfs_path, 'at') as f:
            f.write(f"{values}\n")
        print("Entry Info = {}".format(json.loads(msg.value)))
    except Exception as e:
        print("Error en la escritura en HDFS ", e)

    try:
        print("json a documento mongo db")
        print("Insertar valores en la base mongo db")
        response_mongodb = collection_mongodb.insert_one(document_mongodb)
        last_mongodb_id = response_mongodb.inserted_id
        print("Last inserted id in mongo db was: {}".format(last_mongodb_id))
    except Exception as e:
        print("Error en el documento o base de datos mongo db ", e)

    try:
        print("Guardar info en mysql")
        time = document_mongodb['time']
        voltage = document_mongodb['voltage']
        current = document_mongodb['current']
        power = document_mongodb['Power']
        energy = document_mongodb['Energy']
        frecuency = document_mongodb['Frecuency']
        powerfactor = document_mongodb['PowerFactor']
        query = "INSERT INTO energy (time, voltage, current, power, energy, frecuency, powerfactor) " \
                " VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (time, voltage, current, power, energy, frecuency, powerfactor))
        mydb_sql.commit()
        print(time)
        # hour power recording
        query = "DROP TABLE  IF EXISTS PWH"
        cursor.execute(query)
        query = 'CREATE TABLE PWH AS SELECT ' \
                'CONVERT(CONCAT(SUBSTRING(CONVERT(ROUND(AVG(time)), CHAR), 1,12), "00") , DATETIME) ' \
                'as time, avg(power) as avg FROM energy GROUP BY hour(time), dayofyear(time)'
        cursor.execute(query)
        mydb_sql.commit()
    except Exception as e:
        print("Error en la base de datos MySQL ", e)
