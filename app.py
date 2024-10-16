from flask import Flask, request, jsonify
import requests

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

    api_key = "TU_API_KEY"  
    datos_clima = obtener_clima(ciudad, api_key, unidades)

    if datos_clima:
        return jsonify({
            'ciudad': datos_clima['name'],
            'pais': datos_clima['sys']['country'],
            'temperatura': f"{datos_clima['main']['temp']}°{unidad_temp}",
            'descripcion': datos_clima['weather'][0]['description'],
            'humedad': f"{datos_clima['main']['humidity']}%",
            'velocidad_viento': f"{datos_clima['wind']['speed']} m/s"
        })
    else:
        return jsonify({'error': 'No se pudo obtener el clima'}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
