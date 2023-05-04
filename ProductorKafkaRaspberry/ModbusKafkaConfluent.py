from email.policy import default
from encodings import utf_8
from ensurepip import bootstrap
import json
from json import JSONEncoder 
from kafka import KafkaProducer
import time
from Modbus import datajson
import datetime
#Subclass jsonEncoder para datetime
class DateTimeEncoder(JSONEncoder):
    #Override the deafult method
    def default(self, obj):
        if isinstance (obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        
## metodo json serializer, convertir a equivalente json
def json_serializer(data):
    return json.dumps(data, cls = DateTimeEncoder).encode("utf-8")

## Kafka producer: configuración
# producer  = KafkaProducer(bootstrap_servers=['192.168.1.70:9092'],
#                             value_serializer=json_serializer)
producer  = KafkaProducer(bootstrap_servers=['pkc-4v5zz.sa-east-1.aws.confluent.cloud:9092'],
                            value_serializer=json_serializer,
                            security_protocol="SASL_SSL",
                            sasl_mechanism="PLAIN",
                            sasl_plain_password="IxCP/IjHOSKTalN9ht7OtCN1bHCEH5SbMBjC6wFUdWThdDiCEmKECQiW4sbwDrfF",
                            sasl_plain_username="ZN2I4E6J7ZQHUSOM")

if __name__ == "__main__":
    while 1==1 :
        time.sleep(4)
        registers = datajson()
        print(registers)
        producer.send("Energy", registers)
        