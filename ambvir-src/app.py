"""Flask app"""

from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.site import Sites, Site
from sql_alchemy import banco

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request
def cria_banco():
    """Create database"""

    banco.create_all()


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:url>')

banco.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
