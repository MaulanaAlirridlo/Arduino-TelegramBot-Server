from flask import Flask, jsonify, request
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def store():
    with open('store.json', 'w') as f:
        json.dump(request.get_json(), f)
    return jsonify({'status' : 200})

if __name__ == '__main__':
    app.run(host="192.168.45.22", debug=True, port=8000)