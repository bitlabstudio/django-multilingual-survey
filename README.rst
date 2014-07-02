.. image:: https://badge.fury.io/py/django-multilingual-survey.svg
    :target: http://badge.fury.io/py/django-multilingual-survey

Django Multilingual Survey
==========================

Survey app that allows questions and answers to be created in several
languages.

Allows users to submit free text in an "other" field, if none of the choices
are sufficient for the user. Users can even submit several custom answers to
a question by submitting several comma separated values.

Admins will get notified if a user submits a custom answer via the "other"
field. They have an admin view that allows to accept, reject or rename the
custom answer.

This ensures that users who submit the same custom answer but with different
spelling (i.e. "Vim" and "VIM") will ultimately get hooked up with the same
unified SurveyAnswer object, which makes the creation of reports much easier
and yields more accurate survey results.

Questions and answers can be provided in several languages using
`django-hvad <https://github.com/kristianoellegaard/django-hvad>`_

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-multilingual-survey

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/bitmazk/django-multilingual-survey.git#egg=multilingual_survey

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
