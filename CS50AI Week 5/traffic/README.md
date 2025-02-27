Experiments

Originally:
333/333 - 2s - 6ms/step - accuracy: 0.0545 - loss: 3.4982

Added another conv and pooling layer:
333/333 - 3s - 10ms/step - accuracy: 0.9759 - loss: 0.0943

by adding 
tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

The additional conv and pooling made it possible to "learn" about the other details in the photos which increases accuracy by a lot.

Increasing the filters and increasing the size of kernals:
333/333 - 3s - 9ms/step - accuracy: 0.0559 - loss: 3.4964

by changing:
tf.keras.layers.Conv2D(
        64, (4, 4), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
    ),
The effect of such change is not significiant. The reasoning maybe because with just 1 conv layer, the features cannot be fully captured,
hence even with a larger filter and more filters, there is not much change in the accuracy.

Increasing the pooling size:
333/333 - 2s - 6ms/step - accuracy: 0.0557 - loss: 3.4951

by changing:
tf.keras.layers.MaxPooling2D(pool_size=(4, 4)),

Once again, no significant changes. It seemed like the only logical change was to add another conv and pooling layer.