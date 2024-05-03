from flask import Flask, render_template, url_for, redirect, request, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key="123"

db = mysql.connector.connect(
    host="localhost",
    database="tecnocell1",
    user="root",
    password=""
)

## INICIO

@app.route('/')
def index():
    if "usr" in session:
        return render_template('index.html', usr=session["usr"])
    else:
        return redirect(url_for('login'))

## CRUD PRODUCTOS

@app.route('/productos', methods=['GET', 'POST'])
def mostrar_productos():
    if "usr" in session:
        if request.method == 'POST':
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            precio_unitario = float(request.form['precio_unitario'])
            stock = int(request.form['stock'])

            if not nombre or precio_unitario is None or stock is None:
                flash('Todos los campos excepto la descripción son obligatorios.', 'alert-danger')
            else:
                cursor = db.cursor()

                query = "INSERT INTO productos (nombre, descripcion, precio_unitario, stock) VALUES (%s, %s, %s, %s)"
                values = (nombre, descripcion, precio_unitario, stock)
                cursor.execute(query, values)
                db.commit()

                flash('Celular/Productos agregado/s correctamente.', 'alert-success')

                cursor.close()

        cursor = db.cursor()

        cursor.execute("SELECT * FROM productos WHERE activo = TRUE")
        datos = cursor.fetchall()

        cursor.close()

        return render_template('mostrar_productos.html', datos=datos)
    else:
        return redirect(url_for('login'))
    
@app.route('/productos/delete/<int:id>')
def eliminar_productos(id):
    if "usr" in session:

        cursor = db.cursor()

        cursor.execute("SELECT * FROM productos WHERE id=%s", (id,))
        datos = cursor.fetchone()

        if datos is None:
            flash('Producto no encontrado', 'alert-danger')
            return redirect(url_for('mostrar_productos'))
        
        cursor.execute("UPDATE productos SET activo = FALSE WHERE id=%s", (id,))

        db.commit()
        flash('Producto eliminado', 'alert-success')
        cursor.close()

        return redirect(url_for('mostrar_productos'))
    else:
        return redirect(url_for('login'))
    
@app.route('/productos/update/<int:id>', methods=["GET", "POST"])
def actualizar_productos(id):
    if "usr" in session:

        cursor = db.cursor()


        cursor.execute(f"SELECT * FROM productos WHERE id={id}")
        datos = cursor.fetchone()

        if datos is None:
            flash('Producto no encontrado', 'alert-danger')
            return redirect(url_for('mostrar_productos'))

        if request.method == 'POST':
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            precio_unitario = float(request.form['precio_unitario'])
            stock = int(request.form['stock'])

            if not nombre or precio_unitario is None or stock is None:
                flash('Todos los campos excepto la descripción son obligatorios.', 'alert-danger')
            else:
                query = "UPDATE productos SET nombre = %s, descripcion = %s, precio_unitario = %s, stock = %s where id=%s"
                values = (nombre, descripcion, precio_unitario, stock, id)
                cursor.execute(query, values)
                db.commit()

                flash('Celular/Producto actualizado correctamente.', 'alert-success')
                return redirect(url_for('mostrar_productos'))

        return render_template('actualizar_productos.html', datos=datos)
    else:
        return redirect(url_for('login'))

## CRUD REPUESTOS

@app.route('/repuestos', methods=['GET', 'POST'])
def mostrar_repuestos():
    if "usr" in session:
        if request.method == 'POST':
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            precio_unitario = float(request.form['precio_unitario'])
            stock = int(request.form['stock'])

            if not nombre or precio_unitario is None or stock is None:
                flash('Todos los campos excepto la descripción son obligatorios.', 'alert-danger')
            else:
                cursor = db.cursor()

                query = "INSERT INTO repuestos (nombre, descripcion, precio_unitario, stock) VALUES (%s, %s, %s, %s)"
                values = (nombre, descripcion, precio_unitario, stock)
                cursor.execute(query, values)
                db.commit()

                flash('Repuesto/s agregado/s correctamente.', 'alert-success')

                cursor.close()

        cursor = db.cursor()

        cursor.execute("SELECT * FROM repuestos WHERE activo=TRUE")
        datos = cursor.fetchall()

        cursor.close()

        return render_template('mostrar_repuestos.html', datos=datos)
    else:
        return redirect(url_for('login'))


