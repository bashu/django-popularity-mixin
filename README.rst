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

The ``popularity.views.PopularityMixin`` can be used to do the
business-logic of counting the hits asynchronously by setting
``count_hit`` to ``True``.

.. code-block:: python

    # views.py

    from django.views.generic.detail import DetailView

    from popularity.views import PopularityMixin


    class CustomDetailView(PopularityMixin, DetailView):
        count_hit = True    # set to True if you want it to try and count the hit asynchronously
        template_name = "template.html"
        ...

The ``popularity.viwes.PopularityMixin`` extends Django’s generic
``django.views.generic.detail.DetailView`` and injects an additional
context variable ``hitcount``.

.. code-block:: html+django

    <!-- template.html -->

    {# the primary key for the hitcount object #}
    {{ hitcount.pk }}

    {# the total hits for the object #}
    {{ hitcount.total_hits }}

For a more granular approach to viewing the hits for a related object you can use the ``get_hit_count`` template tag.

.. code-block:: html+django

    {# remember to load the tags first #}
    {% load popularity_tags %}

    {# Return total hits for an object: #}
    {% get_hit_count for [object] %}

    {# Get total hits for an object as a specified variable: #}
    {% get_hit_count for [object] as [var] %}

    {# Get total hits for an object over a certain time period: #}
    {% get_hit_count for [object] within ["days=1,minutes=30"] %}

    {# Get total hits for an object over a certain time period as a variable: #}
    {% get_hit_count for [object] within ["days=1,minutes=30"] as [var] %}

Please see ``example`` application. This application is used to manually test the functionalities of this package. This also serves as good example...

You need Django 1.8.1 or above to run that. It might run on older versions but that is not tested.

Contributing
------------

If you like this module, forked it, or would like to improve it, please let us know!
Pull requests are welcome too. :-)

.. _django-cacheback: https://github.com/codeinthehole/django-cacheback
.. _django-hitcount: https://github.com/thornomad/django-hitcount
