import os
import json
from bakisha import settings
from enum import Enum, unique
from django.contrib import messages
from django.db.models import Model
from django.core.handlers.wsgi import WSGIRequest
from game.models import Game
from organization.models import Organization


@unique
class Operation(Enum):
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'


class UserPassesTest(object):

    @staticmethod
    def user_passes_test_with_message(request, operation, model_class, model_instance=None):
        """
        Returns True if user passes the test, and False otherwise.
        It also sets the permission_denied_message to the passed
        view instance if user doesn't pass the test

        :param request: instance of WSGIRequest
        :param operation: instance of Operation
        :param model_class: subclass of Model
        :param model_instance: instance of Model
        :return: boolean
        """

        UserPassesTest.__check_request(request)
        UserPassesTest.__check_operation(operation)
        UserPassesTest.__check_model_class(model_class)
        UserPassesTest.__check_model_instance(model_instance, model_class)

        passes = UserPassesTest.__is_permission_denied(request, operation, model_class, model_instance)
        if not passes:
            message = UserPassesTest.__get_permission_denied_message(operation, model_class, model_instance)
            messages.error(request, message)

        return passes

    @staticmethod
    def __is_permission_denied(request, operation, model_class, model_instance):
        if model_class == Organization:
            if operation == Operation.CREATE:
                return request.user.groups.filter(name='Administrators').exists()
            elif operation == Operation.UPDATE:
                is_administrator = request.user.groups.filter(name='Administrators').exists()
                is_org_admin = model_instance.administrators.filter(id=request.user.id).exists()
                return is_administrator and is_org_admin
            elif operation == Operation.DELETE:
                return request.user == model_instance.created_by

        if model_class == Game:
            if operation == Operation.CREATE:
                return request.user.administrating_organizations.first() is not None
            elif operation == Operation.UPDATE or operation == Operation.DELETE:
                return model_instance.organization.administrators.filter(pk=request.user.pk).exists()

        return False

    @staticmethod
    def __get_permission_denied_message(operation, model_class, model_instance):

        model_name = model_class.__name__
        message_template = UserPassesTest.__get_permission_denied_message_template(model_name, operation.value)

        message_args = {}
        if operation in (Operation.UPDATE, Operation.DELETE):
            if model_class == Organization:
                message_args['organization'] = model_instance.name
            if model_class == Game:
                message_args['organization'] = model_instance.organization.name
                message_args['game'] = model_instance.name
        if operation == Operation.CREATE and model_class == Organization:
            message_args['group'] = 'Administrators'

        return message_template.format(**message_args)

    @staticmethod
    def __check_request(request):
        if not isinstance(request, WSGIRequest):
            raise TypeError(f'Invalid value for request! Got "{request}". Instance of "{WSGIRequest}" expected.')

    @staticmethod
    def __check_operation(operation):
        if not isinstance(operation, Operation):
            raise TypeError(f'Invalid value for operation! Got "{operation}". Instance of "{Operation}" expected.')

    @staticmethod
    def __check_model_class(model_class):
        if not issubclass(model_class, Model):
            raise TypeError(f'Invalid value for model_class! Got "{model_class}". Class of "{Model}" expected.')

    @staticmethod
    def __check_model_instance(model_instance, model_class):
        if model_instance is not None and not isinstance(model_instance, model_class):
            raise TypeError(f'model_instance "{model_instance}" is not an instance of model_class "{model_class}". '
                            f'model_instance and model_class need to match.')

    @staticmethod
    def __get_permission_denied_message_template(model, operation):
        json_path = os.path.join(settings.BASE_DIR, 'common/utils/assets/permission_denied_messages.json')
        with open(json_path) as message_templates_json:
            message_templates = json.load(message_templates_json)
            return message_templates[model][operation]
