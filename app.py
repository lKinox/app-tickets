from flask import Flask, render_template, request, redirect, url_for, send_file, make_response
from datetime import datetime, timedelta
import sqlite3
import json
import pdfkit
import io
import xlsxwriter
import ast


app = Flask(__name__)
DATABASE = 'facturas.db'

#conn = sqlite3.connect('facturas.db')
#cursor = conn.cursor()
#cursor.execute('''
#CREATE TABLE facturas (
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    nombre TEXT,
#    apellido TEXT,
#    productos TEXT,
#    total REAL,
#    fecha TEXT,
#    serial TEXT,
#    anulada TEXT,
#    fecha_anulacion TEXT,
#    pagada TEXT,
#    monto_pago TEXT
#        
#)
#''')
#conn.commit()
#conn.close()



granjita = [
    {'nombre': 'Delfín', 'imagen': '0.webp', 'origen': 'La Granjita'},
    {'nombre': 'Ballena', 'imagen': '00.webp', 'origen': 'La Granjita'},
    {'nombre': 'Carnero', 'imagen': '1.webp', 'origen': 'La Granjita'},
    {'nombre': 'Toro', 'imagen': '2.webp', 'origen': 'La Granjita'},
    {'nombre': 'Cienpiés', 'imagen': '3.webp', 'origen': 'La Granjita'},
    {'nombre': 'Alacrán', 'imagen': '4.webp', 'origen': 'La Granjita'},
    {'nombre': 'León', 'imagen': '5.webp', 'origen': 'La Granjita'},
    {'nombre': 'Rana', 'imagen': '6.webp', 'origen': 'La Granjita'},
    {'nombre': 'Perico', 'imagen': '7.webp', 'origen': 'La Granjita'},
    {'nombre': 'Ratón', 'imagen': '8.webp', 'origen': 'La Granjita'},
    {'nombre': 'Águila', 'imagen': '9.webp', 'origen': 'La Granjita'},
    {'nombre': 'Tigre', 'imagen': '10.webp', 'origen': 'La Granjita'},
    {'nombre': 'Gato', 'imagen': '11.webp', 'origen': 'La Granjita'},
    {'nombre': 'Caballo', 'imagen': '12.webp', 'origen': 'La Granjita'},
    {'nombre': 'Mono', 'imagen': '13.webp', 'origen': 'La Granjita'},
    {'nombre': 'Paloma', 'imagen': '14.webp', 'origen': 'La Granjita'},
    {'nombre': 'Zorro', 'imagen': '15.webp', 'origen': 'La Granjita'},
    {'nombre': 'Oso', 'imagen': '16.webp', 'origen': 'La Granjita'},
    {'nombre': 'Pavo ', 'imagen': '17.webp', 'origen': 'La Granjita'},
    {'nombre': 'Burro', 'imagen': '18.webp', 'origen': 'La Granjita'},
    {'nombre': 'Chivo', 'imagen': '19.webp', 'origen': 'La Granjita'},
    {'nombre': 'Cochino', 'imagen': '20.webp', 'origen': 'La Granjita'},
    {'nombre': 'Gallo', 'imagen': '21.webp', 'origen': 'La Granjita'},
    {'nombre': 'Camello', 'imagen': '22.webp', 'origen': 'La Granjita'},
    {'nombre': 'Cebra', 'imagen': '23.webp', 'origen': 'La Granjita'},
    {'nombre': 'Iguana', 'imagen': '24.webp', 'origen': 'La Granjita'},
    {'nombre': 'Gallina', 'imagen': '25.webp', 'origen': 'La Granjita'},
    {'nombre': 'Vaca', 'imagen': '26.webp', 'origen': 'La Granjita'},
    {'nombre': 'Perro', 'imagen': '27.webp', 'origen': 'La Granjita'},
    {'nombre': 'Zamuro', 'imagen': '28.webp', 'origen': 'La Granjita'},
    {'nombre': 'Elefante', 'imagen': '29.webp', 'origen': 'La Granjita'},
    {'nombre': 'Caimán', 'imagen': '30.webp', 'origen': 'La Granjita'},
    {'nombre': 'Lapa', 'imagen': '31.webp', 'origen': 'La Granjita'},
    {'nombre': 'Ardilla', 'imagen': '32.webp', 'origen': 'La Granjita'},
    {'nombre': 'Pescado', 'imagen': '33.webp', 'origen': 'La Granjita'},
    {'nombre': 'Venado', 'imagen': '34.webp', 'origen': 'La Granjita'},
    {'nombre': 'Jirafa', 'imagen': '35.webp', 'origen': 'La Granjita'},
    {'nombre': 'Culebra', 'imagen': '36.webp', 'origen': 'La Granjita'},
]

