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


# Introduction

EIS (Exploration Information Systems) QGIS Plugin is a tool with graphical user interface for prospectivity mapping of critical raw materials.

EIS QGIS Plugin is a product of the EIS Horizon EU project, which seeks to implement a modern and comprehensive collection of digital mineral exploration tools. EIS QGIS Plugin consists of two main components: EIS Wizard, collection of guided workflows for mineral prospectivity mapping, and EIS Processing Algorithms. As a byproduct, EIS Processing Algorithms offer users the option to create their custom models and workflows in QGIS Model Builder using the inidividual algorithms.

EIS QGIS Plugin uses [EIS Toolkit](https://github.com/GispoCoding/eis_toolkit) as its computational backend.

> [!NOTE]  
> EIS QGIS Plugin is still in active development. See [roadmap](#roadmap) for more details.


## Getting started
TODO


### Prerequisites
- QGIS

### Installation
- Either:
  - Download relase ZIP from GitHub
  - Download from QGIS repo
- Install EIS Toolkit
- Configure install location / environment 


## Usage

### EIS Wizard
- Click EIS icon in plugins navbar (screenshot here)
- Make sure EIS Toolkit is configured
- Start working!
- More info somewhere?


### EIS Processing
- You can use processing algorithms individually for maximum flexibility
- Can leverage QGIS Model builder for custom workflows 


### EIS Wizard design
The objective of EIS Wizard is to provide guidance and a convenient interface to use EIS Processing Algorithms in approriate ways. Since EIS Processing Algorithms already implement handy and concise interfaces for the tools, in some cases EIS Wizard will forward the user to run some processing algorithm, and in other cases another customized interface is created for the task.

EIS Wizard will have at least the following pages:

- **Mineral system proxies**: This page let's the user to choose their mineral system and study scale (custom option possible). A list of mineral deposit proxies is presented based on the selections and the user can process their raw data to produce a set of the proxies.
- **EDA (Explorative Data Analysis)**: In EDA page, the user can produce basic exploratory plots, calculate statistics and use various exploratory methods.
- **Modeling**: The Modeling page facilitates model specific data preparation and running models. For machine learning models, training, application and testing are available separately.
- **Settings**: In Settings page, users can customize the behaviour of EIS Wizard and define the environment with EIS Toolkit installation
- **About**: The About page has information about EIS QGIS Plugin and EIS project.

## Roadmap
- Beta release in April 2024.
- v1 release in TBD


## License
Licensed under GPL 2 or later.
