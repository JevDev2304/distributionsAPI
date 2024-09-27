from pydantic import BaseModel
from typing import Literal
class PoissonInput(BaseModel):
    lamb: int
    x: int
    operator: Literal["=", "<", ">", "<=", ">="]
