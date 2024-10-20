import mysql.connector
#CODI NECESARI PER CONECTAR AMB LA BASE DE DADES EN AQUET CAS AMB LA QUE ESTA FETA A HEIDI_DB
def db_client():
    
    try:
        dbname = "alumnat"
        user = "root"
        password = "1234"
        host = "localhost"
        port = "3306"
        collation="utf8mb4_general_ci"
        
        return mysql.connector.connect(
            host = host,
            port = port,
            user = user,
            password = password,
            database = dbname,
            collation=collation
        ) 
            
    except Exception as e:
            return {"status": -1, "message": f"Error de connexió:{e}" }
            
            
            
            
           