# Apache Spark

- install spark-cluster (or on local)

### for all nodes (master or slaves):
in ~/.bashrc `export SPARK_HOME=/usr/local/spark-3.3.0-bin-hadoop3/`
cp SPARK_HOME/conf/
cp spark-env.sh.template spark-env.sh
vim spark-env.sh
add master-ip as follows:
`SPARK_MASTER_HOST='<master.ip.addr>'`

### on master-node:
```
cd SPARK_HOME/sbin
./start-master.sh
```

### on all slaves:
```
cd SPARK_HOME/sbin
./start-slave.sh  spark://<master.ip.addr>:7077
```

### Check web-ui:
http://<master.ip.addr>:<8080>/

it should show the slaves running
