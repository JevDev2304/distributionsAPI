from fastapi import APIRouter, HTTPException
from models.uniform import UniformInput
from models.gamma import GammaInput
from models.exponential import ExponentialInput
from models.chi import  ChiSquareInput
from models.normal import NormalInput
from typing import List
from math import exp, gamma, pi , sqrt

continuosRouter = APIRouter(prefix="/continuos",
    tags=["Continuos"])


@continuosRouter.post("/uniform/")
def calculate_uniform(input: UniformInput):
    a = input.theta_1
    b = input.theta_2
    x = input.x
    operator = input.operator


    if a >= b:
        raise HTTPException(status_code=400, detail="El límite inferior 'a' debe ser menor que el límite superior 'b'.")


    x_axis = []
    y_axis = []


    current = a
    while current <= b:
        x_axis.append(round(current, 2))  # Redondear a 2 decimales
        y_axis.append(round(1 / (b - a), 2))  # Densidad constante en el intervalo
        current += 0.01


    probability = 0

    if operator == "=":
        probability = 0
    elif operator == "<":
        if x <= a:
            probability = 0
        elif x < b:
            probability = round((x - a) / (b - a), 5)
        else:
            probability = 1
    elif operator == ">":
        if x >= b:
            probability = 0
        elif x > a:
            probability = round((b - x) / (b - a), 5)
        else:
            probability = 1
    elif operator == "<=":
        if x < a:
            probability = 0
        elif x >= b:
            probability = 1
        else:
            probability = round((x - a) / (b - a), 5)
    elif operator == ">=":
        if x > b:
            probability = 0
        elif x <= a:
            probability = 1
        else:
            probability = round((b - x) / (b - a), 5)
    else:
        raise HTTPException(status_code=400, detail="Operador no válido")

    return {
        "probability": round(probability, 5),
        "x": x_axis,
        "f(x)": y_axis
    }


@continuosRouter.post("/gamma/")
def calculate_gamma(input: GammaInput):
    alpha = input.alpha
    beta = input.beta
    x = input.x
    operator = input.operator

    # Validaciones iniciales
    if alpha <= 0 or beta <= 0:
        raise HTTPException(status_code=400, detail="Los parámetros alpha y beta deben ser mayores que 0.")

    if x < 0:
        raise HTTPException(status_code=400, detail="x debe ser mayor o igual a 0.")

    # Variables para la PDF y configuración del paso
    x_axis: List[float] = []
    y_axis: List[float] = []
    current_x = 0.0
    step = 0.01  # Disminuir el paso para mayor precisión
    gamma_alpha = gamma(alpha)  # Constante Gamma(alpha)

    # Inicializamos la CDF
    cdf = 0.0

    # Cálculo de la PDF y acumulación de la CDF hasta x usando la regla del trapecio
    while current_x <= (alpha + 4 * beta):
        # PDF de la distribución gamma
        pdf = (beta ** alpha / gamma_alpha) * (current_x ** (alpha - 1)) * exp(-beta * current_x)

        # Agregamos puntos al gráfico
        x_axis.append(round(current_x, 3))  # Redondeo para precisión en la salida
        y_axis.append(round(pdf, 6))

        # Acumulamos la CDF hasta x
        if current_x <= x:
            cdf += pdf * step

        # Avanzamos el valor de current_x
        current_x += step

    # Cálculo de la probabilidad según el operador
    if operator == "=":
        probability = 0  # Probabilidad de un valor exacto en distribución continua es 0.
    elif operator == "<":
        probability = cdf
    elif operator == "<=":
        probability = cdf
    elif operator == ">":
        probability = 1 - cdf
    elif operator == ">=":
        probability = 1 - cdf
    else:
        raise HTTPException(status_code=400, detail="Operador no válido")

    # Retorno del resultado
    return {
        "probability": round(probability, 6),  # Más precisión en el resultado final
        "x": x_axis,
        "f(x)": y_axis
    }


@continuosRouter.post("/exponential/")
def calculate_exponential(input: ExponentialInput):
    lamb = input.lamb
    x = input.x
    operator = input.operator

    # Validar que lambda sea mayor que 0
    if lamb <= 0:
        raise HTTPException(status_code=400, detail="El parámetro lambda debe ser mayor que 0.")

    if x < 0:
        raise HTTPException(status_code=400, detail="x debe ser mayor o igual a 0.")

    # Inicializar ejes x y y
    x_axis = []
    y_axis = []
    current_x = 0.0
    step = 0.01

    # Cálculo de la PDF de la distribución exponencial y llenado de los ejes
    while current_x <= (x + 10):  # Se extiende el rango para mostrar la curva completa
        # PDF de la distribución exponencial
        pdf = lamb * exp(-lamb * current_x)

        # Añadir a los ejes
        x_axis.append(round(current_x, 2))
        y_axis.append(round(pdf, 5))

        # Incrementar el valor de x en 0.01
        current_x += step

    # Calcular la CDF acumulada hasta x
    cdf = 1 - exp(-lamb * x)

    # Calcular la probabilidad según el operador
    probability = 0
    if operator == "=":
        probability = 0  # En distribuciones continuas, la probabilidad de un valor exacto es 0.
    elif operator == "<":
        probability = cdf
    elif operator == ">":
        probability = 1 - cdf
    elif operator == "<=":
        probability = cdf
    elif operator == ">=":
        probability = 1 - cdf
    else:
        raise HTTPException(status_code=400, detail="Operador no válido")

    return {
        "probability": round(probability, 5),
        "x": x_axis,
        "f(x)": y_axis
    }
