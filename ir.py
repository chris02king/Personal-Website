from flask import Flask, request, jsonify
import boto3

app = Flask(__name__)

@app.route('/list_objects', methods=['POST'])
def list_objects():
    data = request.get_json()
    bucket_name = data.get('bucket_name')

    if not bucket_name:
        return jsonify({"error": "Bucket name is required"}), 400

    s3 = boto3.client('s3')

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        objects = [obj['Key'] for obj in response.get('Contents', [])]
        return jsonify({"objects": objects}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_object', methods=['POST'])
def get_object():
    data = request.get_json()
    bucket_name = data.get('bucket_name')
    object_key = data.get('object_key')

    if not bucket_name or not object_key:
        return jsonify({"error": "Bucket name and object key are required"}), 400

    s3 = boto3.client('s3')

    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        content = response['Body'].read().decode('utf-8')
        return jsonify({"content": content}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)