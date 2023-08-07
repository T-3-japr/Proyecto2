import pymongo
import json


def menu_inicial():
    """
    Esta es una función para hacer el proyecto un poco más amigable. Vamos a presentar un menú
    con las diferentes opciones. En el main, se generará un bucle para ir haciéndolas todas
    :return: Devuelve la opción elegida
    """
    print('\nBienvenido a su Playlist favorita!!\n')
    print('\tIntroduzca la opción que desea hacer: ')
    print('\t\tPulse 0 para salir: ')
    print('\t\tPulse 1 para crear una base de datos: ')
    print('\t\tPulse 2 para crear un usuario: ')
    print('\t\tPulse 3 para consultar a un usuario: ')
    print('\t\tPulse 4 para dar de alta una canción: ')
    print('\t\tPulse 5 para consultar una canción: ')
    print('\t\tPulse 6 para crear una playlist: ')
    print('\t\tPulse 7 para consultar una playlist: ')
    print('\t\tPulse 8 para añadir una canción a su playlist: ')
    print('\t\tPulse 9 para rellenar con 50 canciones: ')
    print('\t\tPulse 10 para repartir las 50 canciones: ')
    print('\t\tPulse 11 para usar el método mostrar 20 canciones al azar: ')
    print('\t\tPulse 12 para usar el método para añadir una de las canciones anteriores: ')
    print('\t\tPulse 13 para usar el método para mostrar las canciones de una playlist: ')
    opcion = input('\n\tIntroduca la opción deseada: ')
    return opcion


def crear_base_datos():
    """
    Esta fución es espcífica para crear y abrir la base de datos.
    :return: No devuelve nada. Simplemente, la compone e indica si ya estaba hecha. Pase lo que pase, al final la cierra
    """
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017")  # Se conecta a MongoDB Compass
        db = client.musicplaylist                                  # Creamos base de datos y asociamos a la variable db
        db.create_collection("Usuario")                            # Creamos las colecciones
        db.create_collection("Canciones")
        db.create_collection("Playlist")
        print('\n\t\tBase de datos creada!!')
    except Exception as error:                                     # Si se produce algún error, se imprimirá dicho error
        print("Ha ocurrido el error: ", error)
    finally:
        client.close()                                             # Siempre se cierra la conexión


def crear_usuario():
    """
    Con esta función, vamos a dar de alta a los usuarios. Utilizaremos un diccionario que lo recorreremos
    mediante un for para ir rellenándolo
    El índice de esta colección será el Username, ya que debe ser algo único
    :return: Esta función no devuelve nada, pide los datos, abre la conexión, los guarda y cierra la conexión
    """
    client = pymongo.MongoClient("mongodb://localhost:27017")
    # Abrimos la conexión
    db = client.musicplaylist
    datos = {'Nombre': None, 'Apellido': None, 'Username': None, 'e-mail': None}
    # Creamos un dict con las claves como los campos de la colección. Los Valores se irán rellenando
    for dato in datos:
        # Creado para rellenar los valores del diccionario según se piden por teclado
        valor = input(f'\n\tIntroduzca su {dato}: ')
        # Pedimos el valor por teclado
        datos.update({dato: valor})
        # Actualizamos el dict
    cursor = db.Usuario.find_one({"_id": datos['Username']})
    # Creamos un cursor para que busque el nombre del usuario.
    if cursor is None:
        # Si no lo encuentra, rellenamos los campos con los datos del diccionario.
        # Utilizaremos la variable user para almacenar temporalmente la información en formato bson
        user = ([{
            "_id": datos['Username'],
            "nombre": datos['Nombre'],
            "apellidos": datos['Apellido'],
            "e-mail": datos['e-mail'],
        }])
        db.Usuario.insert_many(user)
        # Insertamos la información en la clección Usuario
    else:
        print(f"El usuario {datos['Username']} ya existe...")
        # Si el nombre de usuario se repite, muestra esta información
    client.close()
    # Cerramos la conexión


