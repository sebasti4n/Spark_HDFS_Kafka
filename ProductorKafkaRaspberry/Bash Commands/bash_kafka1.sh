#!/bin/bass

echo "Iniciar Kafka"
cd kafka 
sudo JMX_PORT=8004 bin/kafka-server-start.sh config/server.properties
./bin/kafka-server-start.sh
