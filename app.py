from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests
import os

app = Flask(__name__)

API_KEY = '28948f71c93a9489ea957737009e4b8d'
HISTORIAL_FILE = 'historial.txt'

def guardar_historial(consulta):
    with open(HISTORIAL_FILE, 'a') as file:
        file.write(consulta + '\n')

def leer_historial():
    if not os.path.exists(HISTORIAL_FILE):
        return []
    with open(HISTORIAL_FILE, 'r') as file:
        return file.readlines()

@app.route('/')
def index():
    historial = leer_historial()
    return render_template('index.html', historial=historial)

@app.route('/seleccionar_tipo', methods=['POST'])
def seleccionar_tipo():
    tipo = request.form['tipo']
    return render_template('consulta.html', tipo=tipo)

@app.route('/consultar_clima', methods=['POST'])
def consultar_clima():
    ciudad = request.form['ciudad']
    unidad_temp = request.form['unidad_temp']
    unidad_temp_str = 'Celsius' if unidad_temp == 'metric' else 'Fahrenheit'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&lang=es&units={unidad_temp}'
    response = requests.get(url)
    datos_clima = response.json()

    if response.status_code == 200:
        consulta = f"Clima actual en {ciudad}: {datos_clima['main']['temp']}°{unidad_temp_str}, {datos_clima['weather'][0]['description']}, Humedad: {datos_clima['main']['humidity']}%, Viento: {datos_clima['wind']['speed']} m/s"
        guardar_historial(consulta)
        return render_template('resultado.html', resultado={
            'ciudad': datos_clima['name'],
            'pais': datos_clima['sys']['country'],
            'temperatura': f"{datos_clima['main']['temp']}°{unidad_temp_str}",
            'descripcion': datos_clima['weather'][0]['description'],
            'humedad': f"{datos_clima['main']['humidity']}%",
            'velocidad_viento': f"{datos_clima['wind']['speed']} metros por segundo"
        })
    else:
        return render_template('error.html', error='Compruebe el nombre de la ciudad e intente de nuevo')

@app.route('/consultar_pronostico', methods=['POST'])
def consultar_pronostico():
    ciudad = request.form['ciudad']
    unidad_temp = request.form['unidad_temp']
    unidad_temp_str = 'Celsius' if unidad_temp == 'metric' else 'Fahrenheit'
    fecha = request.form['fecha']
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={ciudad}&appid={API_KEY}&lang=es&units={unidad_temp}'
    response = requests.get(url)
    datos_pronostico = response.json()

    if response.status_code == 200:
        for pronostico in datos_pronostico['list']:
            if fecha in pronostico['dt_txt']:
                consulta = f"Pronóstico en {ciudad} para {fecha}: {pronostico['main']['temp']}°{unidad_temp_str}, {pronostico['weather'][0]['description']}, Humedad: {pronostico['main']['humidity']}%, Viento: {pronostico['wind']['speed']} m/s"
                guardar_historial(consulta)
                return render_template('resultado.html', resultado={
                    'ciudad': datos_pronostico['city']['name'],
                    'pais': datos_pronostico['city']['country'],
                    'temperatura': f"{pronostico['main']['temp']}°{unidad_temp_str}",
                    'descripcion': pronostico['weather'][0]['description'],
                    'humedad': f"{pronostico['main']['humidity']}%",
                    'velocidad_viento': f"{pronostico['wind']['speed']} metros por segundo"
                })
        return render_template('error.html', error='No se encontró pronóstico para la fecha seleccionada')
    else:
        return render_template('error.html', error='Compruebe el nombre de la ciudad e intente de nuevo')

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)