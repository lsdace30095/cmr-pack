from fastapi import FastAPI

app = FastAPI(title="SmartCity STP API")

@app.get("/")
def root():
    return {"status": "SmartCity STP running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