@app.route('/repuestos/delete/<int:id>')
def eliminar_repuestos(id):
    if "usr" in session:
    
        cursor = db.cursor()

        cursor.execute("SELECT * FROM repuestos WHERE id=%s", (id,))

        datos = cursor.fetchone()

        if datos is None:
            flash('Repuesto no encontrado', 'alert-danger')
            return redirect(url_for('mostrar_repuestos'))
        
        cursor.execute("UPDATE repuestos SET activo = FALSE WHERE id=%s", (id,))

        db.commit()
        flash('Repuesto eliminado', 'alert-success')
        cursor.close()

        return redirect(url_for('mostrar_repuestos'))
    else:
        return redirect(url_for('login'))

@app.route('/repuestos/update/<int:id>', methods=["GET", "POST"])
def actualizar_repuestos(id):
    if "usr" in session:

        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM repuestos WHERE id={id}")
        datos = cursor.fetchone()

        if datos is None:
            flash('Repuesto no encontrado', 'alert-danger')
            return redirect(url_for('mostrar_repuestos'))

        if request.method == 'POST':
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            precio_unitario = float(request.form['precio_unitario'])
            stock = int(request.form['stock'])

            if not nombre or precio_unitario is None or stock is None:
                flash('Todos los campos excepto la descripción son obligatorios.', 'alert-danger')
            else:
                query = "UPDATE repuestos SET nombre = %s, descripcion = %s, precio_unitario = %s, stock = %s where id=%s"
                values = (nombre, descripcion, precio_unitario, stock, id)
                cursor.execute(query, values)
                db.commit()

                flash('Repuesto actualizado correctamente.', 'alert-success')
                return redirect(url_for('mostrar_repuestos'))

        return render_template('actualizar_repuestos.html', datos=datos)
    else:
        return redirect(url_for('login'))


## CRUD CLIENTES

@app.route('/clientes', methods=['GET', 'POST'])
def mostrar_clientes():
    if "usr" in session:
        if request.method == 'POST':
            nombre = request.form['nombre']
            direccion = request.form['direccion']
            telefono = int(request.form['telefono'])

            if not nombre or direccion is None or telefono is None:
                flash('Todos los campos son obligatorios.', 'alert-danger')
            else:
                cursor = db.cursor()

                query = "INSERT INTO clientes (nombre, direccion, telefono) VALUES (%s, %s, %s)"
                values = (nombre, direccion, telefono)
                cursor.execute(query, values)
                db.commit()

                flash('Cliente agregado correctamente.', 'alert-success')

                cursor.close()

        cursor = db.cursor()

        cursor.execute("SELECT * FROM clientes")
        datos = cursor.fetchall()

        cursor.close()

        return render_template('mostrar_clientes.html', datos=datos)
    else:
        return redirect(url_for('login'))

@app.route('/clientes/update/<int:id>', methods=["GET", "POST"])
def actualizar_clientes(id):
    if "usr" in session:

        cursor = db.cursor()


        cursor.execute(f"SELECT * FROM clientes WHERE id={id}")
        datos = cursor.fetchone()

        if datos is None:
            flash('Cliente no encontrado', 'alert-danger')
            return redirect(url_for('mostrar_clientes'))

        if request.method == 'POST':
            nombre = request.form['nombre']
            direccion = request.form['direccion']
            telefono = int(request.form['telefono'])

            if not nombre or direccion is None or telefono is None:
                flash('Todos los campos son obligatorios.', 'alert-danger')
            else:
                query = "UPDATE clientes SET nombre = %s, direccion = %s, telefono = %s where id=%s"
                values = (nombre, direccion, telefono, id)
                cursor.execute(query, values)
                db.commit()

                flash('Clientes actualizado correctamente.', 'alert-success')
                return redirect(url_for('mostrar_clientes'))

        return render_template('actualizar_clientes.html', datos=datos)
    else:
        return redirect(url_for('login'))


## VENTAS

