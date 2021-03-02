
class GlobalParamNotFound(Exception):
    def __init__(self):
        message = ""
        message += "Global Parameter does not exists"
        super().__init__(message)

class ParamLimitNotSpecified(Exception):
    def __init__(self):
        message = ""
        message += "The --limits parameter was specified,"
        message += "but no limiting parameter "
        message += "(-min-lat, -max-lat, -min-lon, -max-lon)"
        message += "was provided"
        
        super().__init__(message)


class ParamLimitSpecifiedWithoutParamLimits(Exception):
    def __init__(self):
        message = ""
        message += "A limiting parameter "
        message += "(-min-lat, -max-lat, -min-lon, -max-lon) "
        message += "was provided, but the parameter "
        message += "--limits was not specified"
        super().__init__(message)

        
