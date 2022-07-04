from flask import Flask, jsonify, request

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False    # json 文字コード修正
 
@app.route('/generate', methods=['GET'])
def generate():
    req = request.args
    text = req.get('text')
    print(type(text))
    text = 'Hello world' + text
    return jsonify({'message': text})

if __name__ == "__main__":
    app.run(host='localhost', port=8000, debug=True)