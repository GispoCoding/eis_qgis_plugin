import importlib
import os

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

pluginPath = os.path.dirname(__file__)


class EISProvider(QgsProcessingProvider):
    def __init__(self) -> None:
        self.alg_folder = os.path.join(pluginPath, "algorithms")
        super().__init__()

    def id(self) -> str:
        return "eis"

    def name(self) -> str:
        return "EIS"

    def load(self) -> bool:
        self.refreshAlgorithms()
        return True

    # def icon(self):
    #     return QIcon(os.path.join(pluginPath, '../resources/icons/plugin_icon.png'))

    def loadAlgorithms(self) -> None:
        algorithm_instances = self.load_algorithms_from_directory(self.alg_folder)

        # Add the algorithm instances to the provider
        for algorithm in algorithm_instances:
            self.addAlgorithm(algorithm)

    def load_algorithms_from_directory(self, algorithms_dir: str):
        algorithm_instances = []

        for file_name in os.listdir(algorithms_dir):
            if file_name.endswith(".py") and not file_name.startswith("__"):
                module_name = file_name[:-3]
                class_name_parts = [
                    part.capitalize() for part in module_name.split("_")
                ]
                class_name = "EIS" + "".join(class_name_parts)

                # Import the module
                spec = importlib.util.spec_from_file_location(
                    module_name, os.path.join(algorithms_dir, file_name)
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Create an instance of the algorithm class and add it to the list
                algorithm_class = getattr(module, class_name)
                algorithm_instances.append(algorithm_class())

        return algorithm_instances
