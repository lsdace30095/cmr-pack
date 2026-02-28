@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Intersection Flow Engine"}