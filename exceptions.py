
class GlobalParamNotFound(Exception):
    def __init__(self):
        Exception("Global Parameter does not exists")