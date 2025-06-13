from cerberus import Validator

class ConfigValidator:
    def __init__(self, schema):
        self.validator = Validator(schema)

    def validate(self, config):
        if not self.validator.validate(config):
            raise ValueError(f'Configuration validation failed: {self.validator.errors}')
