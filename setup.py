import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-popularity-mixin',
    version='0.1.1',
    packages=['popularity'],
    include_package_data=True,
    license='GNU Library or LGPL License',
    description='Put short description here...',
    long_description=README,
    author='Basil Shubin',
    install_requires=[
        'celery==3.0.23',
        'django-celery==3.0.23',
        'django-hitcount==0.2.3a',
        'django-cacheback==0.5',
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
