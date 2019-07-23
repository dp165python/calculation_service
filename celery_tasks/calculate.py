from celery_tasks.init_celery import celery
from decimal import Decimal

from data_api import data_api
from services.models import Calculation, Projects
from services.config import db
from additional_features import operator_transformation as ot
from constants.constants import STATUS_COMPLETED, PAGE_TO_ACCESS_TO_PROJECTS


@celery.task
def calculate_by_rules(project_id):
    calculation = Calculation()
    project_info = data_api.AccessToProjects.get(project_id)
    data = project_info.get("data")
    contract = project_info.get("project").get("contract_id")
    rules = data_api.AccessToContracts.get(contract)
    operands = []
    operator = ot.get_operation(rules.get('operator'))
    for key in rules:
        name_field = rules.get(key)
        if name_field in data[rules.get('page')]:
            operands.append(Decimal(data.get(name_field)))

    calculate = Decimal(operator(operands[0], operands[1]) * rules.get('coefficient'))
    calculation.result = calculate
    data_api.AccessToProjects.put(project_id, STATUS_COMPLETED)
    db.session.add(calculation)
    db.session.commit()


@celery.task
def calculate_by_rules_with_pagination(project_id):
    project_info = data_api.AccessToProjectsByPage.get(project_id, PAGE_TO_ACCESS_TO_PROJECTS)
    if db.session.query(Projects).filter_by(id=project_id) == None:
        calculation = Calculation()
        contract = project_info.get('contract_id')
        rules = data_api.AccessToContracts.get(contract)
        page_with_data = rules.get('page')
        data = data_api.AccessToProjectsByPage.get(project_id, page_with_data)
        operands = []
        operator = ot.get_operation(rules.get('operator'))
        for key in rules:
            name_field = rules.get(key)
            if name_field in data:
                operands.append(Decimal(data.get(name_field)))

        calculate = Decimal(operator(operands[0], operands[1]) * rules.get('coefficient'))
        data_api.AccessToProjects.put(project_id, STATUS_COMPLETED)
        calculation.result = calculate
        db.session.add(calculation)
        db.session.commit()
