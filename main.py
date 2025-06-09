from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Mensaje(BaseModel):
    user: str
    mensaje: str

class MensajeConId(Mensaje):
    id: int

mensajes: List[MensajeConId] = []
contador = 1

@app.get("/mensajes", response_model=List[MensajeConId])
def obtenerM():
    return mensajes

@app.get("/mensajes/{mensaje_id}", response_model= MensajeConId)
def obtenerMen(mensaje_id: int):
    for mensaje in mensajes:
        if mensaje.id == mensaje_id:
            return mensaje
    raise HTTPException(status_code=404, detail= "Mensaje no encontrado")

@app.post("/mensajes", response_model= MensajeConId, status_code=201)
def crear_mensaje(mensaje: Mensaje):
    global contador
    nuevo_mensaje = MensajeConId(id=contador, **mensaje.dict())
    mensajes.append(nuevo_mensaje)
    contador += 1
    return nuevo_mensaje

@app.put("/mensajes/{mensaje_id}", response_model= MensajeConId)
def actualizar_mensaje (mensaje_id: int, mensaje_actualizado: Mensaje):
    for i, mensaje in enumerate(mensajes):
        if mensaje.id == mensaje_id:
            mensajes[i] = MensajeConId(id=mensaje_id, **mensaje_actualizado.dict())
            return mensaje[i]
    raise HTTPException(status_code=404, detail= "Mensaje no encontrado")

@app.delete("/mensajes/{mensaje_id}")
def eliminar_mensaje(mensaje_id: int):
    for mensaje in mensajes:
        if mensaje.id == mensaje_id:
            mensajes.remove(mensaje)
            return {"mensaje": "Mensaje eliminado"}
    raise HTTPException(status_code=404, detail= "Mensaje no encontrado")


