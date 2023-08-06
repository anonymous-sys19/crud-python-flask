from flask import Flask, render_template, request, redirect, url_for, session
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'tu_clave_secreta'  # Reemplaza 'tu_clave_secreta' por una clave secreta segura

# Rutas de la aplicación
@app.route('/') 
def home():
    if 'username' in session:
        cursor = db.database.cursor()
        cursor.execute("SELECT * FROM users")
        myresult = cursor.fetchall()
        # Convertir los datos a diccionarioooo
        insertObject = []
        columnNames = [column[0] for column in cursor.description]
        for record in myresult:
            insertObject.append(dict(zip(columnNames, record)))
        cursor.close()
        return render_template('index.html', data=insertObject)
    else:
        return redirect(url_for('login'))


# Ruta para guardar usuarios en la bdd
@app.route('/user', methods=['POST'])
def addUser():
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']

    if username and name and password:
        cursor = db.database.cursor()
        sql = "INSERT INTO users (username, name, password) VALUES (%s, %s, %s)"
        data = (username, name, password)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))


@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM users WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))


@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']

    if username and name and password:
        cursor = db.database.cursor()
        sql = "UPDATE users SET username = %s, name = %s, password = %s WHERE id = %s"
        data = (username, name, password, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar las credenciales en la base de datos
        cursor = db.database.cursor()
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        data = (username, password)
        cursor.execute(sql, data)
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Credenciales válidas, iniciar sesión exitosamente
            # Establecer la variable de sesión para mantener al usuario logeado
            session['username'] = username
            return redirect(url_for('home'))
        else:
            # Credenciales inválidas, mostrar mensaje de error en la página de inicio de sesión
            error = "Nombre de usuario o contraseña incorrectos"
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/logout')
def logout():
    # Remover la variable de sesión para cerrar la sesión del usuario
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=4000)
