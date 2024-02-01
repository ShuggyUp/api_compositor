from typing import List
from fastapi import APIRouter, Body
from schemas import ApiCompositorResponse, ApiCompositorRequest
from controllers import api_compositor as api_compositor_controller

router = APIRouter(prefix="/api_compositor", tags=["api_compositor_service"])


@router.post("", response_model=List[ApiCompositorResponse])
async def calculate_data(
    input_data: ApiCompositorRequest = Body(...),
):
    """
    Вычисляет значения для построения прямых и нахождения их точек пересечения
    """
    return await api_compositor_controller.calculate_data(input_data=input_data)
