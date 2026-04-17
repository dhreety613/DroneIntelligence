from typing import List

from app.schemas.analysis import EnvironmentAnalysisResponse


class CostmapGenerationService:
    """
    Converts Step 2 fused analysis into a weighted grid.
    Lower values = easier/safer traversal.
    Higher values = riskier traversal.
    inf = blocked.
    """

    def generate_costmap(
        self,
        analysis: EnvironmentAnalysisResponse,
        rows: int,
        cols: int,
    ) -> List[List[float]]:
        base_cost = 1.0

        grid = [[base_cost for _ in range(cols)] for _ in range(rows)]

        # 1. Apply terrain difficulty globally as a base multiplier
        terrain_penalty = analysis.terrain_analysis.recommended_penalty
        for r in range(rows):
            for c in range(cols):
                grid[r][c] += 0.35 * terrain_penalty

        # 2. Apply weather penalty globally if weather exists
        if analysis.weather_analysis is not None:
            weather_penalty = analysis.weather_analysis.total_weather_penalty
            for r in range(rows):
                for c in range(cols):
                    grid[r][c] += 3.0 * weather_penalty

            if analysis.weather_analysis.no_fly:
                # Entire map marked highly risky, but not fully blocked
                for r in range(rows):
                    for c in range(cols):
                        grid[r][c] += 8.0

        # 3. Project obstacle detections into grid cells
        img_w = 640.0
        img_h = 640.0

        for det in analysis.obstacle_analysis.detections:
            center_x = det.center_x
            center_y = det.center_y

            col = min(cols - 1, max(0, int((center_x / img_w) * cols)))
            row = min(rows - 1, max(0, int((center_y / img_h) * rows)))

            obstacle_penalty = 4.0 + 6.0 * det.risk_weight
            grid[row][col] += obstacle_penalty

            # Spread some penalty to neighboring cells
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if dr == 0 and dc == 0:
                            continue
                        grid[nr][nc] += obstacle_penalty * 0.35

            # Mark very large / high-risk obstacles as blocked
            if det.risk_weight >= 0.9 or (det.width * det.height) > 80000:
                grid[row][col] = float("inf")

        # 4. If fused analysis says infeasible due to blocked region, strengthen penalties
        if not analysis.feasible and analysis.weather_analysis is None:
            for r in range(rows):
                for c in range(cols):
                    grid[r][c] += 1.5

        return [[round(cell, 3) if cell != float("inf") else cell for cell in row] for row in grid]