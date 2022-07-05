from flask import Flask, jsonify, request
import yaml

# Config
with open('../../../config/server_address.yaml', 'r') as yml:
    api_config = yaml.safe_load(yml)
locaddr = (api_config['host'], api_config['port'])

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False    # json 文字コード修正


@app.route('/generate', methods=['GET'])
def generate():
    req = request.args
    text = req.get('text')
    text = 'Hello world' + text
    return jsonify({'message': text})


if __name__ == "__main__":
    app.run(host=api_config['host'], port=api_config['port'], debug=True)
