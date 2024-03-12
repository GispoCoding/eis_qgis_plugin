import importlib
import os

from qgis.core import QgsProcessingProvider

PLUGIN_PATH = os.path.dirname(__file__)
ICON_PATH = os.path.join(PLUGIN_PATH, "../resources/icons/plugin_icon.png")


class EISProvider(QgsProcessingProvider):
    def __init__(self) -> None:
        self.base_alg_folder = os.path.join(PLUGIN_PATH, "algorithms")
        super().__init__()

    def id(self) -> str:
        return "eis"

    def name(self) -> str:
        return "EIS"

    def load(self) -> bool:
        self.refreshAlgorithms()
        return True

    # def icon(self):
    #     return QIcon(ICON_PATH)

    def loadAlgorithms(self) -> None:
        # Load algorithms from each directory
        validation = self.load_algorithms_from_directory("validation")
        vector_processing = self.load_algorithms_from_directory("vector_processing")
        raster_processing = self.load_algorithms_from_directory("raster_processing")
        exploratory_analysis = self.load_algorithms_from_directory("exploratory_analysis")
        prediction = self.load_algorithms_from_directory("prediction")
        transformations = self.load_algorithms_from_directory("transformations")
        utilities = self.load_algorithms_from_directory("utilities")

        # Add the algorithm instances to the provider
        for algorithm in (
            validation + vector_processing + raster_processing +
            exploratory_analysis + prediction + transformations + utilities
        ):
            self.addAlgorithm(algorithm)

    def load_algorithms_from_directory(self, category: str):
        algorithms_dir = os.path.join(self.base_alg_folder, category)
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
