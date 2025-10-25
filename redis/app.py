from flask import Flask, render_template, request, redirect, url_for
import redis

# 1. Configuración
# Le decimos a Flask que busque el HTML en el mismo directorio ('.')
app = Flask(__name__, template_folder='.')

# Conectamos a Redis (asegúrate que tu servidor en WSL esté corriendo)
try:
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    r.ping()
    print("¡Conectado a Redis!")
except redis.exceptions.ConnectionError as e:
    print(f"No se pudo conectar a Redis: {e}")
    exit()


# 2. Rutas del CRUD

@app.route('/')
def index():
    """
    (READ) - Leer todas las tareas.
    """
    # Usamos LRANGE para obtener todas las tareas de la lista 'tareas'
    lista_de_tareas = r.lrange('tareas', 0, -1)
    
    # render_template buscará 'index.html' en la misma carpeta
    return render_template('index.html', tareas=lista_de_tareas)


@app.route('/add', methods=['POST'])
def add_task():
    """
    (CREATE) - Añadir una nueva tarea.
    """
    nueva_tarea = request.form.get('tarea')
    if nueva_tarea:
        # Usamos RPUSH para añadir la nueva tarea AL FINAL de la lista
        r.rpush('tareas', nueva_tarea)
        
    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete_task():
    """
    (DELETE) - Borrar una tarea.
    """
    tarea_a_borrar = request.form.get('tarea_a_borrar')
    if tarea_a_borrar:
        # Usamos LREM para borrar la tarea de la lista.
        r.lrem('tareas', 0, tarea_a_borrar)
        
    return redirect(url_for('index'))


# 3. Ejecutor
if __name__ == '__main__':
    app.run(debug=True, port=5000)