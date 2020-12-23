Training the Model
==================

TrainSequence
-------------

The class `ml.train_sequence.TrainSequence` provides generation of training data on the fly.

It takes the TimeSeries from `Optimal Position` and:

1. Increase dimension by creating last n observable prices for every minute of the training data set. This is X
2. Take Optimal position which is now Y. So now we have X predicting Y.
3. Normalise the look back observable so it values are between 0 and 1
4. Shuffle the training dataset on each Epoch.

For step one, there is a parameter `lookback_period` that can be used to control how far back the neutral network
can see when training.

The `TrainSequence` can be instantiated like this:

::

    start_date = date(2017, 6, 1)
    end_date = date(2020, 6, 1)
    db = kydb.connect('dynamodb://epython/timeseries')
    ts = db['/symbols/ml/training_data/FX_BTC_JPY']
    pos_df = ts.curve(start_date, end_date)
    seq = TrainSequence(pos_df.reset_index()[['mid', 'position']].copy())

Setting up the model
^^^^^^^^^^^^^^^^^^^^

With `TrainSequence` defined we can get creative and design a TensorFlow model.

Exactly what kind of layers, how many layers, nodes per layer, activation function is
already an art more than science. On top of that we still have choices of
optimizer, loss function, etc..

Luckily AWS Sage Maker makes hyper-parameter optimisation easy.
We will cover that in a later chapter.

So this the below is just an example that I found to give good results.

There are 4 layers:

1. Dense (fully connected) layer with 1024 nodes and ReLU (Rectified Linear Unit) as activation function.
2. Dense layer with 1024 nodes and uses ReLU activation function.
3. Dropout of 0.2 to regulate the network.
4. Dese with just 2 nodes representing buy or sell. Use softmax activation function.

::

    model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(1024, input_shape=(seq.lookback_period,), activation=tf.nn.relu),    
    tf.keras.layers.Dense(1024, activation=tf.nn.relu),  
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(2, activation=tf.nn.softmax)
    ])

Compile the module. use `adam` optimiser `sparse_categorical_crossentropy` as loss function of
and display `accuracy` as it optimises.

::

    model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])              

Now we're all set. Let's fit the model.

Training the model
^^^^^^^^^^^^^^^^^^

::

    model.fit_generator(generator=seq, epochs=10, workers=cpu_count(), use_multiprocessing=True))

Model performance
^^^^^^^^^^^^^^^^^

We can see the performance during training. Loss should be coming down
and accuracy would be go up.

.. code-block:: console

    Epoch 1/10
    119/119 [==============================] - 203s 2s/step - loss: 0.7163 - acc: 0.5772
    Epoch 2/10
    119/119 [==============================] - 200s 2s/step - loss: 0.6434 - acc: 0.6338
    Epoch 3/10
    119/119 [==============================] - 199s 2s/step - loss: 0.6283 - acc: 0.6495
    Epoch 4/10
    119/119 [==============================] - 200s 2s/step - loss: 0.6142 - acc: 0.6645
    Epoch 5/10
    119/119 [==============================] - 199s 2s/step - loss: 0.6010 - acc: 0.6759
    Epoch 6/10
    119/119 [==============================] - 199s 2s/step - loss: 0.5890 - acc: 0.6863
    Epoch 7/10
    119/119 [==============================] - 199s 2s/step - loss: 0.5702 - acc: 0.7024
    Epoch 8/10
    119/119 [==============================] - 199s 2s/step - loss: 0.5528 - acc: 0.7157
    Epoch 9/10
    119/119 [==============================] - 200s 2s/step - loss: 0.5307 - acc: 0.7322
    Epoch 10/10
    119/119 [==============================] - 199s 2s/step - loss: 0.5036 - acc: 0.7516

Of course. Instead of running 3 years of minutely data and hope it all works we can always reduce
the size of the neural network and run on a smaller set of data.

Here is what what happens if we reduce nodes to 512 on the dense network,
train the model and then use the model to predict.

Orange line is the optimal position, blue is the prediciton.

.. image:: ../_static/images/trade_position_prediction.PNG

Persisting the model 
--------------------

The model can be persisted in a file and uploaded to KYDB.

::

    model_file = 'fx_btc_jpy_model.h5'
    model.save(model_file)
    db = kydb.connect('s3://epython')
    with open(model_file, 'rb') as f:
    data = f.read()
    db['/ml/models/' + model_file] = data

Training Notebook
-----------------

`Training Notebook <../_static/notebooks/Training.html>`_ can be found here.
