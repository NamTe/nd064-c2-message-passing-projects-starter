# bus.py
import signal
from json import loads
from os import environ as env
from threading import Event

from flask_kafka import FlaskKafka

KAFKA_HOST = env.get("KAFKA-HOST")
KAFKA_PORT = env.get("KAFKA-PORT")
KAFKA_SERVER = f"{KAFKA_HOST}:{KAFKA_PORT}"


INTERRUPT_EVENT = Event()

bus = FlaskKafka(
    INTERRUPT_EVENT,
    bootstrap_servers=",".join([KAFKA_SERVER]),
    value_deserializer=lambda x: loads(x.decode("utf-8")),
    group_id="consumer-grp-id"
)


def listen_kill_server():
    signal.signal(signal.SIGTERM, bus.interrupted_process)
    signal.signal(signal.SIGINT, bus.interrupted_process)
    signal.signal(signal.SIGQUIT, bus.interrupted_process)
    signal.signal(signal.SIGHUP, bus.interrupted_process)
