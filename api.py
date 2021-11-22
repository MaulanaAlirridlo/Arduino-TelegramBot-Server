from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/', methods=['POST'])
def store():
    txt = open("store.txt", "wb")
    txt.write(request.data)
    return jsonify({'status' : 200})

if __name__ == '__main__':
    app.run(host="192.168.1.8", debug=True, port=8000)