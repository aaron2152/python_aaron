from flask import Flask

app = Flask(__name__)

@app.route("/ver")
def saludar():
    return "<h1>hola mundo</h1>"

@app.route("/hora")
def hora():
    #calcular la hora
    return "<h1>la hora es</h1>"