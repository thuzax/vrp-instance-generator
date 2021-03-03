
class GlobalParamNotFound(Exception):
    def __init__(self, parameter):
        message = ""
        message += "Global Parameter " + parameter + " does not exists"
        super().__init__(message)

class ParamUsedButNoParamRequired(Exception):
    def __init__(self, parameter_used, parameter_needed):
        message = ""
        message += "Parameter " + parameter_used + " was specified, "
        message += "but the needed parameter " + parameter_needed + " "
        message += "was not provided"
        
        super().__init__(message)

        
