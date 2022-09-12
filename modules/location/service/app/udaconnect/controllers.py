from datetime import datetime
from typing import List, Optional

from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from app.udaconnect.services import LocationService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnectLocation", description="Retrieve/Register location")  # noqa


# TODO: This needs better exception handling


@api.route("/locations")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        request.get_json()
        location: Location = LocationService.create(request.get_json())
        return location


@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location


@api.route("/locations/persons/<person_id>")
class LocationsPersonResource(Resource):
    @api.param("person_id", "Unique ID for a given Location's person", _in="query")
    @api.param("start_date", "Lower bound of date range", _in="query")
    @api.param("end_date", "Upper bound of date range", _in="query")
    @responds(schema=LocationSchema, many=True)
    def get(self, person_id) -> List[Location]:
        start_date: datetime = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
        location: Location = LocationService.retrieve_person(
            person_id, start_date, end_date
        )
        return location
