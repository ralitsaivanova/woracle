from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, orm


from cakeshop import dependencies
from cakeshop.db import models as db_models
from cakeshop.schemas import cake as cake_schemas

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


@app.get(
    "/cakes/",
    status_code=200,
    response_model=cake_schemas.CakeListOutput,
    description="Lists all cakes",
)
async def list_all_cakes(
    *, db: Session = Depends(dependencies.get_db)
) -> List[dict] == None:
    query_statement = select(db_models.Cake)
    result = db.execute(query_statement).scalars().all()
    return cake_schemas.CakeListOutput(result)


@app.delete(
    "/cakes/{cake_id}/",
    status_code=204,
    description="Delete a cake",
)
async def delete_cake(
    *, cake_id: int, db: Session = Depends(dependencies.get_db)
) -> None:
    try:
        db.query(db_models.Cake).where(db_models.Cake.id == cake_id).one()
        db.execute(delete(db_models.Cake).where(db_models.Cake.id == cake_id))
        db.commit()
    except orm.exc.NoResultFound:
        raise HTTPException(status_code=404, detail=f"Cake {cake_id} not found")
