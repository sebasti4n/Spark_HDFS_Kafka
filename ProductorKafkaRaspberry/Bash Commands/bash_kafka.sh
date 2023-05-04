#!bin/bash
echo "Para iniciar Zookeeper"
cd kafka
sudo bin/zookeeper-server-start.sh config/zookeeper.properties
