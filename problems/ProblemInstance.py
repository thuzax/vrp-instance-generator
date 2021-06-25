import problems
instance = None

def Instance():
    global instance

    if (instance is None):
        instance = problems.PDPTWURA()
    
    return instance
