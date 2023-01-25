import configparser
from qgis.core import QgsProcessingProvider
from eis_processing_algorithm import EISProcessingAlgorithm


class EISProvider(QgsProcessingProvider):

    def __init__(self, description_file) -> None:
        super().__init__()
        self.description_file = description_file
        self.loadAlgorithms()

    def id(self) -> str:
        return 'eis'

    def name(self) -> str:
        return 'EIS Wizard processing provider'

    def load(self) -> bool:
        self.refreshAlgorithms()
        return True

    def parse_algorithm_config(self, config: configparser.ConfigParser, algorithm: str):
        alg_parameters = []
        alg_descriptions = dict(config.items(algorithm))
        for key, param_data in alg_descriptions.items():
            if key[:6] == 'param_':
                parsed_param_data = self.parse_algorithm_parameter(param_data)
                alg_parameters.append(parsed_param_data)
        return EISProcessingAlgorithm(alg_descriptions, alg_parameters)
        
    def parse_algorithm_parameter(self, parameter_data: str):
        param_data = {}
        elements = parameter_data.split(',')
        for param_element in elements:
            data = [item.strip() for item in param_element.split(':')]
            param_data[data[0].lower()] = data[1]
        return param_data

    def loadAlgorithms(self) -> None:
        config = configparser.ConfigParser()
        config.read(self.description_file)
        for algorithm in config.sections():
            alg = self.parse_algorithm_config(config, algorithm)
            self.addAlgorithm(alg)

# FOR TESTING
def main():
    EISProvider('eis_processing_algs_config.ini')
    print("Done")

main()