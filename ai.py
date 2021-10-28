import keras.losses
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, Dropout, LeakyReLU
from tensorflow.keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt
import random as r

# length
def generate_data_length(amount, shuffle_range):
    import main
    x = []
    y = []
    for i in range(amount):
        table = main.Table()
        table.set_default_table()
        new_y = len(table.shuffle(r.randint(shuffle_range[0], shuffle_range[1])))
        new_x = table.get_glasses()
        for glass in new_x:
            for _ in range(4 - len(glass)):
                glass.append(-1)
        new_y = to_categorical(new_y, 30)
        x.append(new_x)
        y.append(new_y)
    x = np.asarray(x)
    x = np.reshape(x, (-1, 12, 4, 1))
    y = np.asarray(y)
    return x, y


def define_model_length():
    model = Sequential()
    model.add(Conv2D(64, kernel_size=[3, 3], padding='same', activation='relu', input_shape=(12, 4, 1)))
    model.add(Conv2D(64, kernel_size=[3, 3], padding='same', activation='relu'))
    model.add(Conv2D(64, kernel_size=[3, 3], padding='same', activation='relu'))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(30, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    #  model.summary()
    return model


def train_length(model, x, y):
    x = np.reshape(x, (-1, 12, 4, 1))
    history = model.fit(x, y, epochs=10, batch_size=128)
    model.save('watersort.h5')


def print_accuracy(model):
    x, y = generate_data_length(1000, (0, 29))
    result = model.predict(x)
    correct = wrong = 0
    for i in range(1000):
        if np.argmax(y[i]) == np.argmax(result[i]):
          correct += 1
        else:
          wrong += 1
        print(np.argmax(y[i]) - np.argmax(result[i]))
    print(correct, wrong)


def guess(table):
    global Model
    Model = define_model_length()
    Model.load_weights('watersort.h5')
    x = []
    for glass in table.get_glasses():
        x.append(glass.copy())
    for glass in x:
        for _ in range(4 - len(glass)):
            glass.append(-1)
    x = np.reshape(x, (-1, 12, 4, 1))
    y = Model.predict(x)
    y = np.argmax(y)
    return y


if("__main__" == __name__):
  my_model = define_model_length()
  try:
      my_model.load_weights("watersort.h5")
  except:
      x, y = generate_data_length(100000, [2, 29])
      train_length(my_model, x, y)
  print_accuracy(my_model)

