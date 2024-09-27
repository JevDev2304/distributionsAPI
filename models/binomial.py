from pydantic import BaseModel
from typing import Literal
class BinomialInput(BaseModel):
    n: int
    p: float
    x: int
    operator: Literal["=", "<", ">", "<=", ">="]
