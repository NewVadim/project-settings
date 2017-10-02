import os
import sys
import unittest

import logging.config


class SiteSettingsTests(unittest.TestCase):
    def setUp(self):
        from project.conf import settings, apps_settings

        os.environ['PROJECT_SETTINGS_MODULE'] = 'project.conf.main'
        os.environ['PROJECT_GLOBAL_SETTINGS_MODULE'] = 'project.conf.global'
        os.environ['PROJECT_GLOBAL_VAR2'] = 'global_var2_env'

        settings.reconfigure()
        apps_settings.reconfigure()

        self.settings = settings
        self.apps_settings = apps_settings

    def tearDown(self):
        sys.modules.pop('project.conf.main')
        sys.modules.pop('project.conf.global')

        os.environ.pop('PROJECT_SETTINGS_MODULE', None)
        os.environ.pop('PROJECT_GLOBAL_SETTINGS_MODULE', None)
        os.environ.pop('PROJECT_GLOBAL_VAR2', None)

    def test_vars(self):
        self.assertTrue(dir(self.settings))

        self.assertIn('SETTINGS_VAR', self.settings)
        self.assertEqual(self.settings.SETTINGS_VAR, 'settings_var')

        self.assertIn('GLOBAL_VAR1', self.settings)
        self.assertEqual(self.settings.GLOBAL_VAR1, 'global_var1')

        self.assertIn('GLOBAL_VAR2', self.settings)
        self.assertEqual(self.settings.GLOBAL_VAR2, 'global_var2_env')

        self.assertIn('GLOBAL_VAR3', self.settings)
        self.assertEqual(self.settings.GLOBAL_VAR3, 'settings_global_var3')

        self.assertIn('EXTRA_VAR', self.settings)
        self.assertEqual(self.settings.EXTRA_VAR, 'settings_extra_var')

        self.assertIn('COMPLEX_VAR', self.settings)
        self.assertEqual(self.settings.COMPLEX_VAR, 'settings_extra_var' + 'COMPLEX_VAR_VALUE')

    def test_invalid_var(self):
        error = None
        try:
            self.settings.INVALID_VAR
        except AttributeError as exc:
            error = exc

        self.assertTrue(error)

    def test_as_dict(self):
        settings = dict(**self.settings)

        self.assertIn('SETTINGS_VAR', self.settings)
        self.assertEqual(settings['SETTINGS_VAR'], 'settings_var')

    def test_len(self):
        self.assertTrue(len(self.settings))

    def test_items(self):
        settings = dict(self.settings.items())

        self.assertIn('SETTINGS_VAR', self.settings)
        self.assertEqual(settings['SETTINGS_VAR'], 'settings_var')

    def test_update(self):
        self.settings.update({'SETTINGS_VAR': 'update_settings_var'})

        self.assertIn('SETTINGS_VAR', self.settings)
        self.assertEqual(self.settings.SETTINGS_VAR, 'update_settings_var')


class InvalidSettingsModuleTest(unittest.TestCase):
    def setUp(self):
        os.environ['PROJECT_SETTINGS_MODULE'] = 'invalid.path.settings'

    def tearDown(self):
        os.environ.pop('PROJECT_SETTINGS_MODULE', None)

    def test(self):
        from project.conf import settings

        error = None
        try:
            settings.configure()
        except ImportError as exc:
            error = exc

        self.assertTrue(error)


class EmptySettingsModuleTest(unittest.TestCase):
    def setUp(self):
        os.environ.pop('PROJECT_SETTINGS_MODULE', None)
        os.environ.pop('PROJECT_GLOBAL_SETTINGS_MODULE', None)

    def test(self):
        from project.conf import settings

        error = None
        try:
            settings.configure()
        except EnvironmentError as exc:
            error = exc

        self.assertTrue(error)


class AppsSettingsTests(unittest.TestCase):
    def setUp(self):
        from project.conf import settings, apps_settings

        os.environ['PROJECT_SETTINGS_MODULE'] = 'project.conf.main'
        os.environ['APP1_VAR2'] = 'app1_var2_env'

        settings.reconfigure()
        apps_settings.reconfigure()

        self.settings = settings
        self.apps_settings = apps_settings

    def tearDown(self):
        sys.modules.pop('project.conf.main')

        os.environ.pop('PROJECT_SETTINGS_MODULE', None)
        os.environ.pop('APP1_VAR2', None)

    def test_app_settings(self):
        self.assertEqual(len(self.apps_settings.apps), 2)

        self.assertIn('VAR1', self.apps_settings['app1'])
        self.assertEqual('app1_var1', self.apps_settings.app1.VAR1)
        self.assertEqual('app1_var1', self.apps_settings['app1'].VAR1)

        self.assertIn('VAR2', self.apps_settings['app1'])
        self.assertEqual('app1_var2_env', self.apps_settings['app1']['VAR2'])

        self.assertIn('READY_VAR', self.settings)
        self.assertEqual('APP1_READY_VAR', self.settings['READY_VAR'])
        self.assertEqual('APP1_READY_VAR', self.settings.READY_VAR)

        self.assertIn('VAR1', self.apps_settings['app2'])

    def test_app_settings_invalid(self):
        self.assertNotIn('SETTINGS_VAR', self.apps_settings['app1'])
        self.assertNotIn('SETTINGS_VAR', self.apps_settings['app2'])

        error = None
        try:
            self.apps_settings.app1.SETTINGS_VAR
        except AttributeError as exc:
            error = exc

        self.assertTrue(error)
