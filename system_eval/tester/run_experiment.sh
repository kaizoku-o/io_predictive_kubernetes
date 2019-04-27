#!/bin/bash +x

stressormode=$2
experimentnum=$1
scheduler=$3

mysql_yaml="mysql_database.yml"
stressor_yaml="io-stressor.yaml"
experimentdir="/home/ubuntu/system-eval/STOCK/exp1"
stressor_container_name="io-stressor"

promIP="172.31.7.88"
promUser="ubuntu"

echo "Begin Experiment ${experimentnum} with ${stressormode} stressors with scheduler ${scheduler}"

echo "Cleaning up system.."
echo "Deleting existing ${stressor_yaml} Stressors"

kubectl delete -f ${stressor_yaml}
kubectl delete -f ${mysql_yaml}

echo "Waiting for cleanup"
sleep 60

echo "Deploying ${stressormode} stressors"

kubectl create -f ${stressor_yaml}
echo "scaling stressors"
for i in $(seq 1 ${stressormode}); do kubectl scale deployment ${stressor_container_name} --replicas=$i; sleep 30; done
kubectl get pods -o wide

echo "Deploying ${mysql_yaml}"
kubectl create -f ${mysql_yaml}
kubectl get pods -o wide
sleep 30

echo "SSH into prometheus and begin test"
ssh -q ${promUser}@${promIP} << EOF
  cd ${experimentdir} && sudo make test > ${scheduler}_${experimentnum}_${stressormode}.out
  mv query_results.json ${scheduler}_${experimentnum}_${stressormode}.json
  ls
EOF