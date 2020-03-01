from enum import Enum, unique


@unique
class CrudOperations(Enum):
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'


@unique
class ValidationErrors(Enum):
    REMOVE_OWNER_FROM_ADMINS = 'remove_owner_from_admins'
    REMOVE_ADMIN_FROM_MEMBERS = 'remove_admin_from_members'


@unique
class MessageTypes(Enum):
    CRUD_SUCCESS = 'crud_success'
    CRUD_DENIED = 'crud_denied'
    FORM_INVALID = 'form_invalid'
