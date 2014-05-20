Django Multilingual Survey
============

Survey app that allows questions and answers to be created in several languages.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-multilingual-survey

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/bitmazk/django-multilingual-survey.git#egg=multilingual_survey

TODO: Describe further installation steps (edit / remove the examples below):

Add ``multilingual_survey`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'multilingual_survey',
    )

Add the ``multilingual_survey`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^survey/', include('multilingual_survey.urls')),
    )

Before your tags/filters are available in your templates, load them by using

.. code-block:: html

	{% load multilingual_survey_tags %}


Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate multilingual_survey


Usage
-----

TODO: Describe usage or point to docs. Also describe available settings and
templatetags.


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 django-multilingual-survey
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch
