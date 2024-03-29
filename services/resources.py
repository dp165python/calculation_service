from flask_restful import Resource
from flask import jsonify, request
from services.models import Calculations
from celery_tasks.calculate import calculate_by_rules
from services.config import db
from data_api.data_api import AccessToProjects
from constants.constants import STATUS_IN_PROGRESS, STATUS_COMPLETED


class Calculate(Resource):
    def post(self):

        calculate_by_rules.delay(request.json["project_id"])
        AccessToProjects.put(request.json["project_id"], STATUS_IN_PROGRESS)
        return jsonify({'status':STATUS_COMPLETED})


class Results(Resource):
    def get(self):
        project_id = request.json["project_id"]
        calculation = db.session.query(Calculations).filter_by(project_id=project_id).first()
        return jsonify({"result": calculation})
