.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://github.com/cusyio/cusy.restapi.easyform/workflows/ci/badge.svg
    :target: https://github.com/cusyio/cusy.restapi.easyform/actions
    :alt: CI Status

.. image:: https://codecov.io/gh/cusyio/cusy.restapi.easyform/branch/main/graph/badge.svg?token=3JU2SVF5TE
    :target: https://codecov.io/gh/cusyio/cusy.restapi.easyform
    :alt: Coverage Status

.. image:: https://img.shields.io/pypi/v/cusy.restapi.easyform.svg
    :target: https://pypi.python.org/pypi/cusy.restapi.easyform/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/cusy.restapi.easyform.svg
    :target: https://pypi.python.org/pypi/cusy.restapi.easyform
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/cusy.restapi.easyform.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/cusy.restapi.easyform.svg
    :target: https://pypi.python.org/pypi/cusy.restapi.easyform/
    :alt: License


=====================
cusy.restapi.easyform
=====================

EasyForm integration for plone.restapi.

Features
--------

- Get the ``EasyForm`` schema in ``JSON+SCHEMA`` format using the ``@form`` endpoint.
- Post form data to an ``EasyForm`` form using the ``@form`` endpoint.


Installation
------------

Install ``cusy.restapi.easyform`` by adding it to your buildout::

    [buildout]

    ...

    eggs =
        cusy.restapi.easyform


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/cusyio/cusy.restapi.easyform/issues
- Source Code: https://github.com/cusyio/cusy.restapi.easyform


Support
-------

If you are having issues, please let us know by adding a new ticket.


License
-------

The project is licensed under the GPLv2.
