from typing import Dict, List, Optional

from qgis.core import QgsProject
from qgis.PyQt.QtCore import QObject, pyqtSignal

from eis_qgis_plugin.wizard.modeling.ml_model_info import MLModelInfo


class ModelManager(QObject):

    BASE_KEY = "models"
    ALL_MODELS_KEY = "all_models"
    SCOPE = "eis"

    models_updated = pyqtSignal()


    @classmethod
    def _get_key(self, id):
        return f"{self.BASE_KEY}/{id}"

    @classmethod
    def get_model_info(self, id) -> Optional[MLModelInfo]:
        key = self._get_key(id)
        info_json, conversion_ok = QgsProject.instance().readEntry(self.SCOPE, key, "")
        print(info_json, conversion_ok)
        if conversion_ok:
            ml_model_info = MLModelInfo.deserialize(info_json)
            return ml_model_info
        return None

    @classmethod
    def get_all_models(self) -> List[str]:
        models, conversion_ok = QgsProject.instance().readListEntry(self.SCOPE, self.ALL_MODELS_KEY)
        if conversion_ok:
            return models
        return []

    @classmethod
    def get_model_info_all(self) -> Dict[str, MLModelInfo]:
        models = self.get_all_models()
        infos = {}
        for model in models:
            info = self.get_model_info(model)
            infos[model] = info
        return infos

    def save_model_info(self, info: MLModelInfo):
        id = info.model_instance_name
        key = self._get_key(id)
        model_info_json = info.serialize()
        proj = QgsProject.instance()
        proj.writeEntry(self.SCOPE, key, model_info_json)

        models = self.get_all_models()
        models.append(id)
        proj.writeEntry(self.SCOPE, self.ALL_MODELS_KEY, models)

        print(f"Saved model info with key {id}. Info: {info}")

        self.models_updated.emit()

    def remove_model_info(self, id, emit=True):
        key = self._get_key(id)
        proj = QgsProject.instance()
        proj.removeEntry(self.SCOPE, key)

        models = self.get_all_models()
        models.remove(id)
        proj.writeEntry(self.SCOPE, self.ALL_MODELS_KEY, models)

        print(f"Removed model {id}")

        if emit:
            self.models_updated.emit()


    def remove_model_info_all(self):
        models = self.get_all_models()
        for model in models:
            self.remove_model_info(model, emit=False)

        self.models_updated.emit()
