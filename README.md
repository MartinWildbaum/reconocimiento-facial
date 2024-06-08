# Proyecto de Reconocimiento Facial

Este proyecto implementa un sistema de autenticación mediante reconocimiento facial utilizando Flask y una base de datos PostgreSQL. Los usuarios pueden registrarse proporcionando su correo electrónico, contraseña e imagen, y luego iniciar sesión de forma tradicional o mediante reconocimiento facial.

## Requisitos

- Python 3.12
- PostgreSQL
- Virtualenv

## Instalación

### 1. Clonar el Repositorio

```
git clone https://github.com/tu-usuario/reconocimiento-facial.git
cd reconocimiento-facial
```
### 2. Crear y Activar un Entorno Virtual
En macOS/Linux:

```
source venv/bin/activate
```
En Windows:

```
venv\Scripts\activate
```

### 3. Configurar la Base de Datos PostgreSQL
Inicia PostgreSQL y crea una base de datos:

```
sudo -i -u postgres
createdb reconocimiento_facial
createuser --interactive  # Crea un usuario y dale los permisos necesarios
```
Configura el acceso al usuario desde PostgreSQL y asegúrate de que tenga permisos suficientes en la base de datos creada.

### 4. Crear Archivos Estáticos
Descargar los modelos de face-api.js y colocarlos en la carpeta static/models.

```
mkdir -p static/models
cd static/models
wget https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_recognition_model-shard1
wget https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_recognition_model-shard2
wget https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_recognition_model-weights_manifest.json
wget https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_landmark_68_model-shard1
wget https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_landmark_68_model-weights_manifest.json
wget https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/tiny_face_detector_model-shard1
wget https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/tiny_face_detector_model-weights_manifest.json
```
### 5. Configuración de la Aplicación
Asegúrate de que las variables de configuración de la base de datos en app.py están correctamente configuradas:

python
```
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tu_usuario:tu_contraseña@localhost/reconocimiento_facial'
```
### 6. Iniciar la Aplicación

```
python app.py
```
La aplicación debería estar corriendo en http://127.0.0.1:5000.

## Uso
### Registro de Usuario
1. Navega a http://127.0.0.1:5000/sign_up.
2. Completa el formulario con tu correo electrónico, contraseña y una imagen.
3. Haz clic en "Registrarse".
### Inicio de Sesión

**Inicio de Sesión Tradicional**
1. Navega a http://127.0.0.1:5000/sign_in.
2. Completa el formulario con tu correo electrónico y contraseña.
3. Haz clic en "Ingresar".

**Inicio de Sesión con Reconocimiento Facial**
1. Navega a http://127.0.0.1:5000/sign_in.
2. Ingresa tu correo electrónico.
3. Haz clic en "Ingresar con Reconocimiento Facial".
4. Permite el acceso a la cámara y espera a que se realice el reconocimiento facial.
## Herramientas Utilizadas
### Flask
Flask es un microframework para Python que se utiliza para construir aplicaciones web. Es conocido por su simplicidad y flexibilidad. Flask proporciona las herramientas y bibliotecas necesarias para construir una aplicación web robusta sin demasiada sobrecarga. Algunas características clave incluyen:

- Enrutamiento: Define rutas de URL y asigna funciones para manejar las solicitudes.
- Plantillas: Usa Jinja2 para renderizar HTML dinámico.
- Manejo de solicitudes: Facilita el manejo de solicitudes HTTP (GET, POST, etc.).
- Extensibilidad: Permite añadir extensiones para funcionalidad adicional (por ejemplo, Flask-SQLAlchemy).
### PostgreSQL
PostgreSQL es un sistema de gestión de bases de datos relacional de código abierto. Es conocido por su robustez, flexibilidad y conformidad con los estándares SQL. Algunas características importantes de PostgreSQL incluyen:

- Integridad transaccional: Garantiza la consistencia de los datos a través de transacciones ACID.
- Soporte para tipos de datos avanzados: Incluye JSON, XML, y más.
- Extensibilidad: Permite la creación de funciones personalizadas, tipos de datos y operadores.
- Seguridad: Ofrece autenticación robusta y control de acceso.
### SQLAlchemy
SQLAlchemy es una biblioteca de ORM (Object-Relational Mapping) para Python que facilita la interacción con bases de datos relacionales de una manera más intuitiva y eficiente. Algunas características clave incluyen:

- Mapeo de objetos a tablas: Permite definir modelos de datos en Python que se mapean a tablas en una base de datos.
- Consultas SQL avanzadas: Proporciona una API para construir consultas SQL complejas.
- Manejo de sesiones: Facilita la gestión de transacciones y conexiones a la base de datos.
- Compatibilidad con múltiples motores de bases de datos: Soporta PostgreSQL, MySQL, SQLite, entre otros.
### face-api.js
face-api.js es una biblioteca JavaScript para el reconocimiento facial en el navegador. Está construida sobre TensorFlow.js y proporciona modelos preentrenados para detectar y reconocer rostros en imágenes y videos. Algunas características clave incluyen:

- Detección de rostros: Identifica la presencia de rostros en imágenes y videos.
- Reconocimiento facial: Compara y reconoce rostros en función de las características faciales.
- Detección de puntos clave: Identifica y rastrea puntos clave en la cara, como ojos, nariz y boca.
- Soporte para el navegador: Funciona directamente en el navegador sin necesidad de un servidor backend.
### face_recognition
face_recognition es una biblioteca de Python para el reconocimiento facial basada en dlib. Proporciona una API simple para detectar, reconocer y manipular rostros en imágenes. Algunas características importantes incluyen:

- Codificación de rostros: Convierte una imagen de un rostro en una representación matemática.
- Comparación de rostros: Compara codificaciones faciales para determinar si dos rostros son de la misma persona.
- Detección de rostros: Localiza la posición de rostros en una imagen.
- Interfaz simple: Ofrece una API fácil de usar que simplifica el desarrollo de aplicaciones de reconocimiento facial.
## Estructura del Proyecto
```
reconocimiento-facial/
├── static/
│   ├── js/
│   │   └── sign_in.js
│   └── models/
│       ├── face_recognition_model-shard1
│       ├── face_recognition_model-shard2
│       ├── face_recognition_model-weights_manifest.json
│       ├── face_landmark_68_model-shard1
│       ├── face_landmark_68_model-weights_manifest.json
│       ├── tiny_face_detector_model-shard1
│       └── tiny_face_detector_model-weights_manifest.json
├── templates/
│   ├── home.html
│   ├── sign_in.html
│   └── sign_up.html
├── uploads/
│   └── (uploaded images)
├── app.py
├── requirements.txt
└── README.md
```
## Ejemplo de uso del sistema


https://github.com/MartinWildbaum/reconocimiento-facial/assets/85357588/345f4ec4-63df-4fb9-82d1-59b506844dab



