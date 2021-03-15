
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
    def __init__(self, status_code):
        message = ""
        message += "Could not connect to routing server. "
        message += "HTTP request code error: " + str(status_code)

        super().__init__(message)

