import os
import setuptools

VERSION = '0.0.1'

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setuptools.setup(
    name='site-settings',
    version=VERSION,
    author='Shakurov Vadim Vladimirovich',
    author_email='apelsinsd@gmail.com',
    url='https://github.com/newvadim/site-settings',
    long_description=README,
    description='Site settings.',
    py_modules=['site_settings'],
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
