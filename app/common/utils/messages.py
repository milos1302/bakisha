from django import forms
from django.db.models import Model
from django.contrib import messages
from common.utils.files import get_full_file_path, load_json_file_as_dict
from common.utils.errors import raise_type_error
from common.enums import CrudOperations, MessageTypes, ValidationErrors
from organization.models import Organization
from game.models import Game
from user.models import Profile


class Messenger(object):
    MESSAGE_TEMPLATE_DIR_PATH = 'common/assets/message_templates'

    @staticmethod
    def crud_success(request, crud_operation, instance):
        Messenger.__validate_crud_method_args(crud_operation, instance)

        message_args = {
            'class_name': type(instance).__name__
        }
        if type(instance) in (Game, Organization):
            message_args['object_name'] = instance.name
        if type(instance) == Profile:
            message_args['object_name'] = instance.user.username
        message_template = Messenger.__get_message_template(MessageTypes.CRUD_SUCCESS, key=crud_operation.value)
        message = message_template.format(**message_args)
        messages.success(request, message)

    @staticmethod
    def crud_denied(request, crud_operation, instance=None, instance_class=None):
        Messenger.__validate_crud_method_args(crud_operation, instance, instance_class)

        message_args = {}
        if isinstance(instance, Organization):
            message_args['organization'] = instance.name
        if isinstance(instance, Game):
            message_args['game'] = instance.name
            message_args['organization'] = instance.organization.name
        if isinstance(instance, Profile):
            message_args['owner'] = instance.user.username

        first_key = instance_class.__name__ if instance_class is not None else type(instance).__name__
        message_template = Messenger.__get_nested_message_template(MessageTypes.CRUD_DENIED,
                                                                   first_key, second_key=crud_operation.value)
        message = message_template.format(**message_args)
        messages.error(request, message)

    @staticmethod
    def form_invalid(validation_error, username):
        if not isinstance(validation_error, ValidationErrors):
            raise_type_error(arg_name='validation_error', value=validation_error,
                             value_class=ValidationErrors)

        message_args = {
            'username': username
        }
        message_template = Messenger.__get_message_template(MessageTypes.FORM_INVALID, key=validation_error.value)
        message = message_template.format(**message_args)
        raise forms.ValidationError(message)

    @staticmethod
    def __get_message_template(message_type, key):
        templates_path = f'{Messenger.MESSAGE_TEMPLATE_DIR_PATH}/{message_type.value}.json'
        templates = load_json_file_as_dict(get_full_file_path(templates_path))
        return templates[key]

    @staticmethod
    def __get_nested_message_template(message_type, first_key, second_key):
        message_templates = Messenger.__get_message_template(message_type, first_key)
        return message_templates[second_key]

    @staticmethod
    def __validate_crud_method_args(crud_operation, instance=None, instance_class=None):
        if not isinstance(crud_operation, CrudOperations):
            raise_type_error(arg_name='crud_operation', value=instance, value_class=CrudOperations)
        if crud_operation == CrudOperations.CREATE:
            if instance_class is None:
                raise Exception('Missing value for "instance_class"')
            if not issubclass(instance_class, Model):
                raise_type_error(arg_name='instance_class', value=instance_class, value_class=Model)
        if instance is not None and not issubclass(type(instance), Model):
            raise_type_error(arg_name='instance', value=instance, value_class=Model)
