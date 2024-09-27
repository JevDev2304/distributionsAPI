from pydantic import BaseModel
from typing import Literal
class ChiSquareInput(BaseModel):
    v: float
    x: float
    operator: Literal["=", "<", ">", "<=", ">="]