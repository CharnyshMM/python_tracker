# TODO:
class AttributeMissingError (AttributeError):
    def __init__(self,attribute):
        self.attribute = attribute

    def __str__(self):
        return 'AttributeMissingError '+str(self.attribute)



