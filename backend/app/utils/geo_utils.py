from app.schemas.route import MissionBounds


def grid_to_geo(row: int, col: int, rows: int, cols: int, bounds: MissionBounds) -> tuple[float, float]:
    lat = bounds.north - ((row + 0.5) / rows) * (bounds.north - bounds.south)
    lon = bounds.west + ((col + 0.5) / cols) * (bounds.east - bounds.west)
    return lat, lon