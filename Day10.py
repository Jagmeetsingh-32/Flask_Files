from flask import Flask,request,jsonify
import sqlite3
import hashlib
import requests

app=Flask(__name__)

def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()
@app.route('/users',methods=['POST'])
def register():
    data=request.get_json()
    user=data.get('username')
    password=data.get('password')
    if not user or not password: 
        return jsonify({"Error! : Missing Username or Password."})
    con=sqlite3.connect("users.db")
    cursor=con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id PRIMARY KEY INTEGER, username TEXT UNIQUE,password TEXT)")
    cursor.execute("SELECT username FROM users WHERE username=?",(user,))
    if cursor.fetchone():
        con.close()
        return jsonify({"Error: Username is already taken."})
    password=hash_pass(password)
    cursor.execute("INSERT INTO users(username,password) VALUES (?,?)",(user,password))
    con.commit()
    return jsonify({"Registration is done."})

@app.route("/user",methods=['GET'])
def user_data():
    con=sqlite3.connect("users.db")
    cursor=con.cursor()
    cursor.execute("SELECT username  FROM users")
    user=[row[0] for row in cursor.fetchall()]
    con.close()
    return jsonify(user)


if __name__=="__main__":
    app.run(debug=True)