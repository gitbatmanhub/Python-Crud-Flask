from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin1223',
    'database': 'maratongaby'
}


def get_db_connection():
    return mysql.connector.connect(**db_config)


# Ruta para obtener todos los usuarios
@app.route('/', methods=['GET'])
def home():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT concat(nameCliente, ' ', apellidoCliente) as nombreCompleto, idCliente FROM cliente")
    users = cursor.fetchall()
    # print(users)
    cursor.execute
    connection.close()
    return render_template('index.html', users=users)


@app.route('/verfacturas')
def verfacturas():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from datoslistafacturas order by idFactura;")
    facturas = cursor.fetchall()
    # print(users)
    cursor.execute
    connection.close()
    return render_template('todasFacturas.html', facturas=facturas)






# Ruta para agregar un nuevo usuario
@app.route('/agregarUsuario', methods=['POST'])
def add_user():
    nombre = request.form['nameCliente']
    apellido = request.form['apellidoCliente']
    cedula = request.form['cedulaCliente']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO cliente (nameCliente, apellidoCliente, cedulaCliente) VALUES (%s, %s, %s)",
                   (nombre, apellido, cedula))
    connection.commit()
    connection.close()
    return redirect(url_for('home'))


@app.route('/addFactura', methods=['POST'])
def addFactura():
    idCliente = request.form['idCliente']
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO factura (idCliente) VALUES (%s)", (idCliente,))
    factura_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return redirect(url_for('ver_factura', factura_id=factura_id))

@app.route('/factura/<int:factura_id>')
def ver_factura(factura_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM factura WHERE idFactura = %s", (factura_id,))
    detalles_factura = cursor.fetchone()
    id_cliente = detalles_factura['idCliente']
    idStatus = detalles_factura['status']
    #print(id_cliente)
    cursor.execute("select * from cliente where idCliente= %s", (id_cliente,))
    detalles_cliente = cursor.fetchone()
    cursor.execute("select * from categoria")
    datos_categoria = cursor.fetchall()
    cursor.execute("select * from tipoCarrera")
    datos_tipoCarrera = cursor.fetchall()

    cursor.execute("select * from datosEntradasfactura where idFactura=%s", (factura_id,))
    datosFactura = cursor.fetchall()

    cursor.execute("select precioEntrada from datosEntradasfactura where idFactura=%s", (factura_id,))
    precios = cursor.fetchall()
    valores_precios = [precio['precioEntrada'] for precio in precios]
    total_precios = sum(filter(lambda x: isinstance(x, float), valores_precios))
    total_precios = round(total_precios, 2)  # Redondear a 2 decimales
    connection.close()

    return render_template('factura.html', factura_id=factura_id, detalles_cliente=detalles_cliente, datos_categoria=datos_categoria, datos_tipoCarrera=datos_tipoCarrera, datosFactura=datosFactura, total_precios=total_precios, idStatus=idStatus)

@app.route('/cerrarfactura', methods=['POST'])
def cerrarFactura():
    idFactura = request.form['factura_id']
    precioTotal = request.form['precioTotal']
    #print(idFactura)
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("update factura set status=1, precioTotal= %s where idFactura= %s", (precioTotal, idFactura,))
    connection.commit()
    connection.close()
    return redirect(url_for('ver_factura', factura_id=idFactura))



@app.route('/datosaFactura', methods=['POST'])
def datosFactura():
    idCategoria = request.form['idCategoria']
    idTipoCarrera = request.form['idTipoCarrera']
    idFactura = request.form['idFactura']


    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("select precioCategoria from categoria where idCategoria= %s", (idCategoria,))
    precio_categoria = cursor.fetchone()

    cursor.execute("select precioTipoCarrera from tipoCarrera where idTipoCarrera= %s", (idTipoCarrera,))
    precio_tipo = cursor.fetchone()



    #print(precio_categoria)
    #print(precio_tipo)
    preciototal=(float(precio_tipo[0]) + float(precio_categoria[0]))
    #print(preciototal)


    cursor.execute("INSERT INTO entrada (idCategoria, idTipoCarrera, idFactura, precioEntrada) VALUES (%s, %s, %s, %s)", (idCategoria, idTipoCarrera, idFactura, preciototal))
    connection.commit()
    connection.close()


    return redirect(url_for('ver_factura', factura_id=idFactura))


if __name__ == '__main__':
    app.run(port=3000, debug=True)
