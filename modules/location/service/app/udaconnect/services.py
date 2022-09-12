import logging
from json import loads
from os import environ as env
from typing import Dict, List

from app import app, db
from app.bus import bus
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

TOPIC_NAME = env.get("TOPIC_NAME")

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-location-api")


class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def retrieve_person(person_id, start_date, end_date) -> List[Location]:
        locations: List = (
            db.session.query(Location)
            .filter(Location.person_id == person_id)
            .filter(Location.creation_time < end_date)
            .filter(Location.creation_time >= start_date)
            .all()
        )

        return locations

    @staticmethod
    def create(location: Dict) -> Location:
        logger.warning(f"validate message: {location}")
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        db.session.add(new_location)
        db.session.commit()

        return new_location


# def kafka_consumer(db):
#     logger.warning("kafka_consumer")
#     consumer = KafkaConsumer(
#         TOPIC_NAME,
#         bootstrap_servers=KAFKA_SERVER,
#         value_deserializer=lambda x: loads(x.decode("utf-8")),
#     )
#     logger.warning("kafka_consumer hello")
#     for message in consumer:
#         logger.warning("kafka_consumer recieved message")
#         new_location = Location()
#         new_location.person_id = message.value["person_id"]
#         new_location.creation_time = message.value["creation_time"]
#         new_location.coordinate = ST_Point(message.value["latitude"], message.value["longitude"])
#         logger.warning("kafka_consumer add ")
#         db.session.add(new_location)
#         db.session.commit()


@bus.handle("locations")
def kafka_consumer(event):
    with app.app_context():
        try:
            logger.warning("kafka_consumer recieved message")
            LocationService.create(event.value)
            logger.warning("After recieved message")
        except Exception as e:
            logger.warning(f"Ops!!! {e}")
