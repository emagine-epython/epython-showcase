.. _VSCode:

VSCode
======

WSL
---

Install the extension `Remote - WSL`. You would then see a WSL button at the bottom of the IDE,
click on that to launch a new Window. Now open folder and go to the folder where the project
is checked out. See `here <https://code.visualstudio.com/docs/remote/wsl>`_ more detail.

Select Interpreter
------------------

``Ctrl-P`` to go to pallet. Enter ``Python: Select Interpreter``

Enter the path to your python interpreter replacing ``$WORKON_HOME`` with the actual path.

.. code-block:: console

    $WORKON_HOME/epython/bin/python

Recommended Extensions
----------------------

`GitLens <https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens>`_

VSCode already provides a solid Git integration. This plugin just brings it to the next level.

`Pylance <https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance>`_

Fast, feature-rich language support for Python. Powered by Pyright so gives nice type checking.

`Python Test Explorer for Visual Studio Code <https://marketplace.visualstudio.com/items?itemName=LittleFoxTeam.vscode-python-test-adapter>`_

What it says in the tin.

`Python-autopep8 <https://code.visualstudio.com/docs/python/editing>`_

Can `Ctrl-P` -> `Format Code` or format on save.

`reStructuredText <https://marketplace.visualstudio.com/items?itemName=lextudio.restructuredtext>`_

Great for checking your rst as you type.

`Vim <https://github.com/VSCodeVim/Vim>`_

Totally Optional. If you're a VIM geek like myself, then it is mandatory though :P



