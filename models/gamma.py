from pydantic import BaseModel
from typing import  Literal
class GammaInput(BaseModel):
    alpha: float
    beta: float
    x: float
    operator: Literal["=", "<", ">", "<=", ">="]