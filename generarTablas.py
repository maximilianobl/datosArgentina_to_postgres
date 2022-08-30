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

provincias = requests.get('https://infra.datos.gob.ar/catalog/modernizacion/dataset/7/distribution/7.2/download/provincias.json').json()
departamentos = requests.get('https://infra.datos.gob.ar/catalog/modernizacion/dataset/7/distribution/7.3/download/departamentos.json').json()
localidades = requests.get('https://infra.datos.gob.ar/catalog/modernizacion/dataset/7/distribution/7.27/download/localidades-censales.json').json()
calles = requests.get('https://infra.datos.gob.ar/catalog/modernizacion/dataset/7/distribution/7.6/download/calles.json').json()

# Elimino las tablas para generarlas con info nueva
dropTable = """
DROP TABLE IF EXISTS Calles;
DROP TABLE IF EXISTS Localidades;
DROP TABLE IF EXISTS Departamentos;
DROP TABLE IF EXISTS Provincias;
"""
cursor.execute(dropTable)

# Creación tabla provincias
crearTablaProvincias = """
CREATE TABLE Provincias (
  id int NOT NULL,
  nombre varchar(255) NOT NULL,
  PRIMARY KEY (id)
)"""
cursor.execute(crearTablaProvincias)


# For loop para hacer insert de cada provincia
for provincia in provincias['provincias']:
    nombre = provincia['nombre']
    id = provincia['id']
    print(f'Provincias ==> id: {id}, nombre: {nombre}')
    query = "INSERT INTO public.Provincias (id, nombre) VALUES (%s, %s)"
    data = [(id, nombre)]
    cursor.executemany(query, data)    
    conn.commit()
    #conn.close()


# Creación tabla departamentos
crearTablaDepartamentos = """
CREATE TABLE Departamentos (
  id int NOT NULL,
  nombre varchar(255) NOT NULL,
  categoria varchar(255) NOT NULL,
  id_provincia int,
  CONSTRAINT departamentos_fk FOREIGN KEY (id_provincia) REFERENCES public.provincias(id),
  PRIMARY KEY (id)
)"""
cursor.execute(crearTablaDepartamentos)

# For loop para hacer insert de cada Departamento
for departamento in departamentos['departamentos']:
    nombre = departamento['nombre']
    id = departamento['id']
    id_provincia = departamento['provincia']['id']
    categoria = departamento['categoria']
    print(f'Departamentos ==> id: {id}, nombre: {nombre}, id_provincia: {id_provincia}')
    query = "INSERT INTO public.Departamentos (id, nombre, categoria, id_provincia) VALUES (%s, %s, %s, %s)"
    data = [(id, nombre, categoria, id_provincia)]
    cursor.executemany(query, data)
    conn.commit()
    #conn.close()


# Creación tabla localidades
crearTablaLocalidades = """
CREATE TABLE Localidades (
  id int NOT NULL,
  nombre varchar(255) NOT NULL,
  id_departamento int,
  latitud varchar(255) NOT NULL,
  longitud varchar(255) NOT NULL,
  CONSTRAINT localidades_fk FOREIGN KEY (id_departamento) REFERENCES public.Departamentos(id),
  PRIMARY KEY (id)
)"""
cursor.execute(crearTablaLocalidades)

# For loop para hacer insert de cada Localidad
for localidad in localidades['localidades-censales']:
    nombre = localidad['nombre']
    id = localidad['id']
    id_departamento = localidad['departamento']['id']
    latitud = localidad['centroide']['lat']
    longitud = localidad['centroide']['lon']
    print(f'Localidades ==> id: {id}, nombre: {nombre}, id_departamento: {id_departamento}')
    query = "INSERT INTO public.Localidades (id, nombre, id_departamento, latitud, longitud) VALUES (%s, %s, %s, %s, %s)"
    data = [(id, nombre, id_departamento, latitud, longitud)]
    cursor.executemany(query, data)
    conn.commit()
    #conn.close()


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