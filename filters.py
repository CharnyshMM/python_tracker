from enum import Enum

class Filters(Enum):
    START_DATE = "start_date"
    END_DATE = "end_date"
    TAGS = "tags"
    USER_TAGS = 'user_tags'
    PATH = "path"
    OWNER_NAME = "owner_name"
    MESSAGE = "message_text"
    NAME = "name"
