from flask import request


class AccessToProjects:
    @staticmethod
    def get(id):
        response = request.get('https://localhost:6300/projects/{0}/calculation'.format(id))
        return response.json(), response.status_code

    @staticmethod
    def put(id, status):
        request.put('https://localhost:6300/projects/{0}/calculation'.format(id), json={"status": status})


class AccessToProjectsByPage:
    @staticmethod
    def get(id, page):
        response = request.get('https://localhost:6300/projects/{0}/calculation/{1}'.format(id, page))
        return response.json(), response.status_code


class AccessToContracts:
    @staticmethod
    def get(id):
        response = request.get("http://localhost:5000/api/contracts/{0}".format(id))
        return response.json(), response.status_code
