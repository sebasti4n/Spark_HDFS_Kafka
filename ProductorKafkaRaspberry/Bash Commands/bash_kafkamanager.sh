#!/bin/bash

echo "iniciar kafka manager"
sudo rm /home/pi/kafka-manager/kafka-manager/target/universal/cmak-3.0.0.5/RUNNING_PID
cd  kafka-manager/kafka-manager/target/universal/cmak-3.0.0.5
sudo bin/cmak -Dconfig.file=conf/application.conf -Dhttp.port=8080
