from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__, static_folder="static", static_url_path="")


@app.route("/")
def index():
    return "<h1>Welcome to CTF!</h1>"


@app.route("/robots.txt")
def robots():
    return send_from_directory(".", "robots.txt", mimetype="text/plain")


@app.route("/super_secret_page_that_may_contain_flag")
def fake_flag():
    return "<h1>Тут пусто.</h1><p>Ну посмотри на <a href='/super_secret_page_that_may_contain_flag/files/image.png'>картинку</a></p>"


@app.route("/super_secret_page_that_may_contain_flag/files/<path:filename>")
def serve_file(filename):
    safe_path = os.path.join(app.static_folder, filename)
    if not os.path.isfile(safe_path):
        return abort(404)

    return send_from_directory(app.static_folder, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
