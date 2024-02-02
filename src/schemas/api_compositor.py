from typing import List
from pydantic import BaseModel, Field, field_validator


class Inclinometry(BaseModel):
    """
    Схема для валидации данных инклинометрии
    """

    MD: List[float] = Field(title="Измеренная по стволу глубина, м")
    TVD: List[float] = Field(title="Вертикальная глубина, м")

    @field_validator("MD", "TVD")
    def check_positive_numbers(cls, v, values, **kwargs):
        for node in v:
            if node < 0:
                raise ValueError("Числа должны быть больше 0")
        return v


class Pipeline(BaseModel):
    """
    Схема для валидации данных по ЭК
    """

    d: float = Field(title="Диаметр трубы, м", gt=0)


class Tubing(Pipeline):
    """
    Схема для валидации данных по НКТ
    """

    h_mes: float = Field(title="Глубина спуска НКТ, м", gt=0)


class PVT(BaseModel):
    """
    Схема для валидации данных PVT
    """

    wct: float = Field(title="Обводненность, %", ge=0, le=100)
    rp: float = Field(title="Газовый фактор, м3/т", ge=0)
    gamma_oil: float = Field(title="Отн. плотность нефти, доли", ge=0.6, le=1)
    gamma_gas: float = Field(title="Отн. плотность газа, доли", ge=0.5, le=1)
    gamma_wat: float = Field(title="Отн. плотность воды, доли", ge=0.98, le=1.2)
    t_res: float = Field(title="Пластовая температура, C", ge=10, le=500)
    pb: float = Field(title="Давление насыщения, атм")


class ApiCompositorRequest(BaseModel):
    """
    Схема для валидации взодных данных
    """

    inclinometry: Inclinometry = Field(title="Инклинометрия")
    casing: Pipeline = Field(title="Данные по ЭК")
    tubing: Tubing = Field(title="Данные по НКТ")
    pvt: PVT = Field(title="PVT")
    p_wh: float = Field(title="Буферное давление, атм", ge=0)
    geo_grad: float = Field(title="Градиент температуры, C/100 м", ge=0)
    h_res: float = Field(title="Глубина Верхних Дыр Перфорации, м", ge=0)
    p_res: float = Field(title="Пластовое давление, атм", ge=0)
    pi: float = Field(title="Коэффициент продуктивности, м3/сут/атм", ge=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "inclinometry": {"MD": [0, 1000, 1500], "TVD": [0, 1000, 1100]},
                "casing": {"d": 0.1},
                "tubing": {"d": 0.062, "h_mes": 1000},
                "pvt": {
                    "wct": 50,
                    "rp": 100,
                    "gamma_oil": 0.8,
                    "gamma_gas": 0.7,
                    "gamma_wat": 1,
                    "t_res": 90,
                    "pb": 150,
                },
                "p_wh": 10,
                "geo_grad": 3,
                "h_res": 1500,
                "p_res": 200,
                "pi": 1,
            }
        }
    }


class ApiCompositorResponse(BaseModel):
    """
    Схема для валидации ответа сервиса (точек пересечения Vlp и Ipr кривых)
    """

    p_wf: float = Field(title="Забойные давления, атм", ge=0)
    q_liq: float = Field(title="Дебиты жидкости, м3/сут", ge=0)

    model_config = {"json_schema_extra": {"example": {"p_wf": 200, "q_liq": 0}}}
