import json
import httpx
from schemas import ApiCompositorResponse, ApiCompositorRequest
from config import server_settings


def calculate_vlp(input_data: ApiCompositorRequest):
    with httpx.Client() as client:
        vlp_params = {
            "inclinometry": {
                "MD": input_data.inclinometry.MD,
                "TVD": input_data.inclinometry.TVD,
            },
            "casing": {
                "d": input_data.casing.d,
            },
            "tubing": {
                "d": input_data.tubing.d,
                "h_mes": input_data.tubing.h_mes,
            },
            "pvt": {
                "wct": input_data.pvt.wct,
                "rp": input_data.pvt.rp,
                "gamma_oil": input_data.pvt.gamma_oil,
                "gamma_gas": input_data.pvt.gamma_gas,
                "gamma_wat": input_data.pvt.gamma_wat,
                "t_res": input_data.pvt.t_res,
            },
            "p_wh": input_data.p_wh,
            "geo_grad": input_data.geo_grad,
            "h_res": input_data.h_res,
        }
        resp = client.post(
            f"http://{server_settings.vlp_service_host}:{server_settings.vlp_service_port}/vlp/calculator",
            json=vlp_params,
        )
        resp = json.loads(resp.text)
    return resp


def calculate_ipr(input_data: ApiCompositorRequest):
    with httpx.Client() as client:
        ipr_params = {
            "p_res": input_data.p_res,
            "wct": input_data.pvt.wct,
            "pi": input_data.pi,
            "pb": input_data.pvt.pb,
        }
        resp = client.post(
            f"http://{server_settings.ipr_service_host}:{server_settings.ipr_service_port}/ipr/calc",
            json=ipr_params,
        )
        resp = json.loads(resp.text)
    return resp


def calculate_intersection_vlp_with_ipr(input_data: ApiCompositorRequest):
    vlp_nodes = calculate_vlp(input_data=input_data)
    ipr_nodes = calculate_ipr(input_data=input_data)

    with httpx.Client() as client:
        nodal_analysis_params = {
            "vlp": vlp_nodes,
            "ipr": ipr_nodes,
        }
        resp = client.post(
            f"http://{server_settings.nodal_analysis_host}:{server_settings.nodal_analysis_port}/nodal_analysis",
            json=nodal_analysis_params,
        )
        resp = json.loads(resp.text)
    return resp


async def calculate_data(
    input_data: ApiCompositorRequest,
) -> ApiCompositorResponse:
    return calculate_intersection_vlp_with_ipr(input_data=input_data)
