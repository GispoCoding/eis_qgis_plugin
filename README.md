# EIS QGIS Plugin
## Introduction
EIS (Exploration Information Systems) QGIS Plugin will serve as a graphical user interface for the EIS Toolkit.

EIS QGIS plugin is a product of the EIS Horizon EU project, which seeks to implement a modern and comprehensive collection of digital mineral exploration tools. EIS QGIS Plugin consists of two main components: EIS Wizard, collection of guided workflows for mineral prospectivity mapping, and EIS Processing Algorithms. As a byproduct, EIS Processing Algorithms offer users the option to create their custom models and workflows in QGIS Model Builder using the inidividual algorithms.

## EIS Toolkit – the EIS QGIS Plugin backend
EIS Processing Algorithms are powered by EIS Toolkit, a Python library for mineral prospectivity mapping. EIS Toolkit is also developed for the EIS project and designed to work smoothly for EIS QGIS Plugin, but also individually for those that prefer scripting and notebooks. For more information about EIS Toolkit, go checkout the repository: https://github.com/GispoCoding/eis_toolkit.

### Plugin-toolkit communication
Since EIS Toolkit utilizes multiple other Python libraries and using external libraries in a QGIS plugin is in many cases difficult or impossible, EIS Toolkit runs outside of QGIS. The EIS Processing Algorithms call EIS Toolkit via command line and EIS Wizard calls EIS Processing Algorithms for individual steps.

## EIS Wizard UI design
The objective of EIS Wizard is to provide guidance and a convenient interface to use EIS Processing Algorithms in approriate ways. Since EIS Processing Algorithms already implement handy and concise interfaces for the tools, in some cases EIS Wizard will forward the user to run some processing algorithm, and in other cases another customized interface is created for the task. 

The current plan is that EIS Wizard will have the following pages:

**Mineral system proxies**

This page let's the user to choose their mineral system and study scale (custom option possible). A list of mineral deposit proxies is presented based on the selections and the user can process their raw data to produce a set of the proxies.

**EDA (Explorative Data Analysis)**

In EDA page, the user can produce basic plots of their data. Other exploratory methods and data inspection is also made available in this page.

**Modeling**

The Modeling page consists of preparing/preprocessing data for modeling, the model creation itself and model validation.

**Settings**

In settings page, users can customize the behaviour of EIS Wizard, for example the install location of EIS Toolkit, default values for some input fields and the UI.

**About**

About page has information about EIS QGIS Plugin and EIS project.


## License
Licensed under the EUPL-1.2 or later.
