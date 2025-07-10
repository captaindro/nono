from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "NONO V1 is alive!"}
