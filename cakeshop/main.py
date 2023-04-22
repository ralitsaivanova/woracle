from fastapi import FastAPI

app = FastAPI(title="Cakeshop API", openapi_url="/openapi.json")


@app.get("/")
async def root():
    return {"message": "Hello Woracle"}
