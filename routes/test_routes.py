from flask import Blueprint, jsonify, request
from services.test_service import process_get_test, process_post_test, process_get_test_abc

test_bp = Blueprint('test_bp', __name__)
test_abc_bp = Blueprint('test_abc_bp', __name__)

@test_bp.route('/test/get', methods=['GET'])
def test_api():
    response = process_get_test()
    return jsonify(response)

@test_bp.route('/test/post', methods=['POST'])
def test_api_post():
    data = request.get_json()
    response = process_post_test(data)
    
    # Check if response is a tuple (data + status code)
    if isinstance(response, tuple):
        return jsonify(response[0]), response[1]
    
    return jsonify(response)


@test_abc_bp.route('/test-abc/get', methods=['GET'])
def test_abc_api():
    response = process_get_test_abc()
    return jsonify(response)
