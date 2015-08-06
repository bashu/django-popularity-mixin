import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-popularity-mixin',
    version='0.1.5',
    packages=['popularity'],
    include_package_data=True,
    license='LGPLv3 License',
    description='Put short description here...',
    long_description=README,
    author='Basil Shubin',
    install_requires=[
        'django-celery>=3.0,<3.1',
        'django-cacheback>=0.7',
        'django-classy-tags>=0.5',
        'django-hitcount-headless>=0.2',
    ],
    author_email='basil.shubin@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    zip_safe=False,
)
