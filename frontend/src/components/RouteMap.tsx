import { MapContainer, TileLayer, Marker, Polyline, Popup } from "react-leaflet";
import L from "leaflet";

type GeoRouteStep = {
  lat: number;
  lon: number;
};

type RouteMapProps = {
  geoPath: GeoRouteStep[];
};

const startIcon = new L.DivIcon({
  html: `<div style="background:#22c55e;width:18px;height:18px;border-radius:9999px;border:2px solid white;"></div>`,
  className: "",
  iconSize: [18, 18],
  iconAnchor: [9, 9],
});

const goalIcon = new L.DivIcon({
  html: `<div style="background:#ef4444;width:18px;height:18px;border-radius:9999px;border:2px solid white;"></div>`,
  className: "",
  iconSize: [18, 18],
  iconAnchor: [9, 9],
});

export default function RouteMap({ geoPath }: RouteMapProps) {
  if (!geoPath || geoPath.length === 0) return null;

  const positions: [number, number][] = geoPath.map((p) => [p.lat, p.lon]);
  const start = positions[0];
  const goal = positions[positions.length - 1];

  return (
    <MapContainer
      center={start}
      zoom={14}
      style={{ height: "520px", width: "100%", borderRadius: "12px" }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <Polyline positions={positions} pathOptions={{ color: "#38bdf8", weight: 5 }} />

      <Marker position={start} icon={startIcon}>
        <Popup>Start</Popup>
      </Marker>

      <Marker position={goal} icon={goalIcon}>
        <Popup>Goal</Popup>
      </Marker>
    </MapContainer>
  );
}