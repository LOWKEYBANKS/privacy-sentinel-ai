from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Privacy Sentinel API is running"}

