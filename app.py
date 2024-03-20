from config import config
from src import init_app
from extensions import db,migrate

configuration = config['development']
# configuration = config['deploy']

app = init_app(configuration)

db.init_app(app)

migrate.init_app(app,db)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 5000)
