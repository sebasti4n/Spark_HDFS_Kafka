# !/bin/bash
echo "Start hadoop starts the Hadoop DFS daemons, the namenode and datanodes. http://localhost:9870"
echo "http://localhost:9870/explorer.html#/kafka_stock_data"
start-dfs.sh 

echo "Start YARN http://localhost:8088/"
start-yarn.sh

echo "Start mongo db. Se puede monitorear en robo3t"
mongod

echo "Start zookeeper"
gnome-terminal --tab -- bash -c "sleep 1s; bash StartZookeeper.sh; exec bash -i"

echo "Start kafka"
gnome-terminal --tab -- bash -c "sleep 10; bash StartKafka.sh; exec bash -i"

echo "Start MySql"
 echo datamaking | sudo -S service mysql start
 
gnome-terminal -x sh -c "sleep 20s; python3 main_1.py; bash"

gnome-terminal -x sh -c "sudo systemctl start zeppelin; sudo systemctl enable zeppelin; jupyter notebook; sudo systemctl status zeppelin; bash"

echo "Start Superset http://localhost:8099"
cd /home/datamaking/pvenvironments
source datamaking/bin/activate
superset run -h 0.0.0.0 -p 8099  --with-threads --reload --debugger






