import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-popularity',
    version='0.1',
    packages=['popularity'],
    include_package_data=True,
    license='GNU Library or LGPL License',
    description='Put short description here...',
    long_description=README,
    author='Basil Shubin',
    dependency_links = [
        'http://github.com/bashu/django-hitcount/tarball/master#egg=django-hitcount-ng',
    ],
    install_requires=[
        'celery',
        'django-celery',
        'django-cacheback',
        'django-hitcount-ng',
    ],
    author_email='basil.shubin@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    zip_safe=False,
)
