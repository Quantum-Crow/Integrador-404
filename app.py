from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/')
def obtener_clima(ciudad, api_key):
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
        print(f"Error: {respuesta.status_code}")
        return None

def mostrar_clima(datos_clima):
    if datos_clima:
        print(f"Clima en {datos_clima['name']}, {datos_clima['sys']['country']}:")
        print(f"Temperatura: {datos_clima['main']['temp']}°C")
        print(f"Descripción: {datos_clima['weather'][0]['description']}")
        print(f"Humedad: {datos_clima['main']['humidity']}%")
    else:
        print("No se pudo obtener el clima.")

if __name__ == "__main__":
    api_key = "74c4a6477a423e5ba799eef8170910f9" 
    ciudad = input("Introduce el nombre de la ciudad: ")
    unidades = input("Introduce la unidad de temperatura (C para Celsius, F para Fahrenheit): ").upper()

    if unidades == 'C':
        unidades = 'metric'
        unidad_temp = 'C'
    elif unidades == 'F':
        unidades = 'imperial'
        unidad_temp = 'F'
    else:
        print("Unidad de temperatura no válida. Usando Celsius por defecto.")
        unidades = 'metric'
        unidad_temp = 'C'
    datos_clima = obtener_clima(ciudad, api_key)
    mostrar_clima(datos_clima)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
