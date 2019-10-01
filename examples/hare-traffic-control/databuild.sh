export HADOOP_USER_NAME="svc_data-science"
export WORKERS=100
export SPARK_VERSION=2.4.0p1-cdh5-dcc2-1
export SPARK_DIR="/home/agrondin/spark/spark-dist-$SPARK_VERSION-bin"
$SPARK_DIR/bin/spark-submit   --conf spark.ui.port=12345   --conf spark.driver.maxResultSize=2g   --conf spark.shuffle.service.enabled=true   --conf spark.dynamicAllocation.enabled=true   --total-executor-cores $WORKERS  databuild.py

