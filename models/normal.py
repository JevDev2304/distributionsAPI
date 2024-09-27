from pydantic import BaseModel
from typing import Literal

class NormalInput(BaseModel):
    mu: float
    sigma: float
    x: float
    operator: Literal["=", "<", ">", "<=", ">="]