def consulta_usuario():
    """
    La función anterior ha creado usuarios. Con esta, se recuperará la información del
    usuario que se desee conocer
    :return: Al igual que la anterior función, esta no devuelve nada, actúa por sí sola
    """
    print('\n\t\tPulse 1 si desea buscar por user name: ')
    # Le presentamos un menú de opciones
    print('\n\t\tPulse 2 si desea buscar por nombre y apellidos: ')
    print('\n\t\tPulse 3 si desea buscar por e-mail: ')
    print('\n\t\tPulse 0 para salir: ')
    client = pymongo.MongoClient("mongodb://localhost:27017")
    # Nos conectamos
    db = client.musicplaylist
    while True:
        # Generamos un bucle infinito que se corará al pursar el 0
        opcion = input('\n\t\tIntroduzca su opción de búsqueda: ')
        # Pedimos la opción de búsqueda
        if opcion == '1':
            # Y según la opción elegida, abrimos un cursor que busque la coincidencia con la opción elegida
            n = input('\n\tIntroduzca el nombre de usuario: ')
            # Luego mediante un for, mostramos los resultados obtenidos
            cursor = db.Usuario.find({'_id': n})
            # Esto se repite con las 3 opciones dadas
            for dato in cursor:
                print(f'\n\t\tEl usuario es: {dato["nombre"]} {dato["apellidos"]}, con el correo: {dato["e-mail"]}')
        elif opcion == '2':
            n = input('\n\tIntroduzca el nombre y apellidos: ')
            cursor = db.Usuario.find({'nombre': n})
            for dato in cursor:
                print(f'\n\t\tSu nombre de usuario es: {dato["_id"]} y su correo: {dato["e-mail"]}')
        elif opcion == '3':
            n = input('\n\tIntroduzca el correo electrónico: ')
            cursor = db.Usuario.find({'e-mail': n})
            for dato in cursor:
                print(f'\n\t\tEl usuario es: {dato["nombre"]} {dato["apellidos"]} y su nombre de usuario es: '
                      f'{dato["_id"]}')
        elif opcion == '0':
            break
            # Rompemos el bucle while
        else:
            print('Opción incorrecta')
            # Mostramos mensaje si se ha introducido opción inválida
    client.close()
    # Cerramos la conexión


def crear_cancion():
    """
    La estructura de esta función es similar a las anteriores. Creamos un diccionario, lo recorremos con
    un for para rellenarlo y lo guardamos en la colección.
    El id de esta colección va a ser el título de la canción. Pienso que es el dato más excluyente.
    :return: No retorna nada
    """
    datos = {'Título': None, 'Cantante': None, 'Genero': None, 'Album': None, 'Url': None}
    # Creamos un dict con las claves como los campos de la colección. Los Valores se irán rellenando
    client = pymongo.MongoClient("mongodb://localhost:27017")
    # Conectamos a la base de datos
    db = client.musicplaylist
    for dato in datos:  # Creado para rellenar los valores del diccionario según se piden por teclado
        valor = input(f'Introduzca el {dato}: ')  # Pedimos el valor por teclado
        datos.update({dato: valor})  # Actualizamos el dict
    user = ([{
        "_id": datos['Título'],
        "cantante": datos['Cantante'],
        "genero": datos['Genero'],
        "album": datos['Album'],
        "url": datos['Url']
    }])
    # Pasamos los datos del diccionario a formato bson
    db.Canciones.insert_many(user)  # Insertamos la información en la clección Usuario
    client.close()
    # Cerramos  conexión


