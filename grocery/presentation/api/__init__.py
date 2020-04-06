from flask import Flask, jsonify, request

from grocery.application.services.create_user import CreateUserService
from grocery.application.services.list_users import ListUsersService
from grocery.presentation.api.serializer import serialize_user, serialize_users

api = Flask(__name__)


@api.route("/users", methods=["GET"])
def list_users():
    service = ListUsersService()
    users = service.run()
    print(serialize_users(users))
    if users:
        return jsonify(serialize_users(users))
    else:
        return {}, 400


@api.route("/users", methods=["POST"])
def create_user():
    content = request.get_json(force=True)
    if not "name" in content:
        return {}, 400
    service = CreateUserService(username=content["name"])
    user = service.run()
    if user:
        return serialize_user(user)
    else:
        return {}, 400
