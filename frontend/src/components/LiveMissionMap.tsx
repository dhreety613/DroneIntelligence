import { MapContainer, TileLayer, Marker, Polyline, Popup } from "react-leaflet";
import L from "leaflet";

type GeoPoint = {
  lat: number;
  lon: number;
};

type Props = {
  originalPath: GeoPoint[];
  adjustedPath?: GeoPoint[];
  currentPosition?: GeoPoint | null;
};

const droneIcon = new L.DivIcon({
  html: `<div style="background:#22c55e;width:18px;height:18px;border-radius:9999px;border:2px solid white;"></div>`,
  className: "",
  iconSize: [18, 18],
  iconAnchor: [9, 9],
});

const startIcon = new L.DivIcon({
  html: `<div style="background:#3b82f6;width:16px;height:16px;border-radius:9999px;border:2px solid white;"></div>`,
  className: "",
  iconSize: [16, 16],
  iconAnchor: [8, 8],
});

const goalIcon = new L.DivIcon({
  html: `<div style="background:#ef4444;width:16px;height:16px;border-radius:9999px;border:2px solid white;"></div>`,
  className: "",
  iconSize: [16, 16],
  iconAnchor: [8, 8],
});

export default function LiveMissionMap({
  originalPath,
  adjustedPath,
  currentPosition,
}: Props) {
  if (!originalPath || originalPath.length === 0) return null;

  const originalPositions: [number, number][] = originalPath.map((p) => [p.lat, p.lon]);
  const adjustedPositions: [number, number][] =
    adjustedPath?.map((p) => [p.lat, p.lon]) ?? [];

  const start = originalPositions[0];
  const goal = originalPositions[originalPositions.length - 1];
  const center = currentPosition
    ? ([currentPosition.lat, currentPosition.lon] as [number, number])
    : start;

  return (
    <MapContainer center={center} zoom={14} style={{ height: "560px", width: "100%", borderRadius: "12px" }}>
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <Polyline positions={originalPositions} pathOptions={{ color: "#38bdf8", weight: 5 }} />

      {adjustedPositions.length > 0 && (
        <Polyline
          positions={adjustedPositions}
          pathOptions={{ color: "#ef4444", weight: 5, dashArray: "10, 10" }}
        />
      )}

      <Marker position={start} icon={startIcon}>
        <Popup>Start</Popup>
      </Marker>

      <Marker position={goal} icon={goalIcon}>
        <Popup>Goal</Popup>
      </Marker>

      {currentPosition && (
        <Marker position={[currentPosition.lat, currentPosition.lon]} icon={droneIcon}>
          <Popup>Drone Current Position</Popup>
        </Marker>
      )}
    </MapContainer>
  );
}