def consulta_cancion():
    """
    Creamos un menú de búquedas y según la opción elegida, mostrará el resto de la colección
    :return: No devuelve nada
    """
    print('Pulse 1 si desea buscar por título de canción: ')  # Le presentamos un menú de opciones
    print('Pulse 2 si desea buscar por cantante: ')
    print('Pulse 3 si desea buscar por genero de música: ')
    print('Pulse 4 si desea buscar por álbum: ')
    print('Pulse 5 si desea buscar por url: ')
    print('Pulse 0 para salir: ')
    client = pymongo.MongoClient("mongodb://localhost:27017")
    # Abrimos conexión
    db = client.musicplaylist
    while True:  # Generamos un bucle infinito que se corará al pursar el 0
        opcion = input('Introduzca su opción de búsqueda: ')  # Pedimos la opción de búsqueda
        if opcion == '1':
            # Y según la opción elegida, abrimos un cursor que busque la coincidencia con la opción elegida
            n = input(
                'Introduzca el título de la canción: ')  # Luego mediante un for, mostramos los resultados obtenidos
            cursor = db.Canciones.find({'_id': n})  # Esto se repite con las 5 opciones dadas
            for dato in cursor:
                print(
                    f'El título pertenece al álbum: {dato["album"]}, del grupo o solista:'
                    f' {dato["cantante"]}, de género {dato["genero"]}'
                    f' y su enlace es: {dato["url"]}')
        elif opcion == '2':
            n = input('Introduzca el título del cantante o grupo: ')
            cursor = db.Canciones.find({'cantante': n})
            for dato in cursor:
                print(
                    f'El cantante o grupo tiene la canción: {dato["_id"]},'
                    f' del álbum: {dato["album"]}, de género {dato["genero"]} y su enlace es: {dato["url"]}')
        elif opcion == '3':
            n = input('Introduzca el género de música que busca: ')
            cursor = db.Canciones.find({'genero': n})
            for dato in cursor:
                print(
                    f'Del género {dato["genero"]} hay: {dato["_id"]}, '
                    f'del álbum: {dato["album"]}, del cantante o grupo {dato["cantante"]}'
                    f' y su enlace es: {dato["url"]}')
        elif opcion == '4':
            n = input('Introduzca el nombre del álbum: ')
            cursor = db.Canciones.find({'album': n})
            for dato in cursor:
                print(
                    f'Del álbum: {dato["album"]} hay: {dato["_id"]}, '
                    f'del cantante o grupo {dato["cantante"]}, de género álbum: {dato["genero"]}'
                    f' y su enlace es: {dato["url"]}')
        elif opcion == '5':
            n = input('Introduzca la url que desea buscar: ')
            cursor = db.Canciones.find({'url': n})
            for dato in cursor:
                print(
                    f'De la URL: {dato["url"]} hay: la canción {dato["_id"]},'
                    f' del álbum {dato["album"]}, del cantante o grupo {dato["cantante"]},'
                    f' de género álbum: {dato["genero"]}')
        elif opcion == '0':
            break  # Rompemos el bucle while
        else:
            print('Opción incorrecta')  # Mostramos mensaje si se ha introducido opción inválida
    client.close()
    # Cerramos conexión


def crear_playlist():
    """
    Esta función es la que me ha dado más problemas. El tema del Array. Se le introducirá un nombre
    de lista, el nombre de usuario a quien pertenece y el título de una canción. Este título lo buscará
    en la colección de Canciones. Si lo encuentra, lo añade, si no lo encuentra, lo ignora.
    :return: No devuelve nada
    """
    datos = {'Nombre lista': None, 'Username': None,
             'Canciones': []}
    # Creamos un diccionario para almacenar información. Dentro de este diccionario se crea una lista
    # donde se almacenrán las canciones de la playlist. Poniéndolo de esta forma, Mongo lo
    # lo interperta como un Array y funciona perfectamente. Si se deja como parte del diccionario, lo considera
    # como Objeto y no se le pueden ampliar más canciones
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client.musicplaylist
    for dato in datos:  # Con este for vamos rellenando el diccionario con los datos introducidos por teclado
        if dato == 'Canciones':  # Con este if selecciono el campo Canciones
            valor = input(f'Introduzca el título de la canción: ')
            cursor = db.Canciones.find(
                {'_id': valor})  # Busco en la colección Canciones, el título introducido previamente
            for i in cursor:
                datos.update({dato: [i]})
                # Actualizo la clave Canciones con un diccionario obtenido de la búsqueda anterior
        else:  # El else es para el resto de las claves del diccionario
            valor = input(f'Introduzca el {dato}: ')  # Pedimos el valor por teclado
            datos.update({dato: valor})  # Actualizamos el dict
    cursor = db.Playlist.find_one(
        {"_id": datos['Nombre lista']})  # Creamos un cursor para que busque el nombre del usuario.
    if cursor is None:
        # Si no lo encuentra, rellenamos los campos con los datos del diccionario.
        # Utilizaremos la variable user para almacenar temporalmente la información
        user = ([{  # Convertimos el diccionario datos en formato Bson para guardarlo en la BBDD
            "_id": datos['Nombre lista'],
            "nombre": datos['Username'],
            "canciones": datos['Canciones'],
        }])
        db.Playlist.insert_many(user)  # Insertamos la información en la clección Usuario
    else:
        print(f"La lista {datos['Nombre lista']} ya existe")
        # Si el nombre de usuario se repite, muestra esta infortmación
    client.close()


