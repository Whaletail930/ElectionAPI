import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from data_loaders import concat_dfs
from logger_config import logger


def train_model() -> tuple[Sequential, OneHotEncoder, LabelEncoder] or None:
    logger.info("Creating training dataset")
    data = concat_dfs("hungarian_election2014.csv",
                      "hungarian_election2018.csv",
                      "hungarian_election2022.csv")

    df = pd.DataFrame(data)

    logger.info("Training model")
    try:
        onehot_encoder = OneHotEncoder()
        district_encoded = onehot_encoder.fit_transform(df[['district']]).toarray()

        label_encoder = LabelEncoder()
        df['affiliation_encoded'] = label_encoder.fit_transform(df['affiliation'])

        features = pd.DataFrame(district_encoded)
        features['number_votes'] = df['number_votes']
        features['share_votes'] = df['share_votes']
        features['year'] = df['year']

        x_train, x_test, y_train, y_test = train_test_split(features, df['affiliation_encoded'], test_size=0.2, random_state=42)

        model = Sequential()
        model.add(Dense(32, input_dim=x_train.shape[1], activation='relu'))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(len(label_encoder.classes_), activation='softmax'))

        model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        model.fit(x_train, y_train, epochs=50, batch_size=10, validation_split=0.2)

        loss, accuracy = model.evaluate(x_test, y_test)
        print(f'Test Accuracy: {accuracy*100:.2f}%')
        logger.info(f'Training successful. Test Loss: {loss:} Test Accuracy: {accuracy*100:.2f}%')
        if accuracy < 0.80:
            logger.warning('Accuracy is below 80%, result may not be accurate')

        return model, onehot_encoder, label_encoder

    except Exception as e:
        logger.error(f"ERROR: {str(e)}")
        return None


def predict_affiliation(model_input: dict,
                        model: Sequential,
                        onehot_encoder: OneHotEncoder,
                        label_encoder: LabelEncoder) -> str or None:
    logger.info("Making prediction")
    try:
        new_input_df = pd.DataFrame([model_input])

        district_encoded = onehot_encoder.transform(new_input_df[['district']]).toarray()
        district_encoded_df = pd.DataFrame(district_encoded, columns=onehot_encoder.get_feature_names_out(['district']))

        new_input_processed = pd.concat(
            [district_encoded_df, new_input_df[['number_votes', 'share_votes', 'year']].reset_index(drop=True)], axis=1)

        predicted_class_probs = model.predict(new_input_processed)
        predicted_class_index = np.argmax(predicted_class_probs, axis=1)
        predicted_affiliation = label_encoder.inverse_transform(predicted_class_index)[0]

        logger.info(f"Prediction successful. Affiliation: {predicted_affiliation}")
        print(f'Predicted Affiliation: {predicted_affiliation}')

        return predicted_affiliation
    except Exception as e:
        logger.error(f"ERROR: {str(e)}")

        return None


n_model, n_onehot_encoder, n_label_encoder = train_model()

"""new_input = {
    'district': 'Baja',
    'number_votes': 20000,
    'share_votes': 50.0,
    'year': 2024
}

n_predicted_affiliation = predict_affiliation(new_input, n_model, n_onehot_encoder, n_label_encoder)"""

