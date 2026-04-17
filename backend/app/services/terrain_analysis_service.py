import numpy as np
from app.schemas.analysis import TerrainAnalysisResult


class TerrainAnalysisService:
    def compute_slope(self, elevation: np.ndarray) -> np.ndarray:
        dx, dy = np.gradient(elevation)
        slope = np.sqrt(dx**2 + dy**2)
        return slope

    def compute_roughness(self, elevation: np.ndarray) -> float:
        return float(np.std(elevation))

    def analyze_elevation(self, elevation_grid: np.ndarray) -> TerrainAnalysisResult:
        slope = self.compute_slope(elevation_grid)
        avg_slope = float(np.mean(slope))
        roughness = self.compute_roughness(elevation_grid)

        slope_score = min(1.0, avg_slope / 30.0)
        roughness_score = min(1.0, roughness / 50.0)
        difficulty_score = 0.6 * slope_score + 0.4 * roughness_score

        if difficulty_score > 0.75:
            terrain_class = "mountainous"
        elif difficulty_score > 0.5:
            terrain_class = "hilly"
        elif difficulty_score > 0.25:
            terrain_class = "moderate"
        else:
            terrain_class = "flat"

        recommended_penalty = round(1 + 5 * difficulty_score, 3)

        return TerrainAnalysisResult(
            image_path="generated_elevation_grid",
            terrain_class=terrain_class,
            difficulty_score=round(difficulty_score, 3),
            edge_density=0.0,
            texture_variance=0.0,
            vegetation_ratio=0.0,
            water_ratio=0.0,
            builtup_ratio=0.0,
            recommended_penalty=recommended_penalty,
        )