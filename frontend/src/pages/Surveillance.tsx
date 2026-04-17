export default function Surveillance() {
  return (
    <div className="p-6 text-white bg-black h-screen">
      <h2 className="text-2xl mb-4">Live Drone Feed</h2>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gray-800 rounded-lg h-64 flex items-center justify-center">
          Image Frame
        </div>
        <div className="bg-gray-800 rounded-lg h-64 flex items-center justify-center">
          Video Feed
        </div>
      </div>

      <div className="mt-4 bg-gray-800 p-4 rounded">
        <p>Battery: 82%</p>
        <p>Altitude: 120m</p>
        <p>Speed: 14 m/s</p>
      </div>
    </div>
  );
}