
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

class MaxMustBeGreaterThanMin(Exception):
    def __init__(self, min_parameter, max_parameter):
        message = ""
        message += "The parameter " + str(max_parameter) + "value "
        message += "must be greater than the parameter "
        message += str(min_parameter) 

        super().__init__(message)

class ValueCannotBeNoneNegative(Exception):
    def __init__(self, parameter):
        message = ""
        message += "The input parameter " + str(parameter)
        message += "must be greater or equal 0"

        super().__init__(message)

class MinOrMaxGreaterThanZero(Exception):
    def __init__(self, min_parameter, max_parameter):
        message = ""
        message += str(min_parameter) + " or "
        message += str(max_parameter) + " value needs to be "
        message += "greater than 0"

        super().__init__(message)

class GreaterThanZeroParameter(Exception):
    def __init__(self, name):
        message = ""
        message += "The variable " + name + " must have a value"
        message += "greater than 0"

        super().__init__(message)

class ParamMustBeSetted(Exception):
    def __init__(self, name):
        message = ""
        message += "The parameter " + name + " must be setted"

        super().__init__(message)

class ObjectDoesNotHaveAttribute(Exception):
    def __init__(self, class_name, attribute_name):
        message = ""
        message += "Object from class " + str(class_name) + " "
        message += "does not have attribute " + str(attribute_name)

        super().__init__(message)
