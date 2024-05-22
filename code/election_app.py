from flask import Flask, request, jsonify, Response

from model import predict_affiliation, train_model
from logger_config import logger

app = Flask(__name__)


@app.route('/prediction', methods=['POST'])
def make_prediction() -> Response or tuple[Response, int]:
    logger.info("Receiving request for prediction")
    if request.is_json:
        district = request.get_json()
        data = {
                'district': district,
                'number_votes': 20000,
                'share_votes': 51.0,
                'year': 2024
                }
        logger.info("Request received")
        if isinstance(data, dict):
            logger.info("Generating response")
            n_model, n_onehot_encoder, n_label_encoder = train_model()
            result = predict_affiliation(data, n_model, n_onehot_encoder, n_label_encoder)
            logger.info("Response sent")
            return jsonify({"result": result})
        else:
            logger.error("ERROR: Invalid data format, expected a dictionary")
            return jsonify({"error": "Invalid data format, expected a dictionary"}), 400
    else:
        logger.error("ERROR: Invalid JSON")
        return jsonify({"error": "Invalid JSON"}), 400


if __name__ == '__main__':
    logger.info("Starting app")
    app.run(debug=True)

