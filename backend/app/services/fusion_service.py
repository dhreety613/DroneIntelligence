from typing import List, Optional

from app.schemas.analysis import (
    EnvironmentAnalysisResponse,
    ObstacleAnalysisResult,
    TerrainAnalysisResult,
    WeatherAnalysisResult,
    RiskZone,
)


class FusionService:
    def fuse(
        self,
        obstacle_analysis: ObstacleAnalysisResult,
        terrain_analysis: TerrainAnalysisResult,
        weather_analysis: Optional[WeatherAnalysisResult] = None,
    ) -> EnvironmentAnalysisResponse:
        obstacle_risk = 0.0
        if obstacle_analysis.obstacle_count > 0:
            avg_obstacle_risk = sum(d.risk_weight for d in obstacle_analysis.detections) / obstacle_analysis.obstacle_count
            obstacle_risk = min(1.0, 0.4 + 0.6 * avg_obstacle_risk)

        terrain_risk = terrain_analysis.difficulty_score
        weather_risk = weather_analysis.risk_score if weather_analysis else 0.0

        combined_risk_score = min(
            1.0,
            0.45 * obstacle_risk + 0.30 * terrain_risk + 0.25 * weather_risk,
        )

        route_penalty = round(
            1.0
            + 5.0 * obstacle_risk
            + 3.0 * terrain_risk
            + 4.0 * weather_risk,
            3,
        )

        feasible = True
        recommended_action = "Proceed with route planning."

        risk_zones: List[RiskZone] = []

        if obstacle_analysis.blocked:
            risk_zones.append(
                RiskZone(
                    zone_type="obstacle",
                    score=round(obstacle_risk, 3),
                    description="Current frame has dense or large obstacles.",
                )
            )
            feasible = False
            recommended_action = "Avoid this region or wait for alternate frame analysis."

        if terrain_analysis.difficulty_score >= 0.7:
            risk_zones.append(
                RiskZone(
                    zone_type="terrain",
                    score=terrain_analysis.difficulty_score,
                    description=f"Terrain classified as {terrain_analysis.terrain_class} with high traversal difficulty.",
                )
            )

        if weather_analysis:
            if weather_analysis.no_fly:
                risk_zones.append(
                    RiskZone(
                        zone_type="weather",
                        score=weather_analysis.risk_score,
                        description=weather_analysis.reason or "Unsafe weather conditions detected.",
                    )
                )
                feasible = False
                recommended_action = "Do not fly. Reassess after weather improves."
            elif weather_analysis.risk_score >= 0.5:
                risk_zones.append(
                    RiskZone(
                        zone_type="weather",
                        score=weather_analysis.risk_score,
                        description=weather_analysis.reason or "Moderately risky weather conditions.",
                    )
                )

        if feasible and combined_risk_score >= 0.75:
            recommended_action = "High-risk region. Use strong penalty during route planning."
        elif feasible and combined_risk_score >= 0.45:
            recommended_action = "Moderate risk. Route planner should prefer alternate safe corridors."

        return EnvironmentAnalysisResponse(
            image_path=obstacle_analysis.image_path,
            obstacle_analysis=obstacle_analysis,
            terrain_analysis=terrain_analysis,
            weather_analysis=weather_analysis,
            combined_risk_score=round(combined_risk_score, 3),
            route_penalty=route_penalty,
            feasible=feasible,
            risk_zones=risk_zones,
            recommended_action=recommended_action,
        )