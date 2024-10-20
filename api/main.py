from fastapi import FastAPI, File, UploadFile, HTTPException
import db_alumnat  # Les funcions de la base de dades
import csv
from io import StringIO
import alumnes
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware  # Afegit import
from typing import List, Optional


app = FastAPI()

# Configuració de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet l'accés des de qualsevol origen
    allow_credentials=True,
    allow_methods=["*"],  # Permet tots els mètodes (GET, POST, etc.)
    allow_headers=["*"],  # Permet totes les capçaleres
)

class Alumne(BaseModel):
    nomalumne: str
    cicle: str
    curs: int
    grup: str
    idaula: int 

class tablaAlumne(BaseModel):  # Nova classe base
    NomAlumne: str
    Cicle: str
    Curs: int
    Grup: str
    DescAula: str  # Assegura't que aquest camp coincideix amb el que retorna

@app.get("/")
def read_root():
    return {"API"}

@app.get("/alumne/list", response_model=List[alumnes.alumne_schema])  # Cambiado de dict a AlumneSchema
def read_alumnes(orderby: Optional[str] = None, contain: Optional[str] = None, skip: int = 0, limit: Optional[int] = None):
    try:
        alumne_db = db_alumnat.read_all(orderby, contain, skip, limit)
        if not alumne_db:
            raise HTTPException(status_code=404, detail="No hi ha alumnes")
        alumnes_serialized = alumnes.alumnes_schema(alumne_db)
        return alumnes_serialized
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la consulta: {str(e)}")
@app.get("/alumne/show/{id}", response_model=dict)
def read_alumne(id: int):
    alumne_db = db_alumnat.read_id(id)  
    if not alumne_db:
        raise HTTPException(status_code=404, detail="Alumne no trobat")  
    
    alumne_serialized = alumnes.alumne_schema(alumne_db)
    return alumne_serialized

@app.post("/alumne/add", response_model=dict)
def add_alumne(alumne: Alumne):
    aula_exists = db_alumnat.check_aula_exists(alumne.idaula) 
    if not aula_exists:
        raise HTTPException(status_code=400, detail="La ID de Aula no existeix")

    db_alumnat.add_alumne(alumne.nomalumne, alumne.cicle, alumne.curs, alumne.grup, alumne.idaula) 
    return {"message": "S'ha afegit correctament"}

@app.delete("/alumne/delete/{id}", response_model=dict)
def delete_alumne(id: int):
    deleted_rows = db_alumnat.delete_alumne(id)
    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Alumne no trobat")  
    
    return {"message": "S'ha esborrat correctament"}

@app.put("/alumne/update/{id}", response_model=dict)
def update_alumne(id: int, alumne: Alumne):
    if alumne.idaula is not None:
        aula_exists = db_alumnat.check_aula_exists(alumne.idaula)
        if not aula_exists:
            raise HTTPException(status_code=400, detail="La IdAula no existe")

    updated_rows = db_alumnat.update_alumne(id, alumne.nomalumne, alumne.cicle, alumne.curs, alumne.grup, alumne.idaula)
    
    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="Alumne no trobat") 
    
    return {"message": "S’ha modificat correctament"}

@app.post("/alumne/loadAlumnes")
async def load_alumnes(file: UploadFile = File(...)):
    try:
        # Llegir el contingut del fitxer CSV
        contents = await file.read()
        content_str = contents.decode("utf-8")
        
        # Utilitzar StringIO per llegir el contingut com a fitxer
        csv_reader = csv.reader(StringIO(content_str))
        
        next(csv_reader)  # Omet la capçalera
        
        for row in csv_reader:
            DescAula, Edifici, Pis, NomAlumne, Cicle, Curs, Grup = row
            
            # Verificar si l'aula ja existeix
            aula_exists = db_alumnat.check_aula_exists_by_desc(DescAula)
            if not aula_exists:
                # Inserir nova aula
                db_alumnat.add_aula(DescAula, Edifici, Pis)
            
            # Verificar si l'alumne ja existeix
            alumne_exists = db_alumnat.check_alumne_exists(NomAlumne, Cicle, Curs, Grup)
            if not alumne_exists:
                # Inserir nou alumne
                db_alumnat.add_alumne(NomAlumne, Cicle, Curs, Grup, DescAula)
        
        return {"message": "Càrrega massiva realitzada correctament"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error durant la càrrega massiva: {str(e)}")