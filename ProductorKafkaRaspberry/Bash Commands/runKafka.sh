#!/bin/bash

echo "Comenzando"

gnome-terminal --tab -- bash -c  "sleep 1s; bash bash_kafka.sh; exec bash -i"
gnome-terminal --tab -- bash -c  "sleep 10s; bash bash_kafka1.sh; exec bash -i"
gnome-terminal --tab -- bash -c  "sleep 20s; bash bash_kafkamanager.sh; exec bash -i"  
gnome-terminal --tab -- bash -c  "sleep 35s; bash bash_modbuskafka.sh; exec bash -i"
