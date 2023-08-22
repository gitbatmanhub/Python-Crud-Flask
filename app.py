# Importar las bibliotecas necesarias
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin1223',
    'database': 'maratongaby'
}


# Función para obtener una conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(**db_config)


# Ruta para obtener todos los usuarios
@app.route('/', methods=['GET'])
def home():
    # Establecer conexión con la base de datos
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Consulta para obtener la lista de usuarios
    cursor.execute("SELECT concat(nameCliente, ' ', apellidoCliente) as nombreCompleto, idCliente FROM cliente")
    users = cursor.fetchall()
    cursor.execute

    # Cerrar la conexión con la base de datos
    connection.close()

    # Renderizar la plantilla HTML 'index.html' con la lista de usuarios
    return render_template('index.html', users=users)


# Ruta para ver todas las facturas
@app.route('/verfacturas')
def verfacturas():
    # Establecer conexión con la base de datos
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Consulta para obtener la lista de facturas ordenadas por ID
    cursor.execute("select * from datoslistafacturas order by idFactura;")
    facturas = cursor.fetchall()
    cursor.execute

    # Cerrar la conexión con la base de datos
    connection.close()

    # Renderizar la plantilla HTML 'todasFacturas.html' con la lista de facturas
    return render_template('todasFacturas.html', facturas=facturas)


# Ruta para agregar un nuevo usuario
@app.route('/agregarUsuario', methods=['POST'])
def add_user():
    # Obtener los datos del formulario
    nombre = request.form['nameCliente']
    apellido = request.form['apellidoCliente']
    cedula = request.form['cedulaCliente']

    # Establecer conexión con la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()

    # Insertar el nuevo usuario en la base de datos
    cursor.execute("INSERT INTO cliente (nameCliente, apellidoCliente, cedulaCliente) VALUES (%s, %s, %s)",
                   (nombre, apellido, cedula))
    connection.commit()

    # Cerrar la conexión con la base de datos
    connection.close()

    # Redirigir a la página de inicio
    return redirect(url_for('home'))


# Ruta para agregar una nueva factura
@app.route('/addFactura', methods=['POST'])
def addFactura():
    # Obtener el ID del cliente desde el formulario
    idCliente = request.form['idCliente']

    # Establecer conexión con la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()

    # Insertar la nueva factura en la base de datos y obtener el ID de la factura insertada
    cursor.execute("INSERT INTO factura (idCliente) VALUES (%s)", (idCliente,))
    factura_id = cursor.lastrowid
    connection.commit()

    # Cerrar la conexión con la base de datos
    connection.close()

    # Redirigir a la página de visualización de factura con el ID de la factura recién creada
    return redirect(url_for('ver_factura', factura_id=factura_id))


# Ruta para ver los detalles de una factura específica
@app.route('/factura/<int:factura_id>')
def ver_factura(factura_id):
    # Establecer conexión con la base de datos
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Obtener los detalles de la factura según el ID proporcionado
    cursor.execute("SELECT * FROM factura WHERE idFactura = %s", (factura_id,))
    detalles_factura = cursor.fetchone()
    id_cliente = detalles_factura['idCliente']
    idStatus = detalles_factura['status']

    # Obtener los detalles del cliente asociado a la factura
    cursor.execute("select * from cliente where idCliente= %s", (id_cliente,))
    detalles_cliente = cursor.fetchone()

    # Obtener todas las categorías y tipos de carrera
    cursor.execute("select * from categoria")
    datos_categoria = cursor.fetchall()
    cursor.execute("select * from tipoCarrera")
    datos_tipoCarrera = cursor.fetchall()

    # Obtener los detalles de las entradas de la factura
    cursor.execute("select * from datosEntradasfactura where idFactura=%s", (factura_id,))
    datosFactura = cursor.fetchall()

    # Calcular el precio total de las entradas de la factura
    cursor.execute("select precioEntrada from datosEntradasfactura where idFactura=%s", (factura_id,))
    precios = cursor.fetchall()
    valores_precios = [precio['precioEntrada'] for precio in precios]
    total_precios = sum(filter(lambda x: isinstance(x, float), valores_precios))
    total_precios = round(total_precios, 2)  # Redondear a 2 decimales

    # Cerrar la conexión con la base de datos
    connection.close()

    # Renderizar la plantilla HTML 'factura.html' con los detalles de la factura
    return render_template('factura.html', factura_id=factura_id, detalles_cliente=detalles_cliente,
                           datos_categoria=datos_categoria, datos_tipoCarrera=datos_tipoCarrera,
                           datosFactura=datosFactura, total_precios=total_precios, idStatus=idStatus)


# Ruta para cerrar una factura
@app.route('/cerrarfactura', methods=['POST'])
def cerrarFactura():
    # Obtener el ID de la factura y el precio total desde el formulario
    idFactura = request.form['factura_id']
    precioTotal = request.form['precioTotal']

    # Establecer conexión con la base de datos
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Actualizar el estado de la factura y el precio total en la base de datos
    cursor.execute("update factura set status=1, precioTotal= %s where idFactura= %s", (precioTotal, idFactura,))
    connection.commit()

    # Cerrar la conexión con la base de datos
    connection.close()

    # Redirigir a la página de visualización de factura con el ID de la factura actualizada
    return redirect(url_for('ver_factura', factura_id=idFactura))


# Ruta para agregar datos a una factura
@app.route('/datosaFactura', methods=['POST'])
def datosFactura():
    # Obtener los IDs de categoría, tipo de carrera y factura desde el formulario
    idCategoria = request.form['idCategoria']
    idTipoCarrera = request.form['idTipoCarrera']
    idFactura = request.form['idFactura']

    # Establecer conexión con la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()

    # Obtener el precio de la categoría y el tipo de carrera
    cursor.execute("select precioCategoria from categoria where idCategoria= %s", (idCategoria,))
    precio_categoria = cursor.fetchone()

    cursor.execute("select precioTipoCarrera from tipoCarrera where idTipoCarrera= %s", (idTipoCarrera,))
    precio_tipo = cursor.fetchone()

    # Calcular el precio total de la entrada
    preciototal = (float(precio_tipo[0]) + float(precio_categoria[0]))

    # Insertar los datos de la entrada en la base de datos
    cursor.execute("INSERT INTO entrada (idCategoria, idTipoCarrera, idFactura, precioEntrada) VALUES (%s, %s, %s, %s)",
                   (idCategoria, idTipoCarrera, idFactura, preciototal))
    connection.commit()

    # Cerrar la conexión con la base de datos
    connection.close()

    # Redirigir a la página de visualización de factura con el ID de la factura actualizada
    return redirect(url_for('ver_factura', factura_id=idFactura))


# Iniciar la aplicación si se ejecuta este archivo directamente
if __name__ == '__main__':
    # Ejecutar la aplicación en el puerto 3000 en modo de depuración
    app.run(port=3000, debug=True)
