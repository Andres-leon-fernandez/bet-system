from fastapi import FastAPI

app= FastAPI()

@app.get("/") 
def server():
  return {"Hola desde pyton"}