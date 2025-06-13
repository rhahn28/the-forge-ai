import yaml

class ConfigReader:
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def get_config(self):
        return self.config
