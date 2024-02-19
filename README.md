<!-- logo -->
<p align="center">
  <img src="https://github.com/GispoCoding/eis_qgis_plugin/assets/113038549/6792ed06-f1f1-4a69-b9f6-1ca78eaeff4a" align="center"/>
</p>

<h1 align="center">EIS QGIS Plugin</h2>
<p align="center">QGIS plugin for mineral prospectivity mapping</p>

<!-- badges -->
<p align="center">
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json"
  /></a>
  <a href="https://github.com/GispoCoding/eis_qgis_plugin/actions/workflows/code-style.ym">
    <img src="https://github.com/GispoCoding/eis_qgis_plugin/actions/workflows/code-style.yml/badge.svg?branch=master"
  /></a>
  <a href="https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html">
    <img src="https://img.shields.io/badge/License-GPL_v2-blue.svg"
  /></a>
</p>

<!-- links to sections / TOC -->
<p align="center">
  <a href="#getting-started">Getting started</a>
  ·
  <a href="#getting-started">Usage</a>
  ·
  <a href="#getting-started">Roadmap</a>
  ·
  <a href="#getting-started">Contributing</a>
  ·
  <a href="#getting-started">License</a>
</p>


## Introduction

EIS (_Exploration Information Systems_) QGIS Plugin is a tool with graphical user interface for prospectivity mapping of critical raw materials.

EIS QGIS Plugin is a product of the EIS Horizon EU project, which seeks to implement a modern and comprehensive collection of digital mineral exploration tools. EIS QGIS Plugin consists of two main components:
- EIS Wizard, a comprehensive GUI plugin with guided processes and workflows for mineral prospectivity mapping
- EIS Processing Algorithms, the individual tools and algorithms available in QGIS Processing Toolbox

> [!IMPORTANT]  
> EIS QGIS Plugin is still in active development! See [roadmap](#roadmap) for more details.


## Getting started
To use all features of EIS QGIS Plugin, you need to install both EIS QGIS Plugin and [EIS Toolkit](https://github.com/GispoCoding/eis_toolkit), the EIS computational backend. EIS Toolkit is separate from EIS QGIS Plugin to enable using large and complicated environment with machine learning and other heavy libraries. Currently, EIS Toolkit needs to be installed separately, but at a later stage EIS QGIS Plugin will incorporate EIS Toolkit installer.

### Prerequisites
- QGIS 3.X

### Installation
1. Download the latest release ZIP from GitHub in the [Releases](https://github.com/GispoCoding/eis_qgis_plugin/releases) page.
2. In QGIS, open the **Plugins** menu and select **Manage and Install Plugins**.
3. Choose **Install from ZIP** in the window that opens and find the ZIP file you just downloaded. Press **Install Plugin**.
![image](https://github.com/GispoCoding/eis_qgis_plugin/assets/113038549/cd83dfed-a0f5-4eab-b4f1-ace8d1d88713)

If you get a success message from the installer, you have now succesfully installed EIS QGIS Plugin!
![Screenshot from 2024-02-19 10-40-36](https://github.com/GispoCoding/eis_qgis_plugin/assets/113038549/42f20d3e-a8ab-48d5-a9e3-4ddb4bdb2da3)

Next, you need to define for EIS QGIS Plugin where you have installed EIS Toolkit. If you haven't installed EIS Toolkit yet, do that next. Installation instructions can be found in [EIS Toolkit GitHub](https://github.com/GispoCoding/eis_toolkit).


### Toolkit configuration
After you have EIS Toolkit installed in a Python virtual environment, you need to specify the installation environment to EIS QGIS Plugin. To do that, open EIS Wizard by clicking the EIS icon in the Plugins Toolbar.

![Screenshot from 2024-02-19 10-40-53](https://github.com/GispoCoding/eis_qgis_plugin/assets/113038549/5075a261-4e55-4b1a-88fe-5b25ab11568d)

In EIS Wizard, choose **Settings** page in the the menu. You can specify either a Python virtual environment with EIS Toolkit installation or a Docker image with EIS Toolkit. After you have set the required fields, you can click **Verify** to check if your configuration is OK.

![image](https://github.com/GispoCoding/eis_qgis_plugin/assets/113038549/e3c70178-fa2e-48a0-ab0b-84e1dbac2d0e)

> [!WARNING]  
> Docker setup is still actively being developed and tested!


## Usage

### EIS Wizard
To launch EIS Wizard, simply click the EIS icon in the Plugins Toolbar. ![Screenshot from 2024-02-19 10-40-53](https://github.com/GispoCoding/eis_qgis_plugin/assets/113038549/5075a261-4e55-4b1a-88fe-5b25ab11568d)

EIS Wizard is divided into different parts each with their own functionality.

- **Mineral system proxies**: This page let's the user to choose their mineral system and study scale (custom option possible). A list of mineral deposit proxies is presented based on the selections and the user can process their raw data to produce a set of the proxies. The produced proxy data can be used for modeling later.
- **EDA (Explorative Data Analysis)**: In EDA page, the user can produce basic exploratory plots, calculate statistics and use various exploratory methods.
- **Modeling**: The Modeling page facilitates model specific data preparation and running models. For machine learning models, training, application and testing are available separately.
- **Settings**: In Settings page, users can customize the behaviour of EIS Wizard and define the environment with EIS Toolkit installation.
- **About**: The About page has information about EIS QGIS Plugin and EIS project.

> [!NOTE]
> A more detailed user guide will be created later.


### EIS Processing
EIS Processing Algorithms allow using all EIS tools separately and freely. They can be used in combination with EIS Wizard to increase flexibility, or exclusively for those that don't want the guidance of EIS Wizard. If you don't have Processing Toolbox open in QGIS, it can opened by clicking **Processing** and selecting **Toolbox** (or with `CTRL+ALT+T` shortcut) To find EIS Processing Algorithms in Processing Toolbox, you can look for the **EIS** entry in the list or use the search bar.

![image](https://github.com/GispoCoding/eis_qgis_plugin/assets/113038549/0e1e8b63-594e-4061-b0b5-b89ccb9bb6b5)

EIS Processing Algorithms can be launched by double-clicking an algorithm. In the opened window, parameters can be set and description of the algorithm read. QGIS Processing algorithms are fairly intuitive to use, but in case you are new to them, you can refer to various online guides.

![image](https://github.com/GispoCoding/eis_qgis_plugin/assets/113038549/6eabe812-5360-406b-a9ff-150e5a09f44e)


> [!TIP]
> EIS Processing Algorithms, like all algorithms in QGIS Processing Toolbox, can be used to create and save custom workflows in QGIS Model Designer. 


## Roadmap
- Beta release in April 2024.


## Contributing
EIS QGIS Plugin (and EIS Toolkit) are still in activate development by the core team, but feel free join and contribute in any way you like!
- Ideas for new fetures are welcome, even if we have a vision of the final version and its extent in our mind
- Initial testing and bug hunting are helpful
- If you wish to contribute by developing the plugin, read the CONTRIBUTING.MD for instructions


## License
Licensed under GPL 2 or later.
