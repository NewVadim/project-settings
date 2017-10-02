from project_settings import AppSettings


VAR1 = 'app1_var1'
VAR2 = 'app1_var2'


class App1Settings(AppSettings):
    name = 'app1'

    def ready(self):
        from project.conf import settings
        settings.READY_VAR = 'APP1_READY_VAR'
