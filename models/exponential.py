from pydantic import BaseModel
from typing import Literal
class ExponentialInput(BaseModel):
    lamb: float
    x: float
    operator: Literal["=", "<", ">", "<=", ">="]