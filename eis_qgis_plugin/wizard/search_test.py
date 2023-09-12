from typing import Dict, List, Tuple

from qgis.PyQt.QtWidgets import (
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget
)


class SearchDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        # self.setupUi(self)

        self.main_layout = QVBoxLayout()

        proxies: List[Tuple[str, str]] = [
            ("Major structures", "High"),
            ("Lower order structures", "High"),
            ("Fluid flow and deposition", "Moderate"),
            ("Proxy 4", "Low"),
            ("Something", "Low"),
        ]

        self.proxy_widgets: Dict[str, Tuple[str, QWidget]] = {}
        self.proxy_layout = QGridLayout()

        for i, (proxy, importance) in enumerate(proxies):
            proxy_widget = QWidget()
            proxy_layout = QHBoxLayout()

            proxy_label = QLabel(proxy)
            proxy_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            proxy_layout.addWidget(proxy_label)

            importance_label = QLabel(importance)
            importance_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            proxy_layout.addWidget(importance_label)

            process_button = QPushButton("Process")
            process_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            proxy_layout.addWidget(process_button)

            load_button = QPushButton("Load")
            load_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            proxy_layout.addWidget(load_button)

            proxy_widget.setLayout(proxy_layout)

            self.proxy_widgets[proxy] = (importance, proxy_widget)
            self.proxy_layout.addWidget(proxy_widget, i, 0, 1, 4)

        self.search_bar = QLineEdit()
        self.search_bar.textChanged.connect(self.update_widgets)
        self.main_layout.addWidget(self.search_bar)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.addLayout(self.proxy_layout)
        scroll_layout.addStretch()
        scroll_widget.setLayout(scroll_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        self.main_layout.addWidget(scroll_area)

        self.setLayout(self.main_layout)

    def update_widgets(self, text):
        for proxy, (importance, widget) in self.proxy_widgets.items():
            if text.lower() in proxy.lower() or text.lower() in importance.lower():
                widget.show()
            else:
                widget.hide()
