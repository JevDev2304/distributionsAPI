from fastapi import APIRouter, HTTPException
from math import comb
from models.binomial import BinomialInput
from models.poisson import PoissonInput
from math import exp, factorial, sqrt

discreteRouter = APIRouter(prefix="/discrete",
    tags=["Discrete"])


@discreteRouter.post("/binomial/")
def calculate_binomial(input: BinomialInput):
    n = input.n
    p = input.p
    x = input.x
    operator = input.operator
    x_axis = []
    y_axis = []

    # Cálculo de la probabilidad binomial
    probability = 0
    if operator in ["=", "<", ">", "<=", ">="]:
        for i in range(n + 1):
            prob_i = comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
            x_axis.append(i)
            y_axis.append(prob_i)
            if (operator == "=" and i == x) or \
               (operator == "<" and i < x) or \
               (operator == ">" and i > x) or \
               (operator == "<=" and i <= x) or \
               (operator == ">=" and i >= x):
                probability += prob_i
    else:
        raise HTTPException(status_code=400, detail="Operador no válido")

    return {
        "probability": round(probability, 5),
        "x": x_axis,
        "f(x)": y_axis
    }

@discreteRouter.post("/poisson/")
def calculate_poisson(input : PoissonInput):
    lamb = input.lamb
    x = input.x
    operator = input.operator
    x_axis = []
    y_axis = []
    probability = 0
    if operator not in ["=", "<", ">", "<=", ">="]:
        raise HTTPException(status_code=400, detail="Operador no válido")
    max_range = int(lamb + 3 * sqrt(lamb))  # Captura la mayoría de la distribución

    def poisson_pmf(lamb, k):
        return (lamb ** k) * exp(-lamb) / factorial(k)

    # Calcular la probabilidad y la distribución según el operador
    for i in range(0, max_range + 1):
        prob_i = poisson_pmf(lamb, i)
        x_axis.append(i)
        y_axis.append(prob_i)

        # Sumar la probabilidad según el operador
        if operator == "=" and i == x:
            probability += prob_i
        elif operator == "<" and i < x:
            probability += prob_i
        elif operator == ">" and i > x:
            probability += prob_i
        elif operator == "<=" and i <= x:
            probability += prob_i
        elif operator == ">=" and i >= x:
            probability += prob_i

    # Retornar la probabilidad y la distribución calculada
    return {
        "probability": round(probability, 5),
        "x": x_axis,
        "f(x)": y_axis
    }




