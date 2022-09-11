import sqlite3
from flask_restful import Resource, reqparse
from models.hotel import HotelModel

def normalize_path_params(cidade=None,
                          estrelas_min=0,
                          estrelas_max=5,
                          diaria_min=0,
                          diaria_max=10000,
                          limit=50,
                          offset=0, **dados):
    """Normalize json data"""
    result = {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'limit': limit,
            'offset': offset}
    if cidade:
        result['cidade'] = cidade
    return result

path_params = reqparse.RequestParser(bundle_errors=True)
path_params.add_argument('cidade', type=str, help='erro1')
path_params.add_argument('estrelas_min', type=float, help='erro2')
path_params.add_argument('estrelas_max', type=float, help='erro3')
path_params.add_argument('diaria_min', type=float, help='erro4')
path_params.add_argument('diaria_max', type=float, help='erro5')
path_params.add_argument('limit', type=float, help='erro6')
path_params.add_argument('offset', type=float, help='erro7')


class Hoteis(Resource):
    """Hoteis resource"""
    
    def get(self):
        """Return hotels data"""
        
        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)
        
        #query = "SELECT * FROM hoteis \
        #        WHERE (estrelas BETWEEN :estrelas_min AND :estrelas_max) \
        #        AND (diaria BETWEEN :diaria_min AND :diaria_max)"
        #query += " AND cidade = :cidade" if parametros.get('cidade') else ""
        #query += " LIMIT :limit OFFSET :offset"
        
        query = "SELECT * FROM hoteis"
        query += " WHERE (estrelas BETWEEN :estrelas_min AND :estrelas_max)"
        query += " AND cidade = :cidade" if parametros.get('cidade') else ""
        query += " LIMIT :limit OFFSET :offset"
        
        connection = sqlite3.connect('ambvir-src/banco.sqlite')
        connection.set_trace_callback(print)
        cursor = connection.cursor()
        result = cursor.execute(query, parametros)
        
        hotels = []
        for i in result:
            hotels.append({
                'hotel_id': i[0],
                'name': i[1],
                'stars': i[2],
                'daily': i[3],
                'city': i[4]
            })
        return {"hotels": hotels}


class Hotel(Resource):
    """A hotel resource"""

    atributos = reqparse.RequestParser()
    atributos.add_argument(
        "nome", type=str, required=True, help="The field 'nome' can not be left blank"
    )
    atributos.add_argument(
        "estrelas",
        type=str,
        required=True,
        help="The field 'estrelas' can not be left blank",
    )
    atributos.add_argument("diaria")
    atributos.add_argument("cidade")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {"message": "Hotel not found."}, 404  # not found

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {
                "message": "Hotel id '{}' already exists.".format(hotel_id)
            }, 400  # bad request

        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)

        try:
            hotel.save_hotel()
        except:
            return {
                "message": "An internal error ocurred trying to save hotel"
            }, 500  # erro interno

        return hotel.json(), 200  # sucesso

    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            try:
                hotel_encontrado.save_hotel()
            except:
                return {
                    "message": "An internal error ocurred trying to save hotel"
                }, 500  # erro interno

            return hotel_encontrado.json(), 200  # sucesso

        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(), 201  # Ok update

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {
                    "message": "An internal error ocurred trying to delete hotel"
                }, 500  # erro interno
            return {"message": "Hotel deleted."}, 200

        return {"message": "Hotel not found."}, 404