def consulta_playlist():
    """
    Función similar a las otras de consultas
    :return: No retorna nada
    """
    print('Pulse 1 si desea buscar por usuario: ')  # Le presentamos un menú de opciones
    print('Pulse 2 si desea buscar por nombre de playlist: ')
    print('Pulse 0 para salir: ')
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client.musicplaylist
    while True:  # Generamos un bucle infinito que se corará al pursar el 0
        opcion = input('Introduzca su opción de búsqueda: ')  # Pedimos la opción de búsqueda
        if opcion == '1':
            # Y según la opción elegida, abrimos 2-un cursor que busque la coincidencia con la opción elegida
            n = input('Introduzca el nombre de usuario: ')
            # Luego mediante un for, mostramos los resultados obtenidos
            cursor = db.Playlist.find({'nombre': n})  # Esto se repite con las 2 opciones dadas
            for dato in cursor:
                print(f'El usuario {dato["nombre"]} tiene las playlist:'
                      f' {dato["_id"]}, con las canciones \n{dato["canciones"]}')
        elif opcion == '2':
            n = input('Introduzca el nombre de la lista: ')
            cursor = db.Playlist.find({'_id': n})
            for dato in cursor:
                print(
                    f'La lista {dato["_id"]} pertenecde a {dato["nombre"]} y tiene las canciones \n{dato["canciones"]}')
        elif opcion == '0':
            break  # Rompemos el bucle while
        else:
            print('Opción incorrecta')  # Mostramos mensaje si se ha introducido opción inválida
    client.close()


def anadir_cancion():
    """
    Esta función es para añadir una cación que esxiste en la colección de canciones a una
    playlist ya creada. Se pide el título de la canción y el nombre de la Playlist.
    :return: No retorna nada
    """
    n = input('Introduzca el título de la canción: ')  # Pedimos la canción que deseamos buscar
    p = input('Introduzca el nombre de la playlist a la que quiere añadir la canción: ')
    # Pedimos la lista a la que la queremos añadir
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client.musicplaylist
    cursor = db.Canciones.find({'_id': n})  # Creamos un cursor que busca la canción deseada
    for dato in cursor:
        db.Playlist.update_one({"_id": p}, {"$push": {"canciones": dato}})  # Si la encuentra, la añade
    client.close()


def rellenar_bd(ruta, artista):
    """
    Esta función se usará para rellenar la colección de canciones con 50 canciones. 5 de 10 artistas diferentes.
    Es una función algo complicada, en el Juoyter se ha explicado su desarrollo. En resumen, se le pasa la ruta de
    los archovos y los nombres de los artistas mediante 2 listas. Recorriendo estas listas, mediante 2 for, buscaremos
    y pasaremos a la coleccion canciones cada una de las 50 canciones.
    :param ruta: a este parámetro se le pasa la lista con las rutas relativas
    :param artista: a este parámetro se le pasa la lista con los nomnbres de los artistas
    :return: no retorna nada
    """
    acum = []                                      # lista acumulador para los títulos de las canciones
    s = 0                                          # controlamos la lista de los artistas
    n = 0                                          # controlamos la lista de las rutas relativas
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client.musicplaylist
    for grupo in ruta:                             # recorremos la lista de rutas relativas
        with open(grupo) as file:                  # abrimos el archivo
            data = json.loads(file.read())
            for cancion in data['results']:        # Dentro de cada archivo, recorremos por la clave results
                if cancion['artistName'] == artista[s] and cancion['trackName'] not in acum and n < 5:
                    # condiciones para realizar la búsqueda, si se cumnplen
                    n += 1                          # aumentamos contador
                    acum.append(cancion['trackName'])     # añadimos el título a la lista acumuladora
                    user = ([{"_id": cancion['trackName'], "cantante": cancion['artistName'],
                              "genero": cancion['primaryGenreName'], "album": cancion['collectionName'],
                              "url": cancion['trackViewUrl']}])     # Creamos el Bson para volcar en la colleción
                    db.Canciones.insert_many(user)                  # Volcamos en la colección
                elif n >= 5 and s < 9:                               # reiniciamos contadores
                    n = 0
                    s += 1
    client.close()                                                   # Cerramos conexión


def repartir_canciones():
    """
    Con esta función cogeremos las 50 canciones y las repartiremos en playlist ya existentes
    :return: No retorna nada
    """
    n = input('Introduzca el nombre del artista: ')  # Pedimos el nombre del artista que deseamos buscar
    p = input('Introduzca el nombre de la playlist a la que quiere añadir la canción: ')
    # Pedimos la lista a la que la queremos añadir
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client.musicplaylist
    cursor = db.Canciones.find({'cantante': n})  # Creamos un cursor que busca la canción deseada
    for dato in cursor:
        db.Playlist.update_one({"_id": p}, {"$push": {"canciones": dato}})  # Si la encuentra, la añade
    client.close()
