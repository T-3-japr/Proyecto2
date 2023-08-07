from funciones import misfunciones as mf
import pymongo
import random as rd


class Playlist:

    def __init__(self, nombre, usuario, canciones):
        self.nombre_pl = nombre
        self.user = usuario
        self.song = canciones

    def anadir_canciones(self):
        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client.musicplaylist
        print('\tSe van a mostrar 20 canciones al azar de la colección "Canciones", eliga cual quiere añadir:\n')
        Playlist.mostrar_sugerencias(self)
        mf.anadir_cancion()
        client.close()

    def mostrar_sugerencias(self):
        selec = []
        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client.musicplaylist
        cursor = db.Canciones.find()
        for n in cursor:
            selec.append(n["_id"])
        print('Las 20 canciones elegidas al azar, son: \n')
        print(" \n ".join(rd.sample(selec, k=20)))
        client.close()

    def mostrar_canciones(self):
        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client.musicplaylist
        cancion = {}
        while True:
            opcion = input('Introduzca el nombre de la lista o 0 para salir: ')
            if opcion != '0':
                cursor = db.Playlist.find({'_id': opcion})
                for dato in cursor:
                    for clave in dato['canciones']:
                        cancion.update({clave["_id"]: clave["cantante"]})
            elif opcion == '0':
                break
        client.close()
        return f'La lista tiene las canciones: {" - ".join(cancion.keys())} \nde los artistas:' \
               f' {" - ".join(cancion.values())}'

    def consultar_playlist(self):  # Para este método, llamnaremos directamente a la función que hace la misma función
        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client.musicplaylist
        mf.consulta_playlist()
        client.close()

    def metodo_mostrar_playlist(func):
        def mostrar_canciones(self):
            client = pymongo.MongoClient("mongodb://localhost:27017")
            db = client.musicplaylist
            cancion = {}
            while True:
                opcion = input('Introduzca el nombre de la lista o 0 para salir: ')
                if opcion != '0':
                    cursor = db.Playlist.find({'_id': opcion})
                    for dato in cursor:
                        for clave in dato['canciones']:
                            cancion.update({clave["_id"]: clave["cantante"]})
                elif opcion == '0':
                    break
            client.close()
            return func(cancion)

        return mostrar_canciones

    @metodo_mostrar_playlist
    def mostrar_pl(func):
        genero = []
        print(f'La lista tiene las canciones: {" - ".join(func.keys())} \nde los artistas: {" - ".join(func.values())}')
        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client.musicplaylist
        for n in func.keys():
            cursor = db.Canciones.find({'_id': n})
            for dato in cursor:
                genero.append(dato["genero"])
        client.close()
        print(f'Sus géneros musicales son: ', " - ".join(genero))

    def __str__(self):
        return f'{self.mostrar_canciones()}'


PATH = ['datos/heroesdelsilencio.txt', 'datos/mecano.txt', 'datos/celtascortos.txt', 'datos/coldplay.txt',
        'datos/duncandhu.txt', 'datos/fito.txt', 'datos/magodeoz.txt', 'datos/Gorillaz.txt',
        'datos/rem.txt', 'datos/metallica.txt']
ARTISTAS = ['Héroes del Silencio', 'Mecano', 'Celtas Cortos', 'Coldplay', 'Duncan Dhu',
            'Fito Olivares Y Su Grupo', 'Mägo de Oz', 'Gorillaz', 'R.E.M.', 'Metallica']
opcion = None

while opcion != '0':
    opcion = mf.menu_inicial()
    match opcion:
        case '1':
            mf.crear_base_datos()
        case '2':
            mf.crear_usuario()
        case '3':
            mf.consulta_usuario()
        case '4':
            mf.crear_cancion()
        case '5':
            mf.consulta_cancion()
        case '6':
            mf.crear_playlist()
        case '7':
            mf.consulta_playlist()
        case '8':
            mf.anadir_cancion()
        case '9':
            mf.rellenar_bd(PATH, ARTISTAS)
        case '10':
            mf.repartir_canciones()
        case '11':
            nombre = input('Introduzca el nombre de la Playlist: ')
            usuario = input('Introduzca el User: ')
            canciones = input('Introduzca la canción: ')
            Playlist(nombre, usuario, canciones)
            Playlist.mostrar_sugerencias(canciones)
        case '12':
            nombre = input('Introduzca el nombre de la Playlist: ')
            usuario = input('Introduzca el User: ')
            canciones = input('Introduzca la canción: ')
            Playlist(nombre, usuario, canciones)
            Playlist.anadir_canciones(canciones)
        case '13':
            nombre = input('Introduzca el nombre de la Playlist: ')
            usuario = input('Introduzca el User: ')
            canciones = input('Introduzca la canción: ')
            Playlist(nombre, usuario, canciones)
            result = Playlist.mostrar_canciones(canciones)
            print(result)
        case '14':
            nombre = input('Introduzca el nombre de la Playlist: ')
            usuario = input('Introduzca el User: ')
            canciones = input('Introduzca la canción: ')
            Playlist(nombre, usuario, canciones)
            Playlist.consultar_playlist(canciones)
        case '15':
            nombre = input('Introduzca el nombre de la Playlist: ')
            usuario = input('Introduzca el User: ')
            canciones = input('Introduzca la canción: ')
            Playlist(nombre, usuario, canciones)
            Playlist.mostrar_pl(canciones)
        