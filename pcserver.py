from flask import Flask, request

app = Flask(__name__)


@app.route('/set')
def set_status():
    status = request.args.get("status")
    with open("status.txt","w+") as f:
        f.write(status)
    return "ok"

@app.route("/get")
def get_status():
    try:
        with open("status.txt","r+") as f:
            data=f.read()
        return data
    except:
        return "0"


if __name__ == '__main__':
    app.run(port=5000)
