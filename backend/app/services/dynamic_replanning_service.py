from app.schemas.replanning import ReplanningRequest, GeoRouteStep
from app.services.costmap_generation_service import CostmapGenerationService
from app.services.local_obstacle_service import LocalObstacleService
from app.services.local_weather_service import LocalWeatherService
from app.services.obstacle_detection_service import ObstacleDetectionService
from app.services.terrain_analysis_service import TerrainAnalysisService
from app.services.weather_analysis_service import WeatherAnalysisService
from app.services.fusion_service import FusionService
from app.schemas.analysis import WeatherAnalysisInput
from app.utils.graph_utils import GraphUtils
from app.utils.geo_utils import grid_to_geo
from app.utils.terrain_utils import generate_fake_elevation


class DynamicReplanningService:
    def __init__(self) -> None:
        self.costmap_service = CostmapGenerationService()
        self.local_obstacle_service = LocalObstacleService()
        self.local_weather_service = LocalWeatherService()

        self.obstacle_service = ObstacleDetectionService()
        self.terrain_service = TerrainAnalysisService()
        self.weather_service = WeatherAnalysisService()
        self.fusion_service = FusionService()

    def replan(self, mission, payload: ReplanningRequest) -> dict:
        obstacle_result = self.obstacle_service.analyze_image(mission.image_path)

        rows = max(mission.start_row, mission.goal_row, 19) + 1
        cols = max(mission.start_col, mission.goal_col, 19) + 1
        rows = max(rows, 20)
        cols = max(cols, 20)

        elevation = generate_fake_elevation(rows, cols)
        terrain_result = self.terrain_service.analyze_elevation(elevation)

        weather_result = None
        fused = self.fusion_service.fuse(
            obstacle_analysis=obstacle_result,
            terrain_analysis=terrain_result,
            weather_analysis=weather_result,
        )

        costmap = self.costmap_service.generate_costmap(
            analysis=fused,
            rows=rows,
            cols=cols,
        )

        if payload.local_obstacle is not None:
            local_obstacle = self.local_obstacle_service.analyze(payload.local_obstacle)
            r = local_obstacle["row"]
            c = local_obstacle["col"]
            if 0 <= r < rows and 0 <= c < cols:
                if local_obstacle["blocked"]:
                    costmap[r][c] = float("inf")
                else:
                    costmap[r][c] += local_obstacle["penalty"]

                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and costmap[nr][nc] != float("inf"):
                            if dr == 0 and dc == 0:
                                continue
                            costmap[nr][nc] += local_obstacle["penalty"] * 0.4

        if payload.local_weather is not None:
            local_weather = self.local_weather_service.analyze(payload.local_weather)

            if local_weather["no_fly"]:
                return {
                    "mission_id": mission.mission_id,
                    "feasible": False,
                    "algorithm": payload.algorithm,
                    "old_remaining_waypoints": max(0, mission.total_waypoints - 1 - mission.current_waypoint_index),
                    "new_total_waypoints": mission.total_waypoints,
                    "current_row": mission.current_row,
                    "current_col": mission.current_col,
                    "goal_row": mission.goal_row,
                    "goal_col": mission.goal_col,
                    "total_cost": mission.total_cost,
                    "adjusted_geo_path": [],
                    "message": f"Replanning aborted: {local_weather['reason'] or 'unsafe local weather.'}",
                }

            for r in range(rows):
                for c in range(cols):
                    if costmap[r][c] != float("inf"):
                        costmap[r][c] += local_weather["penalty"] * 0.25

        start = (mission.current_row, mission.current_col)
        goal = (mission.goal_row, mission.goal_col)

        if costmap[start[0]][start[1]] == float("inf"):
            raise ValueError("Current drone position is blocked; cannot replan from current location.")

        if costmap[goal[0]][goal[1]] == float("inf"):
            raise ValueError("Goal position is blocked; cannot replan to destination.")

        if payload.algorithm == "astar":
            path, total_cost = GraphUtils.astar(
                costmap,
                start,
                goal,
                diagonal=payload.diagonal_movement,
            )
        else:
            path, total_cost = GraphUtils.dijkstra(
                costmap,
                start,
                goal,
                diagonal=payload.diagonal_movement,
            )

        if not path:
            return {
                "mission_id": mission.mission_id,
                "feasible": False,
                "algorithm": payload.algorithm,
                "old_remaining_waypoints": max(0, mission.total_waypoints - 1 - mission.current_waypoint_index),
                "new_total_waypoints": mission.total_waypoints,
                "current_row": mission.current_row,
                "current_col": mission.current_col,
                "goal_row": mission.goal_row,
                "goal_col": mission.goal_col,
                "total_cost": mission.total_cost,
                "adjusted_geo_path": [],
                "message": "No feasible replanned route found.",
            }

        from app.models.mission import MissionWaypoint
        new_waypoints = [
            MissionWaypoint(
                row=step["row"],
                col=step["col"],
                cumulative_cost=step["cumulative_cost"],
            )
            for step in path
        ]

        adjusted_geo_path = []
        for step in path:
            lat, lon = grid_to_geo(
                row=step["row"],
                col=step["col"],
                rows=rows,
                cols=cols,
                bounds=mission.bounds,
            )
            adjusted_geo_path.append(GeoRouteStep(lat=lat, lon=lon))

        old_remaining = max(0, mission.total_waypoints - 1 - mission.current_waypoint_index)

        mission.waypoints = new_waypoints
        mission.total_waypoints = len(new_waypoints)
        mission.current_waypoint_index = 0
        mission.current_row = new_waypoints[0].row
        mission.current_col = new_waypoints[0].col
        mission.total_cost = total_cost
        mission.algorithm = payload.algorithm

        return {
            "mission_id": mission.mission_id,
            "feasible": True,
            "algorithm": payload.algorithm,
            "old_remaining_waypoints": old_remaining,
            "new_total_waypoints": len(new_waypoints),
            "current_row": mission.current_row,
            "current_col": mission.current_col,
            "goal_row": mission.goal_row,
            "goal_col": mission.goal_col,
            "total_cost": total_cost,
            "adjusted_geo_path": adjusted_geo_path,
            "message": "Mission route replanned successfully from current position.",
        }