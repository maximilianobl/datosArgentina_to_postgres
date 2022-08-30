# datosArgentina_to_postgres
Script Python para pasearlos e insertarlos en una base de datos PostgreSQL. Los datos son tomados desde la web oficial de datos abiertos: https://datosgobar.github.io/georef-ar-api/

# datosArgentina
Creación de tablas "Provincias", "Departamentos", "Localidades" y "Calles" en una base de datos PostgreSQL con psycopg2

El script fue generado con python 3 y crea (las dropea si existen previamente) las tablas 'Provincias', 'Departamentos', 'Localidades' y 'Calles', así como también las relaciones de FK entre ellas en una base de datos PostgreSQL utilizando la librería psycopg2.

Los datos son tomados de un JSON provisto por el gobierno.

En la sección luego de los imports deben especificarse los datos del servidor y db donde se quieran crear las tablas.

Nota: la localidad 'Ciudad Autónoma de Buenos Aires' no está ligada a ningún departamento (FK NULL) ya que así se encuentra en el JSON del gobierno. En el JSON esta localidad esta ligada a la Provincia 'Ciudad Autónoma de Buenos Aires', pero en las tablas generadas no existe esa relación.

# Requerimientos
* Python 3
* psycopg2 (Versión 2.9.3): https://www.psycopg.org/docs/install.html

# Ejecución
* docker-compose up -d --> para ejecutar un contenedor con una base de datos PostgreSQL:9.6, luego se deberá crear una base de datos "demo".
* python3 generarTablas.py --> genera todas las tablas.
* python3 generarCalles.py --> genera solo la tabla de calles, dado que contiene mucha informiación.