animalitos = [
    {'nombre': 'Delfín (0)', 'imagen': '0.webp', 'origen': 'Animalitos'},
    {'nombre': 'Ballena (00)', 'imagen': '00.webp', 'origen': 'Animalitos'},
    {'nombre': 'Carnero (1)', 'imagen': '1.webp', 'origen': 'Animalitos'},
    {'nombre': 'Toro (2)', 'imagen': '2.webp', 'origen': 'Animalitos'},
    {'nombre': 'Cienpiés (3)', 'imagen': '3.webp', 'origen': 'Animalitos'},
    {'nombre': 'Alacrán (4)', 'imagen': '4.webp', 'origen': 'Animalitos'},
    {'nombre': 'León (5)', 'imagen': '5.webp', 'origen': 'Animalitos'},
    {'nombre': 'Rana (6)', 'imagen': '6.webp', 'origen': 'Animalitos'},
    {'nombre': 'Perico (7)', 'imagen': '7.webp', 'origen': 'Animalitos'},
    {'nombre': 'Ratón (8)', 'imagen': '8.webp', 'origen': 'Animalitos'},
    {'nombre': 'Águila (9)', 'imagen': '9.webp', 'origen': 'Animalitos'},
    {'nombre': 'Tigre (10)', 'imagen': '10.webp', 'origen': 'Animalitos'},
    {'nombre': 'Gato (11)', 'imagen': '11.webp', 'origen': 'Animalitos'},
    {'nombre': 'Caballo (12)', 'imagen': '12.webp', 'origen': 'Animalitos'},
    {'nombre': 'Mono (13)', 'imagen': '13.webp', 'origen': 'Animalitos'},
    {'nombre': 'Paloma (14)', 'imagen': '14.webp', 'origen': 'Animalitos'},
    {'nombre': 'Zorro (15)', 'imagen': '15.webp', 'origen': 'Animalitos'},
    {'nombre': 'Oso (16)', 'imagen': '16.webp', 'origen': 'Animalitos'},
    {'nombre': 'Pavo (17)', 'imagen': '17.webp', 'origen': 'Animalitos'},
    {'nombre': 'Burro (18)', 'imagen': '18.webp', 'origen': 'Animalitos'},
    {'nombre': 'Chivo (19)', 'imagen': '19.webp', 'origen': 'Animalitos'},
    {'nombre': 'Cochino (20)', 'imagen': '20.webp', 'origen': 'Animalitos'},
    {'nombre': 'Gallo (21)', 'imagen': '21.webp', 'origen': 'Animalitos'},
    {'nombre': 'Camello (22)', 'imagen': '22.webp', 'origen': 'Animalitos'},
    {'nombre': 'Cebra (23)', 'imagen': '23.webp', 'origen': 'Animalitos'},
    {'nombre': 'Iguana (24)', 'imagen': '24.webp', 'origen': 'Animalitos'},
    {'nombre': 'Gallina (25)', 'imagen': '25.webp', 'origen': 'Animalitos'},
    {'nombre': 'Vaca (26)', 'imagen': '26.webp', 'origen': 'Animalitos'},
    {'nombre': 'Perro (27)', 'imagen': '27.webp', 'origen': 'Animalitos'},
    {'nombre': 'Zamuro (28)', 'imagen': '28.webp', 'origen': 'Animalitos'},
    {'nombre': 'Elefante (29)', 'imagen': '29.webp', 'origen': 'Animalitos'},
    {'nombre': 'Caimán (30)', 'imagen': '30.webp', 'origen': 'Animalitos'},
    {'nombre': 'Lapa (31)', 'imagen': '31.webp', 'origen': 'Animalitos'},
    {'nombre': 'Ardilla (32)', 'imagen': '32.webp', 'origen': 'Animalitos'},
    {'nombre': 'Pescado (33)', 'imagen': '33.webp', 'origen': 'Animalitos'},
    {'nombre': 'Venado (34)', 'imagen': '34.webp', 'origen': 'Animalitos'},
    {'nombre': 'Jirafa (35)', 'imagen': '35.webp', 'origen': 'Animalitos'},
    {'nombre': 'Culebra (36)', 'imagen': '36.webp', 'origen': 'Animalitos'},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    titulo = 'Productos'
    anio = 2023
    return render_template('productos.html', titulo=titulo, anio=anio, granja=granjita, animalitos=animalitos)

@app.route('/factura', methods=['POST'])
def factura():
    # Obtener los datos del formulario
    productos_dict = {}
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    for key, value in request.form.items():
        if key not in ['nombre', 'apellido', 'origen_granjita', 'origen_animalitos']:
            precio = float(value)
            if key in [producto['nombre'] for producto in granjita]:
                producto = next(filtro for filtro in granjita if filtro['nombre'] == key)
                origen = request.form.get('origen_granjita')
            elif key in [producto['nombre'] for producto in animalitos]:
                producto = next(filtro for filtro in animalitos if filtro['nombre'] == key)
                origen = request.form.get('origen_animalitos')
            print('Producto:', key, 'Origen:', origen)
            productos_dict[key] = {'precio': precio, 'origen': origen}
            producto['origen'] = origen
        

    
    # Calcular el total de la factura
    total = sum(producto['precio'] for producto in productos_dict.values())
    

    # Obtener el último número de serie de la base de datos
    conn = sqlite3.connect('facturas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(serial) FROM facturas')
    max_serial = cursor.fetchone()[0]
    if max_serial is None:
        max_serial = 0

    # Generar el número de serie de la factura
    serial = str(int(max_serial) + 1).zfill(8)


    # Generar la factura
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    factura = {
        'nombre': nombre,
        'apellido': apellido,
        'productos': productos_dict,
        'total': total,
        'fecha': fecha,
        'serial': serial
    }

    # Guardar la factura en la base de datos
    guardar_factura(serial, nombre, apellido, productos_dict, total, fecha)

    # Renderizar la plantilla de la factura
    return render_template('factura.html', factura=factura, productos=productos_dict)

def guardar_factura(serial, nombre, apellido, productos_dict, total, fecha):
    conn = sqlite3.connect('facturas.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS facturas (id INTEGER PRIMARY KEY AUTOINCREMENT, serial TEXT, nombre TEXT, apellido TEXT, productos TEXT, total REAL, fecha TEXT)')
    cursor.execute('INSERT INTO facturas (serial, nombre, apellido, productos, total, fecha) VALUES (?, ?, ?, ?, ?, ?)', (serial, nombre, apellido, str(productos_dict), total, fecha))
    conn.commit()
    conn.close()

@app.route('/facturas')
def facturas():
    conn = sqlite3.connect('facturas.db')
    cursor = conn.cursor()

    # Obtiene los valores de fecha desde el formulario
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')

    if fecha_desde and fecha_hasta:
        # Si hay valores de fecha, filtra las facturas por fecha
        cursor.execute('SELECT nombre, apellido, productos, total, fecha, serial, anulada, fecha_anulacion, pagada, monto_pago FROM facturas WHERE fecha BETWEEN ? AND ?', (fecha_desde, fecha_hasta))
    else:
        # Si no hay valores de fecha, obtiene todas las facturas
        cursor.execute('SELECT nombre, apellido, productos, total, fecha, serial, anulada, fecha_anulacion, pagada, monto_pago FROM facturas')

    filas = cursor.fetchall()
    facturas = []
    for fila in filas:
        nombre, apellido, productos_dict, total, fecha, serial, anulada, fecha_anulacion, pagada, monto_pago = fila
        productos_dict = productos_dict.replace("'", "\"")
        try:
            productos = json.loads(productos_dict)
        except json.JSONDecodeError:
            productos = ast.literal_eval(productos_dict)

        if monto_pago is not None and not anulada:
            monto_pago = float(monto_pago)
        else:
            monto_pago = 0.0
        facturas.append({
            'nombre': nombre,
            'apellido': apellido,
            'productos': productos,
            'total': total,
            'fecha': fecha,
            'serial': serial,
            'anulada': anulada,
            'fecha_anulacion': fecha_anulacion,
            'pagada': pagada,
            'monto_pago': monto_pago
        })

    conn.close()

    fecha_filtrada = ''
    if fecha_desde and fecha_hasta:
        # Si hay valores de fecha, muestra la fecha filtrada en la plantilla
        fecha_filtrada = f'{fecha_desde} - {fecha_hasta}'

    return render_template('facturas.html', facturas=facturas, fecha_filtrada=fecha_filtrada)


@app.route('/facturas/anular/<serial>', methods=['POST'])
def anular_factura(serial):
    conn = sqlite3.connect('facturas.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE facturas SET anulada = 1, fecha_anulacion = ? WHERE serial = ?', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), serial))
    conn.commit()
    conn.close()
    return redirect(url_for('facturas'))

