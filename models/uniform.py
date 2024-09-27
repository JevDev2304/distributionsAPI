from pydantic import BaseModel
from typing import Literal
class UniformInput(BaseModel):
    theta_1: float
    theta_2: float
    x : float
    operator: Literal["=", "<", ">", "<=", ">="]