@app.route('/ventas', methods=["GET", "POST"])
def ventas():
    if "usr" in session:
        cursor = db.cursor()


        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()

        cursor.execute("SELECT * FROM productos WHERE activo=TRUE")
        productos = cursor.fetchall()


        if request.method == "POST":
            fecha_venta = request.form['fecha']
            datos_cliente = request.form['idclientes']
            datos_producto = request.form['producto_id']

            if not datos_cliente:
                flash('Debe seleccionar un cliente', 'alert-danger')
                cursor.close()
                return redirect(url_for('ventas'))


            if not datos_producto:
                flash('Debe seleccionar un producto', 'alert-danger')
                cursor.close()
                return redirect(url_for('ventas'))

            cantidad_producto = int(request.form['cantidad'])


            cursor.execute("SELECT stock FROM productos WHERE id=%s", (datos_producto,))
            stock_disponible = cursor.fetchone()[0]

            if cantidad_producto > stock_disponible:
                flash('La cantidad solicitada supera al stock disponible', 'alert-danger')
            else:
                nuevo_stock = stock_disponible - cantidad_producto
                if nuevo_stock == 0:
                    flash('No puedes quedarte con stock en cero, agrega mas stock', 'alert-danger')
                else:
                    cursor.execute("UPDATE productos SET stock = %s WHERE id = %s", (nuevo_stock, datos_producto))

                    cursor.execute("INSERT INTO ventas (fecha, cliente_id) VALUES (%s, %s)", (fecha_venta, datos_cliente))
                    venta_id = cursor.lastrowid

                    cursor.execute("INSERT INTO detalle_venta (venta_id, producto_id, cantidad) VALUES (%s, %s, %s)",
                            (venta_id, datos_producto, cantidad_producto))
                    

                    db.commit()

                    return redirect(url_for('venta_factura', id=venta_id))

        cursor.close() 
        return render_template('ventas.html', clientes=clientes, productos=productos)
    else:
        return redirect(url_for('login'))


@app.route('/ventas/factura/<int:id>', methods=["GET", "POST"])
def venta_factura(id):
    if "usr" in session:
        cursor = db.cursor()

        cursor.execute("SELECT ventas.id, ventas.fecha, clientes.nombre, clientes.direccion, clientes.telefono FROM ventas JOIN clientes ON ventas.cliente_id = clientes.id WHERE ventas.id = %s", (id,))
        venta_info = cursor.fetchone()

        cursor.execute("SELECT productos.nombre, productos.descripcion, detalle_venta.cantidad, productos.precio_unitario, productos.precio_unitario*detalle_venta.cantidad as subtotal FROM detalle_venta JOIN productos ON detalle_venta.producto_id = productos.id WHERE detalle_venta.venta_id = %s", (id,))
        detalles_venta = cursor.fetchall()

        if venta_info is None or detalles_venta is None:
            flash('Factura no encontrada', 'alert-danger')
            return redirect(url_for('index'))

        cursor.close()

        return render_template('venta_factura.html', venta_info=venta_info, detalles_venta=detalles_venta)
    else:
        return redirect(url_for('login'))

@app.route('/ventas/historial')
def historial_ventas():
    if "usr" in session:
        cursor = db.cursor()

        cursor.execute("SELECT ventas.id, ventas.fecha, clientes.nombre FROM ventas JOIN clientes ON ventas.cliente_id = clientes.id ORDER BY ventas.id DESC")
        historial_ventas = cursor.fetchall()

        cursor.close()

        return render_template('historial_ventas.html', historial_ventas=historial_ventas)
    else:
        return redirect(url_for('login'))

#REPARACION

@app.route('/reparaciones', methods=["GET", "POST"])
def reparaciones():
    if "usr" in session:
        cursor = db.cursor()

        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()

        cursor.execute("SELECT * FROM repuestos WHERE activo=TRUE")
        repuestos = cursor.fetchall()

        if request.method == "POST":
            fecha_emision = request.form['fecha']
            datos_cliente = request.form['idclientes']
            descripcion = request.form['descripcion']
            costo_labor = int(request.form['costo_labor'])
            datos_repuesto = request.form['repuesto_id']

            if not datos_cliente:
                flash('Debe seleccionar un cliente', 'alert-danger')
                cursor.close()
                return redirect(url_for('reparaciones'))

            if not datos_repuesto:
                flash('Debe seleccionar un repuesto', 'alert-danger')
                cursor.close()
                return redirect(url_for('reparaciones'))
            
            cantidad_repuesto = int(request.form['cantidad_repuesto'])

            cursor.execute("SELECT stock FROM repuestos WHERE id=%s", (datos_repuesto,))
            stock_disponible = cursor.fetchone()[0]

            if cantidad_repuesto > stock_disponible:
                flash('La cantidad solicitada supera al stock disponible', 'alert-danger')
            else:
                
                nuevo_stock = stock_disponible - cantidad_repuesto
                if nuevo_stock == 0:
                    flash('No puedes quedarte con stock en cero, agrega mas stock', 'alert-danger')
                else:
                    cursor.execute("UPDATE repuestos SET stock = %s WHERE id = %s", (nuevo_stock, datos_repuesto))

                    cursor.execute("INSERT INTO reparaciones (fecha, cliente_id, descripcion, costo_labor) VALUES (%s, %s, %s, %s)", (fecha_emision, datos_cliente, descripcion, costo_labor))
                    reparacion_id = cursor.lastrowid
                    
                    cursor.execute("INSERT INTO detalle_reparacion (reparacion_id, repuesto_id, cantidad) VALUES (%s, %s, %s)",
                            (reparacion_id, datos_repuesto, cantidad_repuesto))

                    db.commit()

                    return redirect(url_for('reparacion_factura', id=reparacion_id))


        return render_template('reparaciones.html', clientes=clientes, repuestos=repuestos)
    else:
        return redirect(url_for('login'))
    

