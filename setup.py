import setuptools

VERSION = '1.1.0'

README = open('README.rst').read()

setuptools.setup(
    name='project-settings',
    version=VERSION,
    author='Shakurov Vadim Vladimirovich',
    author_email='apelsinsd@gmail.com',
    url='https://github.com/NewVadim/project-settings.git',
    license='GNU General Public License v3 (GPLv3)',
    long_description=README,
    description='Project settings in python module.',
    py_modules=['project_settings'],
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
