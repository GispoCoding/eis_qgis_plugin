from typing import Literal, Optional

from qgis.gui import Qgis, QgsMessageBar


class EISMessageManager:

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(EISMessageManager, cls).__new__(cls)
        return cls.instance


    def set_message_bar(self, message_bar: QgsMessageBar):
        self.message_bar = message_bar


    def show_message(
        self,
        text: str,
        level: Literal["success", "info", "warning", "error"] = "info", 
        duration: Optional[int] = None
    ):
        if not self.message_bar:
            raise ValueError("Message bar not set for MessageHandlerSingleton.")

        if not duration:
            duration = -1

        if level == "success":
            self.message_bar.pushMessage("Success", text, Qgis.MessageLevel.Success, duration)
        elif level == "info":
            self.message_bar.pushMessage("Info", text, Qgis.MessageLevel.Info, duration)
        elif level == "warning":
            self.message_bar.pushMessage("Warning", text, Qgis.MessageLevel.Warning, duration)
        elif level == "error":
            self.message_bar.pushMessage("Error", text, Qgis.MessageLevel.Critical, duration)
