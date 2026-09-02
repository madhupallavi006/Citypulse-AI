from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.route_service import get_optimized_route

router = APIRouter(prefix="/api/routes", tags=["Route Optimization"])

class RouteRequest(BaseModel):
    origin: str = "J01"
    destination: str = "J08"
    consider_predictions: bool = True

@router.get("")
def get_routes(origin: str = "J01", destination: str = "J08"):
    route_data = get_optimized_route(origin, destination)
    return {
        "status": "success",
        "route_comparison": route_data
    }

@router.post("")
def optimize_route(req: RouteRequest):
    route_data = get_optimized_route(req.origin, req.destination)
    return {
        "status": "success",
        "route_comparison": route_data
    }
