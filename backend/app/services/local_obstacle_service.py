from app.schemas.replanning import LocalObstacleEvent


class LocalObstacleService:
    def analyze(self, event: LocalObstacleEvent) -> dict:
        penalty = 5.0 + 10.0 * event.severity
        blocked = event.severity >= 0.85

        return {
            "row": event.row,
            "col": event.col,
            "severity": event.severity,
            "label": event.label,
            "source": event.source,
            "penalty": round(penalty, 3),
            "blocked": blocked,
        }