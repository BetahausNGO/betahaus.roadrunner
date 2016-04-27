Betahaus Roadrunner
===================

Basic installation instructions

Install python + virtualenv
Create a local virtualenv and activate local python:

.. code::

   >>> virtualenv .
   >>> source bin/activate

Prepare buildout

.. code::

   >>> python bootstrap-buildout.py

Run buildout

.. code::

   >>> buildout

Start the server

.. code::

   >>> pserve etc/development.ini
