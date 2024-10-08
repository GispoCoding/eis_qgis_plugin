Development of EIS QGIS plugin
===========================

This project uses [qgis_plugin_tools](https://github.com/Gispo/qgis_plugin_tools) submodule. When cloning, remember to use `--recurse-submodules` like so:

`git clone --recurse-submodules https://github.com/GispoCoding/eis_wizard.git`

## Setting up development environment

To get started with the development, follow these steps:

1. Go to the [eis_qgis_plugin](../eis_qgis_plugin) directory with a terminal
1. Create a new Python virtual environment with pre-commit using Python aware of QGIS libraries:
   ```shell
    python build.py venv
    ```
   In Windows it would be best to use python-qgis.bat or python-qgis-ltr.bat:
   ```shell
    C:\OSGeo4W64\bin\python-qgis.bat build.py venv
   ```
1. **Note: This part is  only for developers that are using QGIS < 3.16.8.** If you want to use IDE for development, it is best to start it with the
   following way on Windows:
   ```shell
    :: Check out the arguments with python build.py start_ide -h
    set QGIS_DEV_IDE=<path-to-your-ide.exe>
    set QGIS_DEV_OSGEO4W_ROOT=C:\OSGeo4W64
    set QGIS_DEV_PREFIX_PATH=C:\OSGeo4W64\apps\qgis-ltr
    C:\OSGeo4W64\bin\python-qgis.bat build.py start_ide
    :: If you want to create a bat script for starting the ide, you can do it with:
    C:\OSGeo4W64\bin\python-qgis.bat build.py start_ide --save_to_disk
   ```

Now the development environment should be all-set.

To activate the environment from your current location:
```shell
source ../.venv/bin/activate
```

To deactivate the environment
```shell
deactivate
```

If you want to edit or disable some quite strict pre-commit scripts, edit .pre-commit-config.yaml.
For example to disable typing, remove mypy hook and flake8-annotations from the file.
You can also disable pre-commit for a specific commit like this:
```shell
git commit -m 'message' --no-verify
```


## Developing the plugin

When developing this plugin, it is recommended to use the build.py script to streamline updating the plugin. To transfer modifications in your code directly to QGIS's plugin folder, run:

```shell script
python build.py deploy
```

An important note is that the deployment will target a QGIS profile named specifically as "EIS" (this is defined in the build.py script and can be modified locally). After deploying and reloading the plugin (or restarting QGIS) the plugin will be updated. Deployment script works also when the plugin hasn't been installed before, but in this case it needs to be activated after deploying in the QGIS plugin menu.

You might need to edit [build.py](../eis_qgis_plugin/build.py) to contain working values for *profile*, *lrelease* and *pyrcc*. If you are
running on Windows, make sure the value *QGIS_INSTALLATION_DIR* points to right folder.


## Adding or editing  source files

If you create or edit source files make sure that they contain absolute imports:

```python
from eis_qgis_plugin.eis_processing.eis_provider import EISProvider # Good

from ..processing.eis_provider import EISProvider # Bad
```


## Deployment

Edit [build.py](../eis_wizard/build.py) to contain working values for *profile*, *lrelease* and *pyrcc*. If you are
running on Windows, make sure the value *QGIS_INSTALLATION_DIR* points to right folder

Run the deployment with:

```shell script
python build.py deploy
```

After deploying and restarting QGIS you should see the plugin in the QGIS installed plugins where you have to activate
it.


## Testing

Install python packages listed in [requirements-dev.txt](../requirements-dev.txt) to the virtual environment
and run tests with:

```shell script
pytest
```

### Github Release

Follow these steps to create a release

* Add changelog information to [CHANGELOG.md](../CHANGELOG.md) using this
  [format](https://raw.githubusercontent.com/opengisch/qgis-plugin-ci/master/CHANGELOG.md)
* Make a new commit. (`git add -A && git commit -m "Release 0.1.0"`)
* Create new tag for it (`git tag -a 0.1.0 -m "Version 0.1.0"`)
* Push tag to Github using `git push --follow-tags`
* Create Github release
* [qgis-plugin-ci](https://github.com/opengisch/qgis-plugin-ci) adds release zip automatically as an asset

Modify [release](../.github/workflows/release.yml) workflow according to its comments if you want to upload the
plugin to QGIS plugin repository.

### Local release

For local release install [qgis-plugin-ci](https://github.com/opengisch/qgis-plugin-ci) (possibly to different venv
to avoid Qt related problems on some environments) and follow these steps:
```shell
cd eis_wizard
qgis-plugin-ci package --disable-submodule-update 0.1.0
```
