# !/bin/bash

echo "Start Kafka"
cd workarea/softwares/kafka_2.12-3.2.0
 echo datamaking | sudo -S bin/kafka-server-start.sh config/server.properties 

