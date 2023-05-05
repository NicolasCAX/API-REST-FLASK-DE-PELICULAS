
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/Nbased'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
based = SQLAlchemy(app)
mardb = Marshmallow(app)

class Peliculas(based.Model):
    peliculaID = based.Column(based.Integer,primary_key=True)
    peliName = based.Column(based.String(50))
    pelidesc = based.Column(based.String(100))
    peliCate = based.Column(based.String(30))

    def __init__(self,peliName,pelidesc,peliCate):
        self.peliName = peliName
        self.pelidesc = pelidesc
        self.peliCate = peliCate


based.create_all()

class peliSchema(mardb.Schema):
    class Meta:
        fields = ('peliculaID','peliName','pelidesc',"peliCate")


peli_schema = peliSchema()
peli_schema = peliSchema(many=True)

@app.route('/pelicula',methods=['GET'])
def get_peliculas():
    all_peliculas = Peliculas.query.all()
    result = peli_schema.dump(all_peliculas)
    return jsonify(result)

#GET X ID
@app.route('/pelicula/<id>',methods=['GET'])
def get_pelicula_x_id(id):
    una_pelicula = Peliculas.query.get(id)
    return peli_schema.jsonify(una_categoria)

#POST
@app.route('/pelicula',methods=['POST'])
def insert_categoria():
    data = request.get_json(force=True)
    peliName = data['peliName']
    pelidesc = data['pelidesc']
    peliCate = data['peliCate']

    nuevoPelicula = Peliculas(peliName, pelidesc, peliCate)

    based.session.add(nuevoPelicula)
    based.session.commit()
    return peli_schema.jsonify(nuevoPelicula)

#PUT
@app.route('/pelicula/<id>',methods=['PUT'])
def update_pelicula(id):
    actualizarPelicula = Peliculas.query.get(id)

    data = request.get_json(force=True)
    peliName = data['peliName']
    pelidesc = data['pelidesc']
    peliCate = data['peliCate']

    actualizarPelicula.peliName = peliName
    actualizarPelicula.pelidesc = pelidesc
    actualizarPelicula.peliCate = peliCate

    based.session.commit()

    return categoria_schema.jsonify(actualizarPelicula)

@app.route('/pelicula/<id>',methods=['DELETE'])
def delete_categoria(id):
    eliminarPelicula = Peliculas.query.get(id)
    based.session.delete(eliminarPelicula)
    based.session.commit()
    return peli_schema.jsonify(eliminarPelicula)

#Mensaje de Bienvenida
@app.route('/',methods=['GET'])
def index():
    return jsonify({'Mensaje':'API REST FLASK DE PELICULAS'})

if __name__=="__main__":
    app.run(debug=True)
