from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dropout, Activation, Dense
from tensorflow.keras.optimizers import SGD, Adam
from tensorflow.keras.callbacks import EarlyStopping
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

data = pd.read_csv('bitcoin.csv').drop(['time_period_start', 'time_period_end', 'time_open', 'time_close'], axis=1)
data.head()


def lookback(dataset, timesteps=60):
    # this uses the shift method of pandas dataframes to shift all of the columns down one row
    # and then append to the original dataset
    data = dataset
    for i in range(1, timesteps):
        step_back = dataset.shift(i).reset_index()
        step_back.columns = ['index'] + [f'{column}_-{i}' for column in dataset.columns if column != 'index']
        data = data.reset_index().merge(step_back, on='index', ).drop('index', axis=1)

    return data.dropna()


features = lookback(data)


### split data into features and target
target = features['price_high'].values
features = features.drop('price_high', axis=1).values

model = Sequential()
model.add(Dense(32, input_dim=features.shape[1]))
model.add(Dense(16))
model.add(Dense(8))
model.add(Dense(1, activation='relu'))

model.compile(
    loss='mse',
    optimizer=Adam(lr=0.01), # is this the best optimizer/learning rate?
    metrics=['mean_squared_error', 'mean_absolute_error'] # does accuracy make sense in this context?
)

## callbacks
early_stopping = EarlyStopping(
    monitor='val_loss',
    mode='auto',
    restore_best_weights=True
)


history = model.fit(
    features,
    target,
    validation_split=.3,
    epochs=20,
    verbose=0
)

model.summary()

## prediction
predictions = model.predict(features)

rmse = np.sqrt(np.mean(np.square((target.reshape(-1, 1) - predictions))))
print(rmse)

model.save('yolo_model')
