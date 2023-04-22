from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional


class Cake(BaseModel):
    id: int
    name: str
    comment: str
    imageUrl: HttpUrl
    yumFactor: int


class CakeInput(BaseModel):
    name: str = Field(max_length=30)
    comment: str = Field(max_length=200)
    imageUrl: HttpUrl
    yumFactor: int = Field(gt=0, le=5)


class CakeORM(Cake):
    class Config:
        orm_mode = True


class CakeOutput(CakeORM):
    pass


class CakeListOutput(List[CakeOutput]):
    pass
