from django import forms
from django.contrib import messages
from common.utils.files import get_full_file_path, load_json_file_as_dict
from common.enums import MessageTypes, CrudOperations


class Messenger(object):
    MESSAGE_TEMPLATES_PATH = 'common/assets/message_templates.json'

    @staticmethod
    def crud_message(request, crud_operation, model_class, is_denied=False):
        """
        :param request: instance of django.core.handlers.wsgi.WSGIRequest
        :param crud_operation: instance of common.enums.CrudOperations
        :param model_class: subclass of django.db.models.Model
        :param is_denied: boolean
        """
        message_args = {
            'action': crud_operation.value
        }
        if crud_operation == CrudOperations.CREATE and is_denied:
            message_args['model'] = f'a new {model_class.__name__}'
        elif is_denied:
            message_args['model'] = f'this {model_class.__name__}'
        else:
            message_args['model'] = model_class.__name__

        if is_denied:
            message_args['model'] = message_args['model'].lower()
            message_template = Messenger.__get_message_template(MessageTypes.CRUD_DENIED.value)
            messages.error(request, message_template.format(**message_args))
        else:
            message_args['action'] = f'{message_args["action"]}d'
            message_template = Messenger.__get_message_template(MessageTypes.CRUD_SUCCESS.value)
            messages.success(request, message_template.format(**message_args))



    @staticmethod
    def form_invalid(validation_error):
        """
        :param validation_error: instance of common.enums.ValidationErrors
        """
        template_key = f'{MessageTypes.FORM_INVALID.value}__{validation_error.value}'
        message_template = Messenger.__get_message_template(template_key)
        raise forms.ValidationError(message_template)

    @staticmethod
    def __get_message_template(template_key):
        templates = load_json_file_as_dict(get_full_file_path(Messenger.MESSAGE_TEMPLATES_PATH))
        return templates[template_key]
