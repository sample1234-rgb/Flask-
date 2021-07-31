from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Conv2D, MaxPooling2D, Activation, Flatten, Dropout, Dense, experimental, SeparableConv2D
from keras.layers import BatchNormalization, add, GlobalAveragePooling2D
from keras.preprocessing.image_dataset import image_dataset_from_directory
from keras import backend as K
import keras
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
print('--Modules-Imported--')

class make_model:
    image_size = (300, 450)
    batch = 10
    aug = Sequential([
        experimental.preprocessing.RandomFlip("horizontal"),
        experimental.preprocessing.RandomRotation(0.1)])

    def __init__(self, train_path, test_path, input_shape=image_size + (3,), num_classes=2):
        train_ds, val_ds = self.__inputs__(train_path, test_path)
        self.model = self.__model__(input_shape, num_classes)
        self.fit(train_ds, val_ds)
        self.weights = self.model.weights

    def __inputs__(self, train_path="input/picture/train", test_path="input/picture/validate"):
        train_data = image_dataset_from_directory(train_path, validation_split=0.2, subset="training",
                                                  seed=1337, image_size=self.image_size, batch_size=self.batch)
        val_ds = image_dataset_from_directory(test_path, validation_split=0.2, subset="validation",
                                              seed=1337, image_size=self.image_size, batch_size=self.batch)
        plt.figure(figsize=(10, 10))
        for images, labels in self.train_data.take(1):
            for i in range(9):
                ax = plt.subplot(3, 3, i + 1)
                plt.imshow(images[i].numpy().astype("uint8"))
                plt.title(int(labels[i]))
                plt.axis("off")

        return train_data, val_ds

    def fit(self, train_ds, val_ds):
        # callbacks = [keras.callbacks.ModelCheckpoint("save_at_{epoch}.h5"),]
        self.model.compile(optimizer=keras.optimizers.Adam(1e-3), loss="binary_crossentropy", metrics=["accuracy"],)
        self.model.fit(train_ds, epochs=5, validation_data=val_ds,)   # callbacks=callbacks

    def __model__(self, input_shape, num_classes):
        inputs = keras.Input(shape=input_shape)
        # Image augmentation block
        x = self.aug(inputs)

        # Entry block
        x = experimental.preprocessing.Rescaling(1.0 / 255)(x)
        x = Conv2D(32, 3, strides=2, padding="same")(x)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)

        x = Conv2D(64, 3, padding="same")(x)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)

        previous_block_activation = x  # Set aside residual

        for size in [128, 256, 512, 728]:
            x = Activation("relu")(x)
            x = SeparableConv2D(size, 3, padding="same")(x)
            x = BatchNormalization()(x)

            x = Activation("relu")(x)
            x = SeparableConv2D(size, 3, padding="same")(x)
            x = BatchNormalization()(x)

            x = MaxPooling2D(3, strides=2, padding="same")(x)

            # Project residual
            residual = Conv2D(size, 1, strides=2, padding="same")(previous_block_activation)
            x = add([x, residual])  # Add back residual
            previous_block_activation = x  # Set aside next residual

        x = SeparableConv2D(1024, 3, padding="same")(x)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)

        x = GlobalAveragePooling2D()(x)
        if num_classes == 2:
            activation = "sigmoid"
            units = 1
        else:
            activation = "softmax"
            units = num_classes
        x = Flatten()(x)
        x = Dropout(0.5)(x)
        outputs = Dense(units, activation=activation)(x)
        return Model(inputs, outputs)

    def predict(self, img_array):
        return self.model.predict(img_array)

    def show_model(self):
        return keras.utils.plot_model(model.model, show_shapes=True)

if __name__ == "__main__":
    model = make_model()
