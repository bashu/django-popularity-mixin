django-popularity-mixin
=======================

Simple integration between django-cacheback_ and django-hitcount_

Authored by `Basil Shubin <https://github.com/bashu>`_

.. image:: https://img.shields.io/pypi/v/django-popularity-mixin.svg
    :target: https://pypi.python.org/pypi/django-popularity-mixin/

.. image:: https://img.shields.io/pypi/dm/django-popularity-mixin.svg
    :target: https://pypi.python.org/pypi/django-popularity-mixin/

.. image:: https://img.shields.io/github/license/bashu/django-popularity-mixin.svg
    :target: https://pypi.python.org/pypi/django-popularity-mixin/

.. image:: https://img.shields.io/travis/bashu/django-popularity-mixin.svg
    :target: https://travis-ci.org/bashu/django-popularity-mixin/

Requirements
------------

You must have *django-cacheback* and *django-hitcount* both installed and configured, see the
django-cacheback_ and django-hitcount_ documentation for details and setup instructions.


Installation
============

First install the module, preferably in a virtual environment. It can be installed from PyPI:

.. code-block:: shell

    pip install django-popularity-mixin


Setup
=====

Make sure the project is configured for django-cacheback_ and django-hitcount_.

Then add the following settings:

.. code-block:: python

    INSTALLED_APPS += (
        'popularity',
    )

Usage
=====

[TBD]

Please see ``example`` application. This application is used to manually test the functionalities of this package. This also serves as good example...

You need Django 1.8.1 or above to run that. It might run on older versions but that is not tested.

Contributing
------------

If you like this module, forked it, or would like to improve it, please let us know!
Pull requests are welcome too. :-)

.. _django-cacheback: https://github.com/codeinthehole/django-cacheback
.. _django-hitcount: https://github.com/thornomad/django-hitcount
