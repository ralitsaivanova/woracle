from fastapi import FastAPI, Depends
from cakeshop.schemas import cake as cake_schemas
from cakeshop import dependencies
from sqlalchemy.orm import Session
from cakeshop.db import models as db_models

app = FastAPI(title="Cakeshop API", openapi_url="/openapi.json")


@app.get("/")
async def root():
    return {"message": "Hello Woracle"}


@app.post(
    "/cakes/",
    status_code=201,
    response_model=cake_schemas.CakeOutput,
    description="Add a cake",
)
async def save_cake(
    *, cake: cake_schemas.CakeInput, db: Session = Depends(dependencies.get_db)
) -> dict:
    saved_cake = db_models.Cake(
        name=cake.name,
        comment=cake.comment,
        imageUrl=cake.imageUrl,
        yumFactor=cake.yumFactor,
    )
    db.add(saved_cake)
    db.commit()
    db.refresh(saved_cake)

    return saved_cake
