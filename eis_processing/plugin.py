# import os

# from qgis.PyQt.QtCore import QCoreApplication, QTranslator
from qgis.core import QgsApplication

from eis_processing.eis_provider import EISProvider

#pluginPath = os.path.dirname(__file__)


class EISProcessingPlugin:

    def __init__(self):
        # locale = QgsApplication.locale()
        # qmPath = '{}/i18n/wbt_for_qgis_{}.qm'.format(pluginPath, locale)

        # if os.path.exists(qmPath):
        #     self.translator = QTranslator()
        #     self.translator.load(qmPath)
        #     QCoreApplication.installTranslator(self.translator)

        self.provider = EISProvider()

    def initProcessing(self):
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
