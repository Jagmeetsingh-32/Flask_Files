from flask import Flask,render_template
from datetime import datetime
global user
user="jagga"
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/user_data/<user>")
def user_data(user):
    time=datetime.now().strftime('%D-%M-%Y %H:%M:%S')
    with open("text.txt","a") as file:
        file.write(f"{user}:{time}\n")
        return f"hello {user}"

@app.route("/products")
def products():
    return "<p>Hello, This is products page!</p>"

if __name__=="__main__":
     app.run(debug=True)