from flask import Flask
import search
import page
import add

app = Flask(__name__)

app.register_blueprint(search.search)
app.register_blueprint(page.page)
app.register_blueprint(add.add)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug = True, port=1337)
