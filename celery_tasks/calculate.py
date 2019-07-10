from celery_tasks.init_celery import celery
from decimal import Decimal

from data_api import data_api
from services.models import Calculation
from services.config import db
from constants.constants import STATUS_COMPLETED


@celery.task
def calculate_by_rules(project_id):

    calculation = Calculation()
    project_info = data_api.AccessToProjects.get(project_id)
    data = project_info.get("data")
    contract = project_info.get("contract_id")
    rules = data_api.AccessToContracts.get(contract)
    operands = []
    operator = rules.get('operator')
    for key in rules:
        name_field = rules.get(key)
        if name_field in data:
            operands.append(Decimal(data.get(name_field)))

    expression = str(operands[0]) + operator + str(operands[1]) + "*" + str(rules.get('coefficient'))
    calculate = Decimal(eval(expression))
    db.session.add(calculation)
    db.session.commit()
    data_api.AccessToProjects.put(project_id, STATUS_COMPLETED)
    return calculate