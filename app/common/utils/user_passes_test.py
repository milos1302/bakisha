from game.models import Game
from organization.models import Organization
from user.models import Account
from common.enums import CrudOperations
from common.utils.messages import Messenger


class UserPassesTest(object):

    @staticmethod
    def user_passes_test_with_message(request, crud_operation, model_class, instance=None):
        """
        Returns True if the user passes the test, and False otherwise.
        It also sets the error message if the user hasn't passed the test

        :param request: instance of django.core.handlers.wsgi.WSGIRequest
        :param crud_operation: instance of common.enums.CrudOperations
        :param model_class: subclass of django.db.models.Model
        :param instance: instance of django.db.models.Model
        :return: boolean
        """

        is_allowed = UserPassesTest.__is_allowed(request, crud_operation, model_class, instance)
        if not is_allowed:
            Messenger.crud_message(request, crud_operation, model_class, True)

        return is_allowed

    @staticmethod
    def __is_allowed(request, crud_operation, model_class, instance):
        """
        Returns True if the user is allowed to perform a particular CRUD
        operation, and False otherwise

        :param request: instance of django.core.handlers.wsgi.WSGIRequest
        :param crud_operation: instance of common.enums.CrudOperations
        :param model_class: subclass of django.db.models.Model
        :param instance: instance of django.db.models.Model
        :return: boolean
        """
        if model_class == Organization:
            if crud_operation == CrudOperations.CREATE:
                return request.user.account.subscription == Account.PAID
            elif crud_operation == CrudOperations.UPDATE:
                return instance.administrators.filter(id=request.user.id).exists()
            elif crud_operation == CrudOperations.DELETE:
                return request.user == instance.created_by

        if model_class == Game:
            if crud_operation == CrudOperations.CREATE:
                return request.user.administrating_organizations.first() is not None
            elif crud_operation == CrudOperations.UPDATE or crud_operation == CrudOperations.DELETE:
                return instance.organization.administrators.filter(pk=request.user.pk).exists()

        if model_class == Account:
            if crud_operation == CrudOperations.DELETE:
                return request.user == instance.user

        return False
