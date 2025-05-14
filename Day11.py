from flask import Flask,request,jsonify
import sqlite3
import hashlib

app=Flask(__name__)
request_counts={}

def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest

@app.route('/usere',methods=["POST"])
def register():
    session_id=request.remote_addr
    request_counts[session_id]=request_counts.get(session_id,0)+1
    if request_counts[session_id] >5:
        return jsonify("Error! Too many requests..") ,429
    data=request.get_json()
    user=data.get("username")
    password=data.get('password')
    con=sqlite3.connect("users.db")
    cursor=con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users(id. Integer Primary key,username Unique Text,password Text)")
    cursor.execute("SELECT username FROM users WHERE username=?",(user))
    if cursor.fetchone():
        con.close()
        return jsonify("Error! Username is already exists")
    hashed=hash_pass(password)
    cursor.execute("INSERT INTO users (username,password) VALUES (?,?)",(user,hashed))
    con.commit()
    con.close()
    return jsonify({"Registration is done."})

@app.route('/user',methods=["GET"])
def get_user():
    con=sqlite3.connect("users.db")
    cursor=con.cursor()
    cursor.execute("SELECT username FROM users")
    hello = [row[0] for row in cursor.fetchall()]
    con.close()
    return jsonify(hello)

if __name__=="__main__":
    app.run(debug=True)
