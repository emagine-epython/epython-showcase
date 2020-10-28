
Developer
=========


.. image::  https://codebuild.eu-west-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiZjNZV3FIMGdZQlU3QVgyUjZKSThKNUdPd2g1dTlVS2RwM0MzeXdKMnM4c2xGT0dLWHdzeFM5YWxnV282Ym9IalltU2VUSWpPYWI4azg0N0FJUXFUQmVnPSIsIml2UGFyYW1ldGVyU3BlYyI6Im5lQmNwVXdQV2thZU8vOHYiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master
    :alt: build-badge

Code Cleanliness
----------------

Please be sure to run ``autopep8`` and ``flake8`` **before** committing.

For autopep8, you could get it to auto format all your code.

.. code-block:: console

    autopep8 -i -r .
    flake8
    
Unittest
--------

Please be sure to add unittest to any changes.
Ensure that all (relevent) unittests passes before you commit.

Run all unittests:

.. code-block:: console

    pytest
    
Test a single module:

.. code-block:: console

    pytest tsdb/tests/test_athena.py 
    
Test a single function:

.. code-block:: console

    pytest tsdb/tests/test_athena.py -k test_wait_for_results_timeout

Documentation
-------------

Building
^^^^^^^^

Create build the very documentation you are looking at now.

.. code-block:: console

    cd ~/environment/emagine-epython/docs
    make html
    
Keep an eye on the output to make sure there are no errors or warnings.

Bad example:


.. code-block:: console

    build succeeded, 1 warning.
    
Good example:

.. code-block:: console

    build succeeded.
    
Preview
^^^^^^^
    
To view it locally. Simply open up
``~/environment/emagine-epython/docs/build/html/index.html``

On Cloud9. Run the below:


.. code-block:: console

    cd ~/environment/emagine-epython/docs/build
    python -m http.server 8080
    
At the menu bar click ``Preview`` then ``Preview Running Application``

Upload
^^^^^^

The auto-build of the documentation isn't there yet. So manually upload with.

While still in the `docs` directory:

.. code-block:: console

    aws s3 sync build/ s3://doc.epythoncloud.io/