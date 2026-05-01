from flask import Flask,jsonify,render_template_string,request,Response,render_template
import re
import json
import socket
from pathlib import Path
from werkzeug.datastructures import Headers
from werkzeug.utils import secure_filename
from werkzeug.serving import WSGIRequestHandler
import sqlite3

WSGIRequestHandler.server_version = "Servidor"
WSGIRequestHandler.sys_version = ""


app = Flask(__name__)
app.config['UPLOAD_FOLDER']="C:\\upload"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.after_request
def agregar_cabeceras_seguridad(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none'"
    )
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response


def validar_hostname(hostname):
    patron = r"^[A-Za-z0-9.-]{1,253}$"
    return bool(re.fullmatch(patron, hostname)) and ".." not in hostname

@app.route("/")
def main_page():
    return "REST API"

@app.route("/user/<string:name>")
def search_user(name):
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    cur.execute("select * from test where username = ?", (name,))
    data = str(cur.fetchall())
    con.close()
    import logging
    logging.basicConfig(filename="restapi.log", filemode='w', level=logging.DEBUG)
    logging.debug(data)
    return jsonify(data=data),200


@app.route("/welcome/<string:name>")
def welcome(name):
    data="Welcome "+name
    return jsonify(data=data),200

@app.route("/welcome2/<string:name>")
def welcome2(name):
    data="Welcome "+name
    return data

@app.route("/hello")
def hello_ssti():
    if request.args.get('name'):
        name = request.args.get('name')
        template = f'''<div>
        <h1>Hello</h1>
        {name}
</div>
'''
        import logging
        logging.basicConfig(filename="restapi.log", filemode='w', level=logging.DEBUG)
        logging.debug(str(template))
        return render_template_string(template)

@app.route("/get_users")
def get_users():
    try:
        hostname = request.args.get('hostname')
        
        log_path = Path("restapi.log")
        
        if not log_path.exists():
            return "Archivo de log no encontrado", 404
        data = log_path.read_text(encoding="utf-8", errors="replace")
        return data
        
    except:
        data = str(hostname) + " username didn't found"
        return data

@app.route("/get_log/")
def get_log():
    try:
        log_path = Path("restapi.log")

        if not log_path.exists():
            return "Archivo de log no encontrado", 404

        data = log_path.read_text(encoding="utf-8", errors="replace")
        return data
    except:
        return jsonify(data="Command didn't run"), 200


@app.route("/read_file")
def read_file():
    filename = request.args.get('filename')
    file = open(filename, "r")
    data = file.read()
    file.close()
    import logging
    logging.basicConfig(filename="restapi.log", filemode='w', level=logging.DEBUG)
    logging.debug(str(data))
    return jsonify(data=data),200

@app.route("/deserialization/")
def deserialization():
    try:
        import socket, json
        HOST = "127.0.0.1"
        PORT = 8001
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            connection, address = s.accept()
            with connection:
                received_data = connection.recv(1024)
                data = json.loads(received_data.decode("utf-8"))
                return str(data)
    except:
        return jsonify(data="You must connect 8001 port"), 200


@app.route("/get_admin_mail/<string:control>")
def get_admin_mail(control):
    if control=="admin":
        data="admin@cybersecurity.intra"
        import logging
        logging.basicConfig(filename="restapi.log", filemode='w', level=logging.DEBUG)
        logging.debug(data)
        return jsonify(data=data),200
    else:
        return jsonify(data="Control didn't set admin"), 200

@app.route("/run_file")
def run_file():
    try:
        filename=request.args.get("filename")
        return "Por seguridad, la aplicación no ejecuta archivos recibidos del usuario.", 400
    except:
        return jsonify(data="File failed to run"), 200

@app.route("/create_file")
def create_file():
    try:
        filename=request.args.get("filename")
        text=request.args.get("text")
        file=open(filename,"w")
        file.write(text)
        file.close()
        return jsonify(data="File created"), 200
    except:
        return jsonify(data="File didn't create"), 200


connection = {}
max_con = 50

def factorial(number):
    if number == 1:
        return 1
    else:
        return number * factorial(number - 1)


@app.route('/factorial/<int:n>')
def factroial(n:int):
    if request.remote_addr in connection:
        if connection[request.remote_addr] > 2:
            return jsonify(data="Too many req."), 403
        connection[request.remote_addr] += 1
    else:
        connection[request.remote_addr] = 1
    result=factorial(n)
    if connection[request.remote_addr] == 1:
        del connection[request.remote_addr]
    else:
        connection[request.remote_addr] -= 1
    return jsonify(data=result), 200


@app.route('/login',methods=["GET"])
def login():
    username=request.args.get("username")
    passwd=request.args.get("password")
    if "test" in username and "test" in passwd:
        return jsonify(data="Login successful"), 200
    else:
        return jsonify(data="Login unsuccessful"), 403

@app.route('/route')
def route():
    content_type = request.args.get("Content-Type")
    response = Response()
    headers = Headers()
    headers.add("Content-Type", content_type)
    response.headers = headers
    return response

@app.route('/logs')
def ImproperOutputNeutralizationforLogs():
    data = request.args.get('data')
    import logging
    logging.basicConfig(filename="restapi.log", filemode='w', level=logging.DEBUG)
    logging.debug(data)
    return jsonify(data="Logging ok"), 200


@app.route("/user_pass_control")
def user_pass_control():
    import re
    username=request.form.get("username")
    password=request.form.get("password")
    if re.search(username,password):
        return jsonify(data="Password include username"), 200
    else:
        return jsonify(data="Password doesn't include username"), 200




@app.route('/upload', methods = ['GET','POST'])
def uploadfile():
   import os
   if request.method == 'POST':
      f = request.files['file']
      filename=secure_filename(f.filename)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return 'File uploaded successfully'
   else:
      return '''
<html>
   <body>
      <form  method = "POST"  enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>   
   </body>
</html>


      '''



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8081, debug=False)
