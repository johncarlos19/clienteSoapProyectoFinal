#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from json import *

import zeep
from zeep import helpers, xsd
from zeep.transports import Transport
from requests import Session
from flask import *
import jsonpickle
import base64

listaFormulario = []

def lista_Formulario_buscado_borrar():
    global listaFormulario
    listaFormulario = []

class Formulario(object):

    def __init__(self,fotoBase64,id, latitud,longitud,mimeType,nivelEscolar,nombre,sector):
        self.fotoBase64 = fotoBase64;
        self.id = id;
        self.latitud = latitud;
        self.longitud = longitud;
        self.mimeType = mimeType;
        self.nivelEscolar = nivelEscolar;
        self.nombre = nombre;
        self.sector = sector;


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

def FormularioDecoder(obj):

    return Formulario(obj.fotoBase64, obj.id,obj.latitud,obj.longitud,obj.mimeType,obj.nivelEscolar,obj.nombre,obj.sector)

def jsonDefault(o):
    return o.decode('utf-8')


session = Session()
session.cert
transport = Transport(session=session)
wsdl = 'https://parcial2.intelligence.gq/ws/FormularioWebServices?wsdl'
#wsdl = 'http://localhost:7000/ws/FormularioWebServices?wsdl'
client = zeep.Client(wsdl=wsdl,transport=transport)
app = Flask(__name__, static_url_path='', static_folder='static', template_folder='static')


@app.route('/', methods=['GET'])
def index():

    # active
    # app.send_static_file('index.html', statu=statu);

    return render_template("index.html");
@app.route('/listaFormulario', methods=['GET'])
def listaFormulario():
    lista_Formulario_buscado_borrar()
    posicion = 0
    if (len(listaFormulario) != 0):
        while posicion < len(listaFormulario):
            listaFormulario.pop(posicion)
            posicion = posicion + 1
    for aux in client.service.getListaFormulario():
        listaFormulario.append(FormularioDecoder(aux))

    return render_template("listaFormulario.html",formulario = listaFormulario, title="Lista De Formulario");
@app.route('/ver', methods=['GET'])
def ver():
    #request.args.get('buscar_pac')
    formu = FormularioDecoder(client.service.getFormulario(int(request.args.get('id'))))

    return render_template("formulario.html",formulario = formu, title="Detalle del Individuo");
@app.route('/crear', methods=['POST','GET'])
def crear():
    if(request.method == 'GET'):
        return render_template("crear.html", title="Registrar formulario");
    elif(request.method == 'POST'):
        aux = request.files['foto']
        mimeType = aux.content_type;
        fotoBase64 = base64.b64encode(aux.read())

        va = Formulario( jsonDefault(fotoBase64), 0, request.form['latitud'], request.form['longitud'], mimeType, request.form['nivelEscolar'], request.form['nombre'], request.form['sector']).toJSON()
        print("json: "+va+" desc: "+str(json.loads(va)))
        client.service.crearFormulario(json.loads(va))

        return redirect("/agregado")

@app.route('/agregado', methods=['GET'])
def agregado():

    # active
    # app.send_static_file('index.html', statu=statu);

    return render_template("agregado.html");

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port='5000')



# session = Session()
# session.cert
# transport = Transport(session=session)
# wsdl = 'https://parcial2.intelligence.gq/ws/FormularioWebServices?wsdl'
# #wsdl = 'http://localhost:7000/ws/FormularioWebServices?wsdl'
# client = zeep.Client(wsdl=wsdl,transport=transport)

# while True:
#     print('Bievenido al Portal Estudiantil ')
#     print('\n1) Listar todos las form\t\n2) Consultar Formulario\n3) Crear un nuevo Estudiante\n4)Borrar un estudiante.')
#     opcion = int(input("◄◄◄◄◄◄◄ Ingrese el número de la opción deseada ►►►►►►►: "))
#
#     if opcion == 1:
#         for aux in client.service.getListaFormulario():
#             listaFormulario.append(FormularioDecoder(aux))
#
#
#         for a in listaFormulario:
#             print("va")
#             print(a.nombre)
#
#     if opcion == 2:
#         matricula = int(input('◄◄◄◄◄◄◄ Digite la matricula del estudiante ►►►►►►►: '))
#         xx = client.service.getFormulario(matricula)
#         print(xx.fotoBase64)
#
#
#     if opcion == 3:
#         fotoBase64 = None
#         id = 0
#         latitud = float(input('◄◄◄◄◄◄◄ Digite la latitud ►►►►►►►: '))
#         longitud = round(float(input('◄◄◄◄◄◄◄ Digite la longitud ►►►►►►►: ')),3)
#         mimeType = input('◄◄◄◄◄◄◄ Digite el mimeType ►►►►►►►: ')
#         nivelEscolar = input('◄◄◄◄◄◄◄ Digite la nivelEscolar ►►►►►►►: ')
#         nombre = input('◄◄◄◄◄◄◄ Digite la nombre ►►►►►►►: ')
#         sector = input('◄◄◄◄◄◄◄ Digite el sector ►►►►►►►: ')
#
#         va = Formulario(fotoBase64,id, latitud,longitud,mimeType,nivelEscolar,nombre,sector).toJSON()
#         print("json: "+va+" desc: "+str(json.loads(va)))
#         client.service.crearFormulario(json.loads(va))
#         #print(client.create_message(client.service,"crearEstudiante",json.loads(va)))
#     if opcion == 4:
#         matricula = int(input('◄◄◄◄◄◄◄ Digite la matricula ►►►►►►►: '))
#
#         print("Estudiante eliminado: "+client.service.eliminandoEstudiante(matricula))
#         #Esta funcion no esta implementada en el servidor