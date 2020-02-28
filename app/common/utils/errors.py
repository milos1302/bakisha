from django import forms
from common.enums import ValidationErrors
from common.utils.files import get_full_file_path, load_json_file_as_dict


def raise_validation_error(error_type, username):
    if not isinstance(error_type, ValidationErrors):
        raise TypeError(f'Invalid value for error_type! Got "{error_type}". Instance of "{ValidationErrors}" expected.')

    messages = load_json_file_as_dict(get_full_file_path('common/assets/form_validation_error_messages.json'))
    message = messages[error_type.value]
    message = message.format(username=username)
    raise forms.ValidationError(message)
