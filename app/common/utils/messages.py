from common.utils.files import get_full_file_path, load_json_file_as_dict
from common.enums import CrudOperations
from organization.models import Organization
from game.models import Game


def get_permission_denied_message(operation, model_class, model_instance):
    model_name = model_class.__name__
    message_template = __get_permission_denied_message_template(model_name, operation.value)

    message_args = {}
    if operation in (CrudOperations.UPDATE, CrudOperations.DELETE):
        if model_class == Organization:
            message_args['organization'] = model_instance.name
        if model_class == Game:
            message_args['organization'] = model_instance.organization.name
            message_args['game'] = model_instance.name
    if operation == CrudOperations.CREATE and model_class == Organization:
        message_args['group'] = 'Administrators'

    return message_template.format(**message_args)


def __get_permission_denied_message_template(model, operation):
    message_templates = load_json_file_as_dict(get_full_file_path('common/assets/permission_denied_messages.json'))
    return message_templates[model][operation]