@continuosRouter.post("/chi/")
def calculate_chi_square(input: ChiSquareInput):
    v = input.v
    x = input.x
    operator = input.operator

    # Validación de los parámetros de entrada
    if v <= 0:
        raise HTTPException(status_code=400, detail="Los grados de libertad (v) deben ser mayores que 0.")
    if x < 0:
        raise HTTPException(status_code=400, detail="x debe ser mayor o igual a 0.")

    x_axis = []
    y_axis = []
    current_x = 0.0
    step = 0.001  # Paso más pequeño para mayor precisión

    # Coeficiente de la PDF (precalcular para eficiencia)
    coefficient = 1 / (2 ** (v / 2) * gamma(v / 2))

    # Función de densidad de probabilidad (PDF) para la distribución Chi-Cuadrado
    def chi_square_pdf(v, x):
        return coefficient * (x ** (v / 2 - 1)) * exp(-x / 2)

    # Suma acumulativa para la CDF
    cdf_sum = 0

    # Llenar los ejes con valores de PDF
    while current_x <= (x + 10):
        pdf = chi_square_pdf(v, current_x)

        # Añadir a los ejes
        x_axis.append(round(current_x, 3))  # Redondear a 3 decimales
        y_axis.append(round(pdf, 6))  # Redondear a 6 decimales

        # Sumar a la CDF si estamos dentro del rango de integración
        if current_x <= x:
            cdf_sum += pdf * step

        # Incrementar x
        current_x += step

    # Calcular la probabilidad según el operador
    probability = 0
    if operator == "=":
        probability = 0  # En distribuciones continuas, la probabilidad exacta es 0.
    elif operator == "<":
        probability = cdf_sum
    elif operator == ">":
        probability = 1 - cdf_sum
    elif operator == "<=":
        probability = cdf_sum
    elif operator == ">=":
        probability = 1 - cdf_sum
    else:
        raise HTTPException(status_code=400, detail="Operador no válido")

    # Retorno del resultado con probabilidades y valores de ejes
    return {
        "probability": round(probability, 6),  # Redondear a 6 decimales
        "x": x_axis,
        "f(x)": y_axis
    }
@continuosRouter.post("/normal/")
def calculate_normal(input: NormalInput):
    mu = input.mu
    sigma = input.sigma
    x = input.x
    operator = input.operator

    # Validación de los parámetros de entrada
    if sigma <= 0:
        raise HTTPException(status_code=400, detail="La desviación estándar (sigma) debe ser mayor que 0.")

    # Ejes para los valores de x y su correspondiente PDF
    x_axis = []
    y_axis = []
    current_x = mu - 4 * sigma  # Iniciar en mu - 4σ para cubrir la mayoría de la distribución
    end_x = mu + 4 * sigma  # Terminar en mu + 4σ
    step = 0.001  # Paso para mayor precisión

    # Precalcular constante de la PDF para eficiencia
    pdf_constant = 1 / (sigma * sqrt(2 * pi))

    # Función de densidad de probabilidad (PDF) para la normal
    def normal_pdf(x):
        exponent = -((x - mu) ** 2) / (2 * sigma ** 2)
        return pdf_constant * exp(exponent)

    # Suma acumulativa para la CDF
    cdf_sum = 0

    # Llenar los ejes con valores de PDF y calcular CDF acumulativa
    while current_x <= end_x:
        pdf = normal_pdf(current_x)

        # Añadir a los ejes
        x_axis.append(round(current_x, 3))  # Redondear a 3 decimales
        y_axis.append(round(pdf, 6))  # Redondear a 6 decimales

        # Sumar a la CDF si estamos dentro del rango de integración
        if current_x <= x:
            cdf_sum += pdf * step

        # Incrementar x
        current_x += step

    # Calcular la probabilidad según el operador
    probability = 0
    if operator == "=":
        probability = 0  # En distribuciones continuas, la probabilidad exacta es 0.
    elif operator == "<":
        probability = cdf_sum
    elif operator == ">":
        probability = 1 - cdf_sum
    elif operator == "<=":
        probability = cdf_sum
    elif operator == ">=":
        probability = 1 - cdf_sum
    else:
        raise HTTPException(status_code=400, detail="Operador no válido")

    # Retorno del resultado con probabilidades y valores de ejes
    return {
        "probability": round(probability, 6),  # Redondear a 6 decimales
        "x": x_axis,
        "f(x)": y_axis
    }
