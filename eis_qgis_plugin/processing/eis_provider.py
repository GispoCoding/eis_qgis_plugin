from typing import Dict
import configparser
import os

from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProcessingProvider
from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm

pluginPath = os.path.dirname(__file__)

class EISProvider(QgsProcessingProvider):

    def __init__(self) -> None:
        self.description_file = os.path.join(pluginPath, '../config/eis_config.ini')
        super().__init__()

    def id(self) -> str:
        return 'eis'

    def name(self) -> str:
        return 'EIS'

    def load(self) -> bool:
        # QgsSettings().setValue("path", "/path/to/backend_script.py")

        # NOTE: ProcessingConfig is an older feature and not usable?
        # ProcessingConfig.addSetting(Setting(self.name(),
        #                                     utils.WBT_EXECUTABLE,
        #                                     self.tr('WhiteboxTools executable'),
        #                                     utils.wbtExecutable(),
        #                                     valuetype=Setting.FILE))
        self.refreshAlgorithms()
        return True

    def icon(self):
        return QIcon(os.path.join(pluginPath, '../resources/icons/plugin_icon.png'))

    def parse_algorithm_config(self, config: configparser.ConfigParser, algorithm: str) -> EISProcessingAlgorithm:
        alg_parameters = []
        alg_descriptions = dict(config.items(algorithm))
        for key, param_data in alg_descriptions.items():
            if key[:6] == 'param_':
                parsed_param_data = self.parse_algorithm_parameter(param_data)
                alg_parameters.append(parsed_param_data)
        return EISProcessingAlgorithm(alg_descriptions, alg_parameters)

    def parse_algorithm_parameter(self, parameter_data: str) -> Dict:
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
