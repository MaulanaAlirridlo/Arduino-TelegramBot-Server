from flask import Flask, jsonify, request
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def store():
    if request.is_json() :
        with open('store.json', 'w') as f:
            json.dump(request.get_json(), f)
        return jsonify({'status' : 200})

if __name__ == '__main__':
    app.run(host="47.254.240.15", debug=True, port=8000)