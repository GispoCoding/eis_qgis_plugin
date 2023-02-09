# EIS QGIS plugin
Introduction
EIS (Exploration Information Systems) QGIS plugin will serve as a graphical user interface for the EIS Toolkit.

EIS QGIS plugin is a part of the EIS Horizon EU project, which seeks to implement a modern and comprehensive collection of digital mineral exploration tools. EIS Toolkit will be implemented as a Python library, and EIS QGIS plugin as a QGIS plugin written in Python. EIS QGIS plugin consists of two main parts: EIS Wizard, a collection of workflows and supplementary tools, and EIS Processing, a collection of EIS Toolkit algorithms available in the QGIS processing toolbox and in the QGIS graphical modeler.

Implementation of EIS Wizard
Since EIS Toolkit utilizes multiple other Python libraries and using external libraries in a QGIS plugin is in many cases difficult or impossible, EIS Toolkit must run outside QGIS. The current implementation plan is to execute EIS Toolkit as an external Python program. This is accomplished by using a Python library called subprocess that can be directed to call a virtual environment Python with EIS Toolkit installation. Communication between EIS Wizard and EIS Toolkit will be handled via stdin/stdout. Below are some diagrams of the initial architechture plans.

![concept_diagram_v0 3](https://user-images.githubusercontent.com/113038549/217557033-6d447f46-27fa-4412-92d7-c2df88c8457b.png)


![process_diagram_v0 1](https://user-images.githubusercontent.com/113038549/217557133-3da8d5a8-515d-4b7a-bef4-98aacc2e5da7.png)

![plugin_architecture_v0 2](https://user-images.githubusercontent.com/113038549/217557250-0631334d-47ea-4c0b-8886-0921d84d066c.png)

## Development

Refer to [development](docs/development.md) for developing this QGIS3 plugin.

## License
This plugin is licenced with[GNU General Public License, version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

See [LICENSE](LICENSE) for more information.
