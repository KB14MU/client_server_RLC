import tensorflow as tf
import numpy as np
from collections import deque
from threading import Lock
from custom_logging import logger

class DQNReinforcementLearning:
    def __init__(self, state_size, action_size, epsilon_decay=0.995, learning_rate=0.001):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # discount factor
        self.epsilon = 1.0  # exploration-exploitation trade-off
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = 0.01
        self.learning_rate = learning_rate
        self.model = self._build_model()
        self.lock = Lock()

    def _build_model(self):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(tf.keras.layers.Dense(24, activation='relu'))
        model.add(tf.keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        with self.lock:
            self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        with self.lock:
            act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        with self.lock:
            minibatch = np.array(random.sample(self.memory, batch_size))
        
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                with self.lock:
                    target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))

            target_f = self.model.predict(state)
            target_f[0][action] = target
            with self.lock:
                self.model.fit(state, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def train(self, state, action, reward, next_state, done):
        state = np.reshape(state, [1, self.state_size])
        next_state = np.reshape(next_state, [1, self.state_size])
        with self.lock:
            self.remember(state, action, reward, next_state, done)
        with self.lock:
            self.replay(32)

    def fine_tune(self, new_epsilon_decay, new_learning_rate):
        with self.lock:
            self.epsilon_decay = new_epsilon_decay
            self.learning_rate = new_learning_rate
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def save_model(self, model_path='dqn_model.h5'):
        with self.lock:
            self.model.save(model_path)
            logger.info(f"Model saved to {model_path}")

    def load_model(self, model_path='dqn_model.h5'):
        with self.lock:
            self.model = tf.keras.models.load_model(model_path)
            logger.info(f"Model loaded from {model_path}")