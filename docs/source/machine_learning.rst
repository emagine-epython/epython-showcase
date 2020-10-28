Machine Learning
================

Optimal Position
----------------

For supervised training where we would like our neural network to learn when to long or short,
we would create the optimal position at any given point in time.

There is a class `ml.optimal_position.OptimalPositionGenerator` that allows us to do just that.

Usage:

::

    import kydb
    from datetime import date
    from ml.optimal_position import OptimalPositionGenerator

    db = kydb.connect('dynamodb://epython/timeseries')
    ts = db['symbols/bitflyer/minutely/FX_BTC_JPY']
    opg = OptimalPositionGenerator(ts, start_date, end_date)
    optimal = opg.generate()

Picking some random 3 days windows we would see that if we manage to trade like that, we'd be laughing.

Green is buy and red is sell.

.. image:: _static/images/optimal_strategy.PNG

See `Notebook <_static/notebooks/OptimalPositoinGenerator.html>`_ for more details.

Sage Maker
----------

From AWS Sage Maker, under Notebook select `Notebook instances`. Create instance and select `Open JupyterLab`

Choose `conda_amazonei_tensorflow_p36` as a kernel.

.. image:: _static/images/conda_amazonei_tensorflow_p36.PNG

On the left hand side panel, select `Git`. Then put in your repo url

.. image:: _static/images/clone_a_repo_url.PNG

Optionally you could choose a different branch. I usually like to work on a development branch.

.. image:: _static/images/git_select_development_branch.PNG

