import json
import requests
import psycopg2

# En las siguientes lineas va la información del servidor y la db donde se quieran crear las tablas
conn = psycopg2.connect(
          database="demo",
          host="localhost",
          port=5432,
          user="postgres", 
          password="postgres"
        )
cursor = conn.cursor()

calles = requests.get('https://infra.datos.gob.ar/catalog/modernizacion/dataset/7/distribution/7.6/download/calles.json').json()

# Elimino las tablas para generarlas con info nueva
dropTable = """
DROP TABLE IF EXISTS Calles;
"""
cursor.execute(dropTable)

# Creación tabla calles
crearTablaCalles = """
CREATE TABLE Calles (
  id bigint NOT NULL,
  nombre varchar(255) NOT NULL,
  id_localidad int,
  categoria varchar(255) NOT NULL,
  alt_ini_izq bigint,
  alt_ini_der bigint,
  alt_fin_izq bigint,
  alt_fin_der bigint,
  CONSTRAINT calles_fk FOREIGN KEY (id_localidad) REFERENCES public.Localidades(id),
  PRIMARY KEY (id)
)"""
cursor.execute(crearTablaCalles)

# For loop para hacer insert de cada Calle
for calle in calles['calles']:
    nombre = calle['nombre']
    id = calle['id']
    id_localidad = calle['localidad_censal']['id']
    categoria = calle['categoria']
    alt_ini_izq = calle['altura']['inicio']['izquierda']
    alt_ini_der = calle['altura']['inicio']['derecha']
    alt_fin_izq = calle['altura']['fin']['izquierda']
    alt_fin_der = calle['altura']['fin']['derecha']
    print(f'Calles ==> id: {id}, nombre: {nombre}, id_localidad: {id_localidad}, categoria: {categoria}')
    query = "INSERT INTO public.Calles (id, nombre, id_localidad, categoria, alt_ini_izq, alt_ini_der, alt_fin_izq, alt_fin_der) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    data = [(id, nombre, id_localidad, categoria, alt_ini_izq, alt_ini_der, alt_fin_izq, alt_fin_der)]
    cursor.executemany(query, data)
    conn.commit()
    #conn.close()