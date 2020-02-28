import os
import json
from bakisha import settings

def get_full_file_path(relative_path):
    return os.path.join(settings.BASE_DIR, relative_path)

def load_json_file_as_dict(json_path):
    with open(json_path) as message_templates_json:
        return json.load(message_templates_json)
