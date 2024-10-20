def alumne_schema(fetchAlumnes) -> dict:
    # Converteix un registre d'alumne en un diccionari només amb els camps necessaris
    return {
        "NomAlumne": fetchAlumnes[0],
        "Cicle": fetchAlumnes[1],
        "Curs": fetchAlumnes[2],
        "Grup": fetchAlumnes[3],
        "DescAula": fetchAlumnes[4]  # Ara incloem DescAula que prové de la taula aula
    }

def alumnes_schema(alumnes) -> list:
    # Converteix una llista de registres d'alumnes en una llista de diccionaris
    return [alumne_schema(alumne) for alumne in alumnes]


