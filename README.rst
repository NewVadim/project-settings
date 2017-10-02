Site settings
=============

A sample settings for your any project.
The packages allows to keep project settings in a simple python module.
The module path can be specified in environment variables or specified in the method ``configure``.

In addition, environment variables can contain any variables that will not be overwritten by the module.
All variables must begin with the base name of the settings and in the upper case.

A project can have multiple settings modules:

* base - base settings for the project;
* extra - extra variables, for example dev or staging;
* global - global variables, like variables by default.

All variables in all modules should be in upper case.

Extra variables declared in the base settings module as ``settings.EXTRA_VAR = "VAR_VALUE"`` and
use like so ``VAR = settings.EXTRA_VAR.split('_') + ['example']``.
In the extra settings module declared extra value of variables as ``settings.EXTRA_VAR = "EXTRA_VAR_VALUE"``
and last line import base settings module ``from my_project.conf.base import *``.
In result ``assert VAR == ['EXTRA', 'VAR', 'VALUE', 'example']``.

Example
-------

./start.py::

    import os

    if __name__ == '__main__':
        from my_project import main

        os.environ.setdefault("BASE_SETTINGS_NAME", "MY_PROJECT")
        os.environ.setdefault("MY_PROJECT_SETTINGS_MODULE", "my_project.conf.extra")
        os.environ.setdefault("MY_PROJECT_GLOBAL_SETTINGS_MODULE", "my_project.conf.global")

        os.environ["MY_PROJECT_VAR_2"] = "ENV_VAR_2_VALUE"

        main.run()

./my_project/main.py::

    from my_project.conf import settings


    def run():
        settings.configure()

        # your code
        from my_project import code

./my_project/conf/__init__.py::

    from project_settings import Settings, AppsSettings

    settings = Settings()
    apps_settings = AppsSettings()

./my_project/conf/extra.py::

    from my_project.conf import settings

    settings.EXTRA_VAR = "EXTRA_VAR_VALUE"

    from my_project.conf.base import *

./my_project/conf/base.py::

    from my_project.conf import settings

    VAR_1 = "VAR_1_VALUE"
    VAR_2 = "VAR_2_VALUE"
    settings.EXTRA_VAR = "BASE_EXTRA_VAR_VALUE"
    VAR_5 = settings.VAR_4 + "_VAR_5_VALUE"

./my_project/conf/global.py::

    VAR_1 = "GLOBAL_VAR_1_VALUE"
    VAR_2 = "GLOBAL_VAR_2_VALUE"
    VAR_3 = "GLOBAL_VAR_3_VALUE"
    VAR_4 = "GLOBAL_VAR_4_VALUE"

./my_project/code.py::

    from my_project.conf import settings

    assert settings.VAR_1 == "VAR_1_VALUE"
    assert settings.VAR_2 == "ENV_VAR_2_VALUE"
    assert settings.VAR_3 == "GLOBAL_VAR_3_VALUE"
    assert settings.VAR_4 == "EXTRA_VAR_VALUE"
    assert settings.VAR_5 == "EXTRA_VAR_VALUE_VAR_5_VALUE"

After running ``python start.py`` all settings will be generated after executing ``settings.configure()``.
After configuration, you can overwrite the values of variables, for example: `settings.VAR_1 = "NEW_VALUE_VAR_1"`.

Apps settings
-------------
For use in the settings, you must specify a variable with list of applications
`INSTALLED_APPS = ['my_project.apps.app']` and initialize `apps_settings = AppsSettings()`.
Next, you must add the package `my_project.apps.app` module `settings` on the inside.
The module may contain application variables declared in upper case.

./my_project.apps.app.settings.py::

    from project_settings import AppSettings


    VAR1 = 'app_var1'
    VAR2 = 'app_var2'


    class AppSettings(AppSettings):
        name = 'app'

        def ready(self):
            from my_project.conf import settings

            settings.READY_VAR = 'APP_READY_VAR'


Application settings will be available as `apps_settings.app.VAR1`.
Application settings variables can also be declared using the environment variables,
if it starts with the application name at the upper case, for example ``export APP_ENV_VAR=example``.
