# Criação de uma ETL em flask

## Como iniciar 

Primeiro é necessário coletar uma API Key para substituir no campo respectivo do código. A API Key pode ser coletada no seguinte URL:

https://home.openweathermap.org/api_keys

Após isso, para rodar o código, será necessário realizar a instalação dos módulos utilizados. O seguinte comando, seguido do nome do respectivo módulo, pode resolver esta questão:

python -m pip install nomedomodulo

## Módulos utilizados:

* Flask e render_template: Utilizados para renderizar template HTML e criar a aplicação.
* SQL Alchemy: Utilizado para a criação da database.
* Datetime e pytz: Utilizados para trabalhar com timezone.
* JSON e requests: Utilizados para trabalhar com data JSON e requisições HTTP.

## Estrutura do código

A aplicação é inicializada com "app = Flask(__name__).";

A conexão com a database SQLite é configurada com app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///etl_database.db' e a instância SQLAlchemy é criada com " db = SQLAlchemy(app) ";

" brasil_timezone = pytz.timezone('America/Sao_Paulo') " define a timezone.

A classe WeatherData é um modelo para a tabela SQLite. Essa classe é herdada do db.Model, do SQLAlchemy. A chave primária é o ID, como mostra o parâmetro "primary_key=True"

A função ETL realiza um GET da API para cada cidade, extrai o JSON dos dados recebidos e insere na base de dados. 

A rota /weather_data é utilizada para analisar os dados coletados em um HTML básico feito com essa finalidade.

O último bloco é o  "if __name__ == '__main__'", que a execução do script seja feita de forma direta e não por meio da importação do módulo. Por fim, a função db.create_all() é chamada no context da aplicação Flask para criar as tabelas com base nos modelos definidos.

## Teste

O arquivo teste.py permite a realização de alguns testes com o uso do pytest. 

Para rodar o teste, deve-se inserir no terminal o comando "python -m pytest teste.py". 

Os testes são definidos nos blocos que começam com o comando "assert" e foram definidos alguns como do tipo dos dados, que deve ser "openweather", e do tamanho do array que deve ser igual a 3. 
  
