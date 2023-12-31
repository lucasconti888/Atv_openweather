# python -m pip install Flask
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import requests
import pytz
import logging

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///etl_database.db'
db = SQLAlchemy(app)

brasil_timezone = pytz.timezone('America/Sao_Paulo')

def get_brasil_datetime():
    return datetime.now(brasil_timezone)

class WeatherData(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   data_ingestao = db.Column(db.DateTime, default=get_brasil_datetime)
   data_type = db.Column(db.String(50))
   values = db.Column(db.String(100))
   usage = db.Column(db.String(100))

def weather_data_to_json(weather_data):
   return json.dumps(weather_data, default=lambda o: o.__dict__, 
                    sort_keys=True, indent=4)

def funcao_etl():
    
    api_key = '183b96fb9a43765095d289409d6395d2'
    cidades = ['São Paulo', 'Rio de Janeiro', 'Brasília']
    
    lista_dados_climaticos = []  
    
    for city in cidades:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            weather_data = response.json()
            
            weather_data_json = json.dumps(weather_data)
            
            weather_entry = WeatherData(
                data_type='openweather',
                values=weather_data_json,
                usage='previsao_climatica'
            )
            
            db.session.add(weather_entry)
            db.session.commit()
            
            lista_dados_climaticos.append(weather_data_json)  
            
        else:
            app.logger.error(f'Erro na extração dos dados da API OpenWeather para {city}')
            return f'Erro na extração dos dados da API OpenWeather para {city}', 500
        
    return lista_dados_climaticos

@app.route('/', methods=['GET'])
def etl_route():
    lista_dados_climaticos = funcao_etl()
    return render_template('weather.html')

@app.route('/weather_data', methods=['GET'])
def display_weather_data():
    weather_data = WeatherData.query.all()
    
    return render_template('weather_table.html', weather_data=weather_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
