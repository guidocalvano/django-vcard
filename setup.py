import distribute_setup
distribute_setup.use_setuptools('0.6.10')

from setuptools import setup, find_packages

try:
    README = open('README.rst').read()
except:
    README = None

try:
    REQUIREMENTS = open('requirements.txt').read()
except:
    REQUIREMENTS = None

setup(
    name = 'django-vcard',
    version = "0.1",
    description = 'Django Model for storing, importing and exporting vCards',
    long_description = README,
    install_requires=REQUIREMENTS,
    author = 'Guido Sales Calvano',
    author_email = 'guidocalvano@yahoo.nl',
    url = 'http://github.com/guidocalvano/django-vcard',
    packages = find_packages(),
    include_package_data = True,
    classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                    # 'License :: OSI Approved :: GNU Affero General Public License v3',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
)
