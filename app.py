from flask import Flask, request, jsonify, render_template
import requests
import datetime

app = Flask(__name__)

def obtener_clima(ciudad, api_key, unidades):
    url_base = "http://api.openweathermap.org/data/2.5/weather"
    parametros = {
        'q': ciudad,
        'appid': api_key,
        'units': unidades,  
        'lang': 'es'  
    }

    respuesta = requests.get(url_base, params=parametros)

    if respuesta.status_code == 200:
        datos = respuesta.json()
        return datos
    else:
        return None

def obtener_pronostico(ciudad, api_key, unidades, fecha):
    url_base = "http://api.openweathermap.org/data/2.5/forecast"
    parametros = {
        'q': ciudad,
        'appid': api_key,
        'units': unidades,  
        'lang': 'es'  
    }

    respuesta = requests.get(url_base, params=parametros)

    if respuesta.status_code == 200:
        datos = respuesta.json()
        for item in datos['list']:
            if datetime.datetime.fromtimestamp(item['dt']).date() == fecha:
                return item
    return None

def guardar_historial(ciudad, datos_clima, unidades):
    with open('historial.txt', 'a') as archivo:
        archivo.write(f"Ciudad: {ciudad}\n")
        archivo.write(f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        archivo.write(f"Temperatura: {datos_clima['main']['temp']}°{unidades}\n")
        archivo.write(f"Descripción: {datos_clima['weather'][0]['description']}\n")
        archivo.write(f"Humedad: {datos_clima['main']['humidity']}%\n")
        archivo.write(f"Velocidad del viento: {datos_clima['wind']['speed']} m/s\n")
        archivo.write("\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clima', methods=['GET'])
def clima():
    ciudad = request.args.get('ciudad')
    unidades = request.args.get('unidades', 'C').upper()

    if unidades == 'C':
        unidades = 'metric'
        unidad_temp = 'C'
    elif unidades == 'F':
        unidades = 'imperial'
        unidad_temp = 'F'
    else:
        unidades = 'metric'
        unidad_temp = 'C'

    api_key = "28948f71c93a9489ea957737009e4b8d"  
    datos_clima = obtener_clima(ciudad, api_key, unidades)

    if datos_clima:
        guardar_historial(ciudad, datos_clima, unidad_temp)
        return jsonify({
            'ciudad': datos_clima['name'],
            'pais': datos_clima['sys']['country'],
            'temperatura': f"{datos_clima['main']['temp']}°{unidad_temp}",
            'descripcion': datos_clima['weather'][0]['description'],
            'humedad': f"{datos_clima['main']['humidity']}%",
            'velocidad_viento': f"{datos_clima['wind']['speed']} metros por segundo"
        })
    else:
        return jsonify({'error': 'No se pudo obtener el clima'}), 400

@app.route('/pronostico', methods=['GET'])
def pronostico():
    ciudad = request.args.get('ciudad')
    unidades = request.args.get('unidades', 'C').upper()
    fecha = request.args.get('fecha')

    if unidades == 'C':
        unidades = 'metric'
        unidad_temp = 'C'
    elif unidades == 'F':
        unidades = 'imperial'
        unidad_temp = 'F'
    else:
        unidades = 'metric'
        unidad_temp = 'C'

    api_key = "28948f71c93a9489ea957737009e4b8d"  
    fecha_obj = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()
    datos_pronostico = obtener_pronostico(ciudad, api_key, unidades, fecha_obj)

    if datos_pronostico:
        guardar_historial(ciudad, datos_pronostico, unidad_temp)
        return jsonify({
            'ciudad': ciudad,
            'fecha': fecha,
            'temperatura': f"{datos_pronostico['main']['temp']}°{unidad_temp}",
            'descripcion': datos_pronostico['weather'][0]['description'],
            'humedad': f"{datos_pronostico['main']['humidity']}%",
            'velocidad_viento': f"{datos_pronostico['wind']['speed']} m/s"
        })
    else:
        return jsonify({'error': 'No se pudo obtener el pronóstico'}), 400

@app.route('/historial', methods=['GET'])
def historial():
    try:
        with open('historial.txt', 'r') as archivo:
            contenido = archivo.read()
        return render_template('historial.html', contenido=contenido)
    except FileNotFoundError:
        return render_template('historial.html', contenido="No hay historial disponible.")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

