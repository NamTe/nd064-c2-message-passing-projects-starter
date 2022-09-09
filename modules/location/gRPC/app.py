import json
import logging
import sys
import time
from concurrent import futures
from os import environ as env

import grpc
from kafka import KafkaProducer

import location_pb2
import location_pb2_grpc

TOPIC_NAME = env.get("TOPIC_NAME")
KAFKA_HOST = env.get("KAFKA-HOST")
KAFKA_PORT = env.get("KAFKA-PORT")

KAFKA_SERVER = f"{KAFKA_HOST}:{KAFKA_PORT}"


DATE_FORMAT = "%Y-%m-%d"

server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
kafka_producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

class LocationGRPCServicer(location_pb2_grpc.LocationRpcServiceServicer):
    def Create(self, request, context):

        request_value = {
            "person_id": request.person_id,
            "latitude": request.latitude,
            "longitude": request.longitude,
            "creation_time": request.creation_time,
        }
        print(request_value)
        logging.info("Before Send")
        kafka_producer.send(TOPIC_NAME, request_value)
        logging.info("After Send")
        kafka_producer.flush()
        logging.info("After flush")

        return location_pb2.LocationMessage(**request_value)


def init_grpc():
    # Initialize gRPC server
    location_pb2_grpc.add_LocationRpcServiceServicer_to_server(
        LocationGRPCServicer(), server
    )
    print("Server starting on port 5005...")
    server.add_insecure_port("[::]:5005")
    server.start()


if __name__ == "__main__":
    init_grpc()
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [stdout_handler]
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=handlers,
        format="%(levelname)s:%(name)s: %(asctime)s, %(message)s",
    )
    logging.info("KAFKA-HOST: " + KAFKA_HOST)
    # kafka_producer = init_kafka()
    # Keep thread alive
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
