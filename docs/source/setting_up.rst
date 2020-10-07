Setting Up
==========

WSL 2
^^^^^

Skip this if you are running Linux or if you are using a Cloud IDE like Cloud9 or Gitpod.

Windows Subsystem for Linux. 

Highly recommended as this is an easy way to have Linux running on your windows 10 PC.

See `Windows Subsystem for Linux Installation Guide for Windows 10 <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`_

AWS Code Commit (Git)
---------------------

Skip if you are using Cloud9.

Ensure Git is installed. `Dowload Git <https://git-scm.com/downloads>`_

Setup AWS credential helper:

.. code-block:: console

    git config --global credential.helper '!aws codecommit credential-helper $@'
    git config --global credential.UseHttpPath true

The Git credential helper writes the following value to ``~/.gitconfig``:

.. code-block:: console

    [credential]    
        helper = !aws codecommit credential-helper $@
        UseHttpPath = true

See `AWS Docs <https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-https-unixes.html>`_ for more detail.

Clone the repo
^^^^^^^^^^^^^^

.. code-block:: console

    git clone https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/emagine-epython


Setup your Python environment
-----------------------------

Python
^^^^^^

On CentOS or AWS EC2/Cloud9:

Find source from https://www.python.org/downloads/source/

.. code-block:: console

    wget https://www.python.org/ftp/python/3.8.6/Python-3.8.6.tgz
    cd Python-3.8.6
    sudo ./configure --enable-optimizations
    sudo make altinstall


On Ubuntu or WSL:

.. code-block:: console

    sudo apt update && upgrade
    sudo apt install python3 python3-pip ipython3

On Windows:

`Download <https://www.python.org/downloads/release/python-385/>`_ the installer.

virtualenvwrapper
^^^^^^^^^^^^^^^^^

See `Instructions <https://virtualenvwrapper.readthedocs.io/en/latest/>`_ for installation:


Create a virtual environment.

.. code-block:: console

    mkvirtualenv epython

From now on each time you want to work on the your project you would do

.. code-block:: console

    workon epython

You could also switch to your other project using workon.

cd into your repository:

.. code-block:: console

    cd emagine-epython

Add path to virtual env and set project:

.. code-block:: console

    add2virtualenv $(pwd)
    setvirtualenvproject emagine-epython $(pwd)

Installing Libraries
^^^^^^^^^^^^^^^^^^^^

Upgrade pip

.. code-block:: console

    pip install -U pip

Install requirements:

.. code-block:: console

    pip install -r requirements.txt 

IDE
---

:ref:`VSCode`

Document Building
-----------------

In order to build Jupyter notebook into sphinx we would need to install ``pandoc``

.. code-block:: console

    sudo apt-get install texlive texlive-latex-extra pandoc