import re
class CollectionResponse:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class TaskResponse:
    def __init__(self):
        self.id
  
str_to_val = {"NONE":0, "LOW":1, "MEDIUM":2, "HIGH":3}
val_to_str = {val:key for key, val in str_to_val.items()}
def get_priority_val(str):
    return str_to_val[str]
def get_priority_str(val):
    return val_to_str[val].capitalize()

def datetime_to_mdy(str) -> str:
    date = re.compile(r'(\d{4})-(\d{2})-(\d{2})*')
    match = re.match(date, str)
    year, month, day = match[1], match[2], match[3]
    return f'{month}/{day}/{year}'

email_pattern = re.compile(r'\w+@\w+.[A-Za-z]{3}')
def valid_email(str) -> bool:
    return True
