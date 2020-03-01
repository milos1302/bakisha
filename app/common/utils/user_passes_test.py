from django.contrib import messages
from django.db.models import Model
from django.core.handlers.wsgi import WSGIRequest
from game.models import Game
from organization.models import Organization
from user.models import Account
from common.enums import CrudOperations
from common.utils.messages import Messenger


class UserPassesTest(object):

    @staticmethod
    def user_passes_test_with_message(request, crud_operation, instance_class, instance=None):
        """
        Returns True if user passes the test, and False otherwise.
        It also sets the permission_denied_message to the passed
        view instance if user doesn't pass the test

        :param request: instance of WSGIRequest
        :param crud_operation: instance of Operation
        :param instance_class: subclass of Model
        :param instance: instance of Model
        :return: boolean
        """

        UserPassesTest.__check_request(request)
        UserPassesTest.__check_crud_operation(crud_operation)
        UserPassesTest.__check_instance_class(instance_class)
        UserPassesTest.__check_instance(instance, instance_class)

        passes = UserPassesTest.__is_permission_denied(request, crud_operation, instance_class, instance)
        print('PASSES', passes)
        if not passes:
            message = Messenger.crud_denied(request, crud_operation, instance_class=instance_class,
                                            instance=instance)
            messages.error(request, message)

        return passes

    @staticmethod
    def __is_permission_denied(request, crud_operation, instance_class, instance):
        if instance_class == Organization:
            if crud_operation == CrudOperations.CREATE:
                return request.user.account.subscription == Account.PAID
            elif crud_operation == CrudOperations.UPDATE:
                has_paid_subscriptions = request.user.account.subscription == Account.PAID
                is_org_admin = instance.administrators.filter(id=request.user.id).exists()
                return has_paid_subscriptions and is_org_admin
            elif crud_operation == CrudOperations.DELETE:
                return request.user == instance.created_by

        if instance_class == Game:
            if crud_operation == CrudOperations.CREATE:
                return request.user.administrating_organizations.first() is not None
            elif crud_operation == CrudOperations.UPDATE or crud_operation == CrudOperations.DELETE:
                return instance.organization.administrators.filter(pk=request.user.pk).exists()

        if instance_class == Account:
            if crud_operation == CrudOperations.DELETE:
                return request.user == instance.user

        return False

    @staticmethod
    def __check_request(request):
        if not isinstance(request, WSGIRequest):
            raise TypeError(f'Invalid value for request! Got "{request}". Instance of "{WSGIRequest}" expected.')

    @staticmethod
    def __check_crud_operation(crud_operation):
        if not isinstance(crud_operation, CrudOperations):
            raise TypeError(
                f'Invalid value for crud_operation! Got "{crud_operation}". Instance of "{CrudOperations}" expected.')

    @staticmethod
    def __check_instance_class(instance_class):
        if not issubclass(instance_class, Model):
            raise TypeError(f'Invalid value for instance_class! Got "{instance_class}". Class of "{Model}" expected.')

    @staticmethod
    def __check_instance(instance, instance_class):
        if instance is not None and not isinstance(instance, instance_class):
            raise TypeError(f'instance "{instance}" is not an instance of instance_class "{instance_class}". '
                            f'instance and instance_class need to match.')
