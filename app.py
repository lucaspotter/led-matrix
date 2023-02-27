from flask import Flask, render_template, request, abort

app = Flask(__name__)


def addRequestToQueue(data):  # add new request to queue
    print(data)
    file1 = open("data.txt", "a")
    file1.write(data + "\n")
    file1.close()

ip_ban_list = []  # i had it public and that's where this came from.

@app.before_request
def block_method():  # some people can't let us have nice things.
    ip = request.environ.get('REMOTE_ADDR')
    if ip in ip_ban_list:
        abort(403)

@app.route('/', methods=['GET'])
def form():
    return render_template('form.html')


@app.route('/sent', methods=['GET', 'POST'])
def sent():
    if request.method == 'POST':
        return render_template('response.html', content=request.form['content']), addRequestToQueue(
            request.form.get("content"))  # thanks for the post req, adding it to queue
    elif request.method == 'GET':
        return render_template('form.html')


if __name__ == "__main__":
    app.run()  # if you need the server to be externally accessible, put host='0.0.0.0' in the brackets
