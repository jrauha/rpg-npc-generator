class ValidationError(Exception):
    def __init__(self, attribute, reason):
        self.attribute = attribute
        self.reason = reason
        super(ValidationError, self).__init__((attribute, reason))
