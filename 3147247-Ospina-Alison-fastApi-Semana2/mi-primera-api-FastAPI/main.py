from fastapi import FastAPI
from typing import List, Dict

app = FastAPI(title="My First API")

# ANTES (Semana 1)
@app.get("/")
def hello_world():
    return {"message": "My first FastAPI!"}

# DESPUÉS (con type hints)
@app.get("/")
def hello_world() -> dict:
    return {"message": "My first FastAPI!"}

# Si tenías endpoint con parámetro
@app.get("/greeting/{name}")
def greet_user(name: str) -> dict:
    return {"greeting": f"Hello {name}!"}

# Endpoint con múltiples parámetros
@app.get("/calculate/{num1}/{num2}")
def calculate(num1: int, num2: int) -> dict:
    result = num1 + num2
    return {"result": result, "operation": "sum"}

# Lista de strings
@app.get("/fruits")
def get_fruits() -> List[str]:
    return ["apple", "banana", "orange"]

# Lista de números
@app.get("/numbers")
def get_numbers() -> List[int]:
    return [1, 2, 3, 4, 5]

# Diccionario con estructura conocida
@app.get("/user/{user_id}")
def get_user(user_id: int) -> Dict[str, str]:
    return {
        "id": str(user_id),
        "name": "Alison Ospina",
        "email": "alisonospinaariza0126@gmail.com"
    }