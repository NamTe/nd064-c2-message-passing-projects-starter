# Deploy
1. `kubectl apply -f deployment/db-configmap.yaml` - Set up environment variables for the pods
2. `kubectl apply -f deployment/db-secret.yaml` - Set up secrets for the pods
3. `kubectl apply -f deployment/postgres.yaml` - Set up a Postgres database running PostGIS
4. `kubectl apply -f deployment/udaconnect-app.yaml` - Set up the service and deployment for the web app
5. `kubectl apply -f deployment/kafka-configmap.yaml` - Set up environment variables for the Kafka
6. `kubectl apply -f deployment/kafka-service.yaml` - Set up Kafka queue
7. `kubectl apply -f deployment/zookeeper-service.yaml` - Set up Kafka queue
8. `kubectl apply -f deployment/udaconnect-location-api.yaml` - Set up location api
9. `kubectl apply -f deployment/udaconnect-connection-api.yaml` - Set up connection api
10. `kubectl apply -f deployment/udaconnect-location-gRPC.yaml` - Set up location grpc
11. `kubectl apply -f deployment/udaconnect-person-api.yaml` - Set up person api
12. `sh scripts/run_db_command.sh <POD_NAME>` - Seed your database against the `postgres` pod. (`kubectl get pods` will give you the `POD_NAME`)