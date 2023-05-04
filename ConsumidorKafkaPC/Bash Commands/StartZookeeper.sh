# !/bin/bash

echo "Start zookeeper"
cd workarea/softwares/kafka_2.12-3.2.0
 echo datamaking | sudo -S bin/zookeeper-server-start.sh config/zookeeper.properties
