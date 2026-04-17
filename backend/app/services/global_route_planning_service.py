from app.schemas.route import (
    RoutePlanningRequest,
    RoutePlanningResponse,
    RouteStep,
    GeoRouteStep,
)
from app.services.obstacle_detection_service import ObstacleDetectionService
from app.services.terrain_analysis_service import TerrainAnalysisService
from app.services.weather_analysis_service import WeatherAnalysisService
from app.services.fusion_service import FusionService
from app.services.costmap_generation_service import CostmapGenerationService
from app.services.weather_api_service import WeatherAPIService
from app.schemas.analysis import WeatherAnalysisInput
from app.utils.graph_utils import GraphUtils
from app.utils.terrain_utils import generate_fake_elevation
from app.utils.geo_utils import grid_to_geo


class GlobalRoutePlanningService:
    def __init__(self) -> None:
        self.obstacle_service = ObstacleDetectionService()
        self.terrain_service = TerrainAnalysisService()
        self.weather_service = WeatherAnalysisService()
        self.fusion_service = FusionService()
        self.costmap_service = CostmapGenerationService()
        self.weather_api = WeatherAPIService()

    def plan_route(self, payload: RoutePlanningRequest) -> RoutePlanningResponse:
        obstacle_result = self.obstacle_service.analyze_image(payload.image_path)

        elevation = generate_fake_elevation(
            payload.costmap.rows,
            payload.costmap.cols,
        )
        terrain_result = self.terrain_service.analyze_elevation(elevation)

        weather_result = None
        if payload.include_weather:
            lat, lon = 26.7271, 88.3953
            weather_data = self.weather_api.get_weather(lat, lon)
            weather_input = WeatherAnalysisInput(**weather_data)
            weather_result = self.weather_service.analyze(weather_input)

        fused = self.fusion_service.fuse(
            obstacle_analysis=obstacle_result,
            terrain_analysis=terrain_result,
            weather_analysis=weather_result,
        )

        rows = payload.costmap.rows
        cols = payload.costmap.cols

        if payload.start.row >= rows or payload.start.col >= cols:
            raise ValueError("Start point is outside costmap bounds.")

        if payload.goal.row >= rows or payload.goal.col >= cols:
            raise ValueError("Goal point is outside costmap bounds.")

        costmap = self.costmap_service.generate_costmap(
            analysis=fused,
            rows=rows,
            cols=cols,
        )

        start = (payload.start.row, payload.start.col)
        goal = (payload.goal.row, payload.goal.col)

        if costmap[start[0]][start[1]] == float("inf"):
            raise ValueError("Start point is blocked.")

        if costmap[goal[0]][goal[1]] == float("inf"):
            raise ValueError("Goal point is blocked.")

        if payload.algorithm == "astar":
            path, total_cost = GraphUtils.astar(
                costmap,
                start,
                goal,
                diagonal=payload.costmap.diagonal_movement,
            )
        else:
            path, total_cost = GraphUtils.dijkstra(
                costmap,
                start,
                goal,
                diagonal=payload.costmap.diagonal_movement,
            )

        feasible = len(path) > 0 and total_cost != float("inf")

        message = (
            "Route planned successfully."
            if feasible
            else "No feasible route found for the given environment."
        )

        route_steps = [RouteStep(**step) for step in path]

        geo_steps = []
        for step in path:
            lat, lon = grid_to_geo(
                row=step["row"],
                col=step["col"],
                rows=rows,
                cols=cols,
                bounds=payload.bounds,
            )
            geo_steps.append(GeoRouteStep(lat=lat, lon=lon))

        return RoutePlanningResponse(
            algorithm=payload.algorithm,
            image_path=payload.image_path,
            feasible=feasible,
            start=payload.start,
            goal=payload.goal,
            total_cost=0.0 if total_cost == float("inf") else total_cost,
            path_length=len(route_steps),
            path=route_steps,
            geo_path=geo_steps,
            message=message,
            costmap_rows=rows,
            costmap_cols=cols,
            bounds=payload.bounds,
        )