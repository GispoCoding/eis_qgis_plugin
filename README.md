# EIS QGIS plugin
## Introduction
EIS (Exploration Information Systems) QGIS Plugin will serve as a graphical user interface for the EIS Toolkit.

EIS QGIS plugin is a part of the EIS Horizon EU project, which seeks to implement a modern and comprehensive collection of digital mineral exploration tools. EIS Toolkit will be implemented as a Python library, and EIS QGIS Plugin as a QGIS plugin written in Python. EIS QGIS Plugin consists of two main components: EIS Wizard, a collection of guided workflows and supplementary tools, and EIS Processing Algorithms, the EIS Toolkit algorithms made available in the QGIS processing toolbox. As a byproduct of implementing EIS Processing Algorithms, users will be able to create their custom models in QGIS Model Builder using the contents of EIS Toolkit.  

## EIS QGIS Plugin - EIS Toolkit architecture
Since EIS Toolkit utilizes multiple other Python libraries and using external libraries in a QGIS plugin is in many cases difficult or impossible, EIS Toolkit runs outside of QGIS. The EIS Processing Algorithms call EIS Toolkit via command line and EIS Wizard will call/guide the user in using EIS Processing Algorithms. When running EIS QGIS Plugin for the first time, the user will need to specify their EIS Toolkit installation location.

![EIS_architecture_0 6](https://user-images.githubusercontent.com/113038549/228445620-77a2a8b3-3b24-4109-8c3a-2d8f9d59ff2f.png)


## EIS Wizard UI design
The objective of EIS Wizard is to provide guidance and a convenient interface to use EIS Processing Algorithms in approriate ways. Because EIS Processing Algorithms implement specific user interfaces for each tool, the aim is to utilize these already defined UIs as much as possible. In practice, this means that EIS Wizard will have links/buttons that open EIS Processing Algorithms.

The current plan is that EIS Wizard will have the following dialogs:
- Preprocess data (for each mineral system)
- Prepare proxy data (from preprocess, for each type of proxy)
- Explore data
- Model (either as one window, or as a "mini wizard" with phases such as start, model, validate)
- Settings



## Development

Refer to [development](docs/development.md) for developing this QGIS3 plugin.

## License
This plugin is licenced with[GNU General Public License, version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

See [LICENSE](LICENSE) for more information.
