from client import db_client
from fastapi import HTTPException

def read_all(orderby=None, contain=None, skip=0, limit=None):
    try:
        conn = db_client()
        cur = conn.cursor()

        # Construir la consulta base
        query = """
            SELECT NomAlumne, Cicle, Curs, Grup, DescAula 
            FROM alumne 
            JOIN aula ON alumne.IdAula = aula.IdAula
        """

        # Filtro para el parámetro 'contain'
        if contain:
            query += f" WHERE NomAlumne LIKE '%{contain}%'"

        # Ordenar por 'NomAlumne' si el parámetro 'orderby' está presente
        if orderby == "asc":
            query += " ORDER BY NomAlumne ASC"
        elif orderby == "desc":
            query += " ORDER BY NomAlumne DESC"

        # Aplicar paginación si 'limit' y 'skip' están presentes
        if limit is not None:
            query += f" LIMIT {limit} OFFSET {skip}"

        cur.execute(query)
        alumne = cur.fetchall()

    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}"}
    
    finally:
        conn.close()

    return alumne


def read_id(id):
    # Retorna un alumne per la seva Id.
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT * FROM alumne WHERE IdAlumne = %s", (id,))  # Corregido
        alumne = cur.fetchone()
            
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}"}
    
    finally:
        conn.close()
    
    return alumne

def check_aula_exists(idaula):
    # Comprova si l'IdAula existeix a la taula Aula.
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT * FROM aula WHERE IdAula = %s", (idaula,))
        aula = cur.fetchone()
        return aula is not None 
    except Exception as e:
        return False  
    finally:
        conn.close()

def add_alumne(nomalumne, cicle, curs, grup, idaula):
    # Afegeix un nou alumne a la base de dades.
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "INSERT INTO alumne (NomAlumne, Cicle, Curs, Grup, IdAula, CreatedAt, UpdatedAt) VALUES (%s, %s, %s, %s, %s, NOW(), NOW())"
        cur.execute(query, (nomalumne, cicle, curs, grup, idaula))
        conn.commit() 
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Error al añadir l'alumne: {e}")
    finally:
        conn.close()

def delete_alumne(id):
    # Elimina un alumne per la seva Id.
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "DELETE FROM alumne WHERE IdAlumne = %s"
        cur.execute(query, (id,))
        conn.commit() 
        return cur.rowcount 
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Error al eliminar l'alumne: {e}")
    finally:
        conn.close()

def update_alumne(id, nomalumne, cicle, curs, grup, idaula):
    # Actualitza les dades d'un alumne.
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "UPDATE alumne SET NomAlumne = %s, Cicle = %s, Curs = %s, Grup = %s, IdAula = %s WHERE IdAlumne = %s"
        cur.execute(query, (nomalumne, cicle, curs, grup, idaula, id))
        conn.commit()  
        return cur.rowcount 
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al modificar l'alumne: {e}")
    finally:
        conn.close()

def check_aula_exists_by_desc(DescAula):
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT * FROM aula WHERE DescAula = %s", (DescAula,))
        aula = cur.fetchone()
        return aula is not None
    except Exception as e:
        return False
    finally:
        conn.close()

def add_aula(DescAula, Edifici, Pis):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "INSERT INTO aula (DescAula, Edifici, Pis, CreatedAt, UpdatedAt) VALUES (%s, %s, %s, NOW(), NOW())"
        cur.execute(query, (DescAula, Edifici, Pis))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al afegir aula: {e}")
    finally:
        conn.close()

def check_alumne_exists(NomAlumne, Cicle, Curs, Grup):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT * FROM alumne WHERE NomAlumne = %s AND Cicle = %s AND Curs = %s AND Grup = %s"
        cur.execute(query, (NomAlumne, Cicle, Curs, Grup))
        alumne = cur.fetchone()
        return alumne is not None
    except Exception as e:
        return False
    finally:
        conn.close()

def add_alumne(NomAlumne, Cicle, Curs, Grup, DescAula):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = """
            INSERT INTO alumne (NomAlumne, Cicle, Curs, Grup, IdAula, CreatedAt, UpdatedAt) 
            VALUES (%s, %s, %s, %s, (SELECT IdAula FROM aula WHERE DescAula = %s), NOW(), NOW())
        """
        cur.execute(query, (NomAlumne, Cicle, Curs, Grup, DescAula))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al afegir alumne: {e}")
    finally:
        conn.close()
