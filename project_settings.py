# coding=utf-8

import os
import importlib

from collections import OrderedDict
from copy import deepcopy


__author__ = 'vadim'


class BaseSettings(object):
    __slots__ = ('name', 'settings', 'configured')

    def __init__(self):
        self.settings = {}
        self.configured = False

    def __dir__(self):
        return list(self.settings)

    def __getattr__(self, item):
        try:
            value = self.settings[item]
        except KeyError:
            raise AttributeError(
                'Setting `{name}` has not attribute {attr}'.format(
                    name=self.get_name(), attr=item
                ))

        return value

    def __setattr__(self, key, value):
        if key in self.__slots__:
            super(BaseSettings, self).__setattr__(key, value)
        else:
            if not self.configured and key in self.settings:
                return

            self.settings[key] = value

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __len__(self):
        return len(self.settings)

    def __iter__(self):
        return iter(self.settings)

    def keys(self):
        return list(self.settings)

    def items(self):
        for key, value in self.settings.items():
            yield key, value

    def get_name(self):
        raise NotImplemented()

    def configure(self):
        raise NotImplemented()

    def reconfigure(self):
        self.configured = False
        self.configure()

    def update(self, kwargs):
        self.settings.update(kwargs)


class Settings(BaseSettings):
    __slots__ = ('name', 'settings', 'configured')

    def get_name(self):
        return 'settings'

    def configure(self, base_settings_name=None, project_settings_module=None, global_settings_module=None):
        if not base_settings_name:
            base_settings_name = os.environ.get(
                'BASE_SETTINGS_NAME',
                'PROJECT'
            )

        if not project_settings_module:
            project_settings_module_name = os.environ.get(
                'PROJECT_SETTINGS_MODULE_NAME',
                '{}_SETTINGS_MODULE'.format(base_settings_name)
            )
            project_settings_module = os.environ.get(project_settings_module_name)

        if not global_settings_module:
            global_settings_module_name = os.environ.get(
                'GLOBAL_SETTINGS_MODULE_NAME',
                '{}_GLOBAL_SETTINGS_MODULE'.format(base_settings_name)
            )
            global_settings_module = os.environ.get(global_settings_module_name)

        if not project_settings_module and not global_settings_module:
            raise EnvironmentError('SETTINGS_MODULE not specified!')

        # Настройки из переменных окружения, если они начинаются на базовое имя
        prefix = '{}_'.format(base_settings_name)
        self.settings = {
            key.replace(prefix, ''): value
            for key, value in os.environ.items()
            if key.isupper() and key.startswith(prefix)
        }

        # Настройки из модулей
        for settings_module in filter(None, [project_settings_module, global_settings_module]):
            try:
                settings_module = importlib.import_module(settings_module)
            except ImportError:
                raise ImportError('Invalid settings module.')

            for name in dir(settings_module):
                if not name.isupper():
                    continue

                setattr(self, name, deepcopy(getattr(settings_module, name)))

        self.INSTALLED_APPS = []

        self.configured = True


class AppSettings(BaseSettings):
    __slots__ = (
        'settings', 'configured',
        'project_settings', 'settings_module',
        'label', 'app', 'app_module', 'is_ready'
    )

    def __init__(self, project_settings, settings_module, label, app):
        self.project_settings = project_settings
        self.settings_module = settings_module
        self.label = label
        self.app = app
        self.app_module = None
        self.is_ready = False
        super(AppSettings, self).__init__()

    def get_name(self):
        return '{} settings'.format(self.label)

    def configure(self):
        upper_label = self.label.upper()
        prefix = '{}_'.format(upper_label)

        # Настроики для приложения из переменных окружения, если они начинаются на имя приложения
        self.settings = {
            key.replace(prefix, ''): value
            for key, value in os.environ.items()
            if key.upper() and key.startswith(prefix)
        }

        # Настроики для приложения из основных настроек, если они начинаются на имя приложения
        for key, value in self.project_settings.items():
            if not key.isupper() or not key.startswith(prefix):
                continue

            setattr(self, key.replace(prefix, ''), value)

        # Настройка из модуля
        for name in dir(self.settings_module):
            if not name.isupper():
                continue

            setattr(self, name, deepcopy(getattr(self.settings_module, name)))

        self.configured = True

    def build(self):
        self.app_module = importlib.import_module(self.app)
        self.is_ready = True

    def ready(self):
        pass


class AppsSettings:
    __slots__ = (
        'project_settings', 'configured',
        'is_ready', 'apps'
    )

    def __init__(self, project_settings):
        self.is_ready = False
        self.apps = OrderedDict()
        self.project_settings = project_settings
        self.configured = False

    def __getitem__(self, item):
        return self.apps[item]

    def __getattr__(self, item):
        return self.apps[item]

    def reconfigure(self):
        self.configured = False
        self.configure()

    def configure(self):
        for app in self.project_settings.INSTALLED_APPS:
            app_label = app.split('.')[-1]
            cls_name = '{app_label}Settings'.format(
                app_label=''.join(map(lambda x: x.capitalize(), app_label.split('_'))))

            settings_module = importlib.import_module('{}.settings'.format(app))

            cls = getattr(settings_module, cls_name)
            config = cls(
                project_settings=self.project_settings, settings_module=settings_module,
                label=app_label, app=app
            )
            config.configure()

            self.apps[app_label] = config

        self.build()
        self.configured = True

    def build(self):
        for app_settings in self.apps.values():
            app_settings.build()

        self.is_ready = True

        for app_settings in self.apps.values():
            app_settings.ready()
