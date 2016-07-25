import os
import importlib
from collections import OrderedDict

__author__ = 'vadim'

BASE_SETTINGS_NAME = os.environ.get(
    'BASE_SETTINGS_NAME',
    'SITE'
)
GLOBAL_SETTINGS_MODULE_NAME = os.environ.get(
    'GLOBAL_SETTINGS_MODULE_NAME',
    '{}_GLOBAL_SETTINGS_MODULE'.format(BASE_SETTINGS_NAME)
)
SITE_SETTINGS_MODULE_NAME = os.environ.get(
    'SITE_SETTINGS_MODULE_NAME',
    '{}_SETTINGS_MODULE'.format(BASE_SETTINGS_NAME)
)


class BaseSettings:
    settings_attrs = ['settings']

    def __init__(self):
        self.settings = {}

    def __getattr__(self, item):
        try:
            value = self.settings[item]
        except KeyError:
            raise AttributeError('Setting module {module} has not attribute {attr}'.format(
                module=self.module, attr=item
            ))

        return value

    def __getattribute__(self, item):
        if item == '__dict__' or item == '__class__':
            item = 'settings'

        return super(BaseSettings, self).__getattribute__(item)

    def __setattr__(self, key, value):
        if key in self.settings_attrs:
            super(BaseSettings, self).__setattr__(key, value)
        else:
            self.settings[key] = value

    def update(self, kwargs):
        self.settings.update(kwargs)


class Settings(BaseSettings):
    settings_attrs = ['module', 'settings']

    def __init__(self):
        super(Settings, self).__init__()
        global_settings_module = os.environ.get(GLOBAL_SETTINGS_MODULE_NAME)
        settings_module = os.environ.get(SITE_SETTINGS_MODULE_NAME)
        if not settings_module and not global_settings_module:
            raise EnvironmentError('SETTINGS_MODULE not found!')

        settings_module = importlib.import_module(settings_module)
        global_settings_module = importlib.import_module(global_settings_module)

        self.settings.update({
            **{name: getattr(settings_module, name) for name in dir(global_settings_module) if name.upper()},
            **{name: getattr(settings_module, name) for name in dir(settings_module) if name.upper()},
            **{key: value for key, value in os.environ.items() if key.upper() and key.startswith(BASE_SETTINGS_NAME)},
        })


class AppSettings(BaseSettings):
    def __init__(self, label):
        self.label = label
        self.app = None
        self.app_module = None
        self.ready = False
        super(AppSettings, self).__init__()

        upper_label = label.upper()
        self.settings.update({
            **{key: value for key, value in self.settings.items() if key.upper() and key.startswith(upper_label)},
            **{key: value for key, value in os.environ.items() if key.upper() and key.startswith(upper_label)},
        })

    def build(self):
        self.app_module = importlib.import_module(self.app)
        self.ready = True

    def ready(self):
        pass


class AppsSettings:
    def __init__(self):
        self.ready = False
        self.apps = OrderedDict()
        for app in settings.INSTALED_APPS:
            app_label = app.split('.')[-1]
            cls_name = '{app_label}Settings'.format(
                app_label=''.join(map(lambda x: x.capitalize(), app_label.split('_'))))

            settings_module = importlib.import_module('{}.settings'.format(app))
            self.apps[app_label] = getattr(settings_module, cls_name)(label=app_label)

    def build(self):
        for app_settings in self.apps.values():
            app_settings.build()

        self.ready = True

        for app_settings in self.apps.values():
            app_settings.ready()


settings = Settings()
apps_settings = AppsSettings()