@app.route('/reparaciones/factura/<int:id>')
def reparacion_factura(id):
    if "usr" in session:
        cursor = db.cursor()
        cursor.execute("SELECT reparaciones.id, reparaciones.fecha, clientes.nombre, clientes.direccion, clientes.telefono FROM reparaciones JOIN clientes ON reparaciones.cliente_id = clientes.id WHERE reparaciones.id = %s", (id,))
        reparacion_info = cursor.fetchone()

        cursor.execute("SELECT repuestos.nombre, repuestos.descripcion, reparaciones.descripcion, detalle_reparacion.cantidad, repuestos.precio_unitario, reparaciones.costo_labor, ((repuestos.precio_unitario*detalle_reparacion.cantidad)+reparaciones.costo_labor) FROM detalle_reparacion JOIN repuestos ON detalle_reparacion.repuesto_id = repuestos.id JOIN reparaciones ON detalle_reparacion.reparacion_id = reparaciones.id WHERE detalle_reparacion.reparacion_id = %s", (id,))
        detalles_reparacion = cursor.fetchall()


        if reparacion_info is None or detalles_reparacion is None:
            flash('Reparación no encontrada', 'alert-danger')
            return redirect(url_for('index'))

        cursor.close()

        return render_template('factura_reparacion.html', reparacion_info=reparacion_info, detalles_reparacion=detalles_reparacion)
    else:
        return redirect(url_for('login'))
    
@app.route('/reparaciones/historial')
def historial_reparaciones():
    if "usr" in session:
        cursor = db.cursor()

        cursor.execute("SELECT reparaciones.id, reparaciones.fecha, clientes.nombre FROM reparaciones JOIN clientes ON reparaciones.cliente_id = clientes.id ORDER BY reparaciones.id DESC")
        historial_reparaciones = cursor.fetchall()

        cursor.close()

        return render_template('historial_reparaciones.html', historial_reparaciones=historial_reparaciones)
    else:
        return redirect(url_for('login'))

#SESION

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if "usr" in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        usr = request.form['email']
        pwd = request.form['password']


        if usr and pwd:
            cursor = db.cursor()

            cursor.execute("SELECT * FROM usuario where username = %s", (usr,))
            usuarioExiste = cursor.fetchone()

            if usuarioExiste:
                flash('Ya existe una cuenta con ese correo electronico', 'alert-danger')
            else:
                cursor.execute("INSERT INTO usuario (username, password) VALUES (%s, %s)", (usr, pwd))
                db.commit()
                cursor.close()

                flash('Registro exitoso', "alert-success")
                return redirect(url_for('login'))
        else:
            flash('Debes ingresar datos', 'alert-danger')

    return render_template('signup.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if not "usr" in session:
        if request.method == 'POST':
            usr = request.form['username']
            pwd = request.form['password']
            cursor = db.cursor()
            cursor.execute("SELECT * FROM usuario WHERE username = %s AND password = %s", (usr, pwd))
            user = cursor.fetchone()
            cursor.close()
            if user:
                session["usr"]=usr
                return redirect(url_for('index'))
            else:
                flash('Datos incorrectos', "alert-danger")
                return redirect(url_for('login'))
    else:
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop("usr", None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug= True)
