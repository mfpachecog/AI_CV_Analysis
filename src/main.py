from fastapi import FastAPI

app = FastAPI()

@app.get("/dev")
def read_root():
    messagee = "Hello this is my first app in FastAPI"
    return{messagee}