
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

class DistanceToPointCannotBeCalculated(Exception):
    def __init__(self, point):
        message = ""
        message += "The distances to the point " + str(point)
        message += "could not be calculated with OSRM. "
        message += "Please verify if the server is working properly"
        message += "and if there is valid routes to the point."
        
        super().__init__(message)

class CouldNotReachTheRoutingServer(Exception):
    def __init__(self, request_url, status_code):
        message = ""
        message += "Could not connect to routing server. "
        message += "URL: " + request_url + " . "
        message += "HTTP request code error: " + str(status_code) + "."

        super().__init__(message)

class MinServiceTimeGreaterThanMax(Exception):
    def __init__(self):
        message = ""
        message += "The input param 'max_service_time' must be greater than "
        message += "the 'max_service_time' input param."

        super().__init__(message)

class MinServiceTimeCannotBeNoneNegative(Exception):
    def __init__(self):
        message = ""
        message += "The input param 'max_service_time'"
        message += "must be greater or equal 0"

        super().__init__(message)

class GreaterThanZeroMinAndMaxServicesTimes(Exception):
    def __init__(self):
        message = ""
        message += "Service Time Constraint needs a "
        message += "'min_service_time' or 'max_service_time'"
        message += "greater than 0"

        super().__init__(message)

class GreaterThanZeroParameter(Exception):
    def __init__(self, name):
        message = ""
        message += "The variable " + name + " must have a value"
        message += "greater than 0"

        super().__init__(message)