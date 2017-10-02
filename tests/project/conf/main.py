from project.conf import settings

SETTINGS_VAR = 'settings_var'

settings.EXTRA_VAR = 'settings_extra_var'

GLOBAL_VAR3 = 'settings_global_var3'

COMPLEX_VAR = settings.EXTRA_VAR + 'COMPLEX_VAR_VALUE'

INSTALLED_APPS = [
    'project.apps.app1',
    'project.apps.app2',
]

APP2_VAR1 = 'settings_app2_var1'