@app.route('/facturas/pagar/<serial>', methods=['POST'])
def pagar_factura(serial):
    conn = sqlite3.connect('facturas.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE facturas SET pagada = 1, monto_pago = ? WHERE serial = ?', (float(request.form['producto_a_pagar']), serial))
    conn.commit()
    conn.close()
    return redirect(url_for('facturas'))

@app.route('/facturas/eliminar/<serial>', methods=['POST'])
def eliminar_factura(serial):
    conn = sqlite3.connect('facturas.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM facturas WHERE serial = ?', (serial,))
    conn.commit()
    conn.close()
    return redirect(url_for('facturas'))


def connect_db():
    return sqlite3.connect(DATABASE)

@app.route('/facturas/pdf/<serial>', methods=['GET','POST'])
def generar_pdf_factura(serial):
    conn = sqlite3.connect('facturas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, apellido, productos, total, fecha, serial FROM facturas WHERE serial = ?', (serial,))
    factura = cursor.fetchone()
    conn.close()

    # Convertir la lista de productos en un diccionario
    productos_dict = json.loads(factura[2].replace("'", "\""))

    # Renderizar la plantilla de la factura
    html = render_template('factura_pdf.html', factura=factura, productos=productos_dict)

    # Generar el PDF
    pdf = pdfkit.from_string(html, False, configuration=pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'))

    # Crear una respuesta HTTP con el archivo PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={factura[5]}.pdf'

    return response

@app.route('/pdf/<serial>')
def descargar_pdf(serial):
    ruta_pdf = generar_pdf_factura(serial)
    return send_file(ruta_pdf, as_attachment=True)

@app.route('/descargar_excel', methods=['POST'])
def descargar_excel():
    conn = sqlite3.connect('facturas.db')
    cursor = conn.cursor()

    fecha_desde = request.form['fecha_desde']
    fecha_hasta = request.form['fecha_hasta']

    if fecha_desde and fecha_hasta:
        cursor.execute('SELECT nombre, apellido, productos, total, fecha, serial, anulada, fecha_anulacion, pagada, monto_pago FROM facturas WHERE fecha BETWEEN ? AND ?', (fecha_desde, fecha_hasta))
    else:
        cursor.execute('SELECT nombre, apellido, productos, total, fecha, serial, anulada, fecha_anulacion, pagada, monto_pago FROM facturas')

    filas = cursor.fetchall()
    facturas = []
    for fila in filas:
        nombre, apellido, productos_dict, total, fecha, serial, anulada, fecha_anulacion, pagada, monto_pago = fila
        productos_dict = productos_dict.replace("'", "\"")
        try:
            productos = json.loads(productos_dict)
        except json.JSONDecodeError:
            productos = ast.literal_eval(productos_dict)
        facturas.append({
            'nombre': nombre,
            'apellido': apellido,
            'productos': productos,
            'total': total,
            'fecha': fecha,
            'serial': serial,
            'anulada': anulada,
            'fecha_anulacion': fecha_anulacion,
            'pagada': pagada,
            'monto_pago': monto_pago
        })

    conn.close()

    # Crear un archivo Excel en memoria
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Escribir encabezados de columna
    columnas = ['Nombre', 'Apellido', 'Productos', 'Total', 'Fecha', 'Serial', 'Anulada', 'Fecha de anulación', 'Pagada', 'Monto de pago']
    for i, columna in enumerate(columnas):
        worksheet.write(0, i, columna)

    # Escribir filas de datos
    for i, factura in enumerate(facturas):
        anulada = "Sí" if factura['anulada'] else "No"
        pagada = "Sí" if factura['pagada'] else "No"
        monto_pago = float(factura['monto_pago']) * 30 if factura['monto_pago'] else 0
        productos = ', '.join([f"{producto} - Bs{precio}" for producto, precio in factura['productos'].items()])
        worksheet.write(i+1, 0, factura['nombre'])
        worksheet.write(i+1, 1, factura['apellido'])
        worksheet.write(i+1, 2, productos)
        worksheet.write(i+1, 3, factura['total'])
        worksheet.write(i+1, 4, factura['fecha'])
        worksheet.write(i+1, 5, factura['serial'])
        worksheet.write(i+1, 6, anulada)
        worksheet.write(i+1, 7, factura['fecha_anulacion'])
        worksheet.write(i+1, 8, pagada)
        worksheet.write(i+1, 9, monto_pago)

    workbook.close()

    # Enviar archivo Excel al usuario
    output.seek(0)
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='facturas.xlsx')

if __name__ == "__main__":
    app.run(debug=True)
