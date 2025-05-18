import React from 'react';
import { VehicleData } from '../types';
import { Search } from 'lucide-react';

interface SpeedMonitorProps {
  vehicles: VehicleData[];
  speedLimit: number;
}

const SpeedMonitor: React.FC<SpeedMonitorProps> = ({ vehicles, speedLimit }) => {
  const sortedVehicles = [...vehicles].sort((a, b) => b.speed - a.speed);
  
  return (
    <div className="bg-gray-800 rounded-lg shadow-lg overflow-hidden">
      <div className="p-3 bg-gray-700 border-b border-gray-600">
        <h2 className="font-semibold">Vehicle Speed Monitor</h2>
      </div>
      
      <div className="p-3">
        <div className="relative">
          <input
            type="text"
            placeholder="Search vehicle..."
            className="w-full p-2 pl-9 bg-gray-700 border border-gray-600 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <Search className="absolute left-2 top-2.5 h-4 w-4 text-gray-400" />
        </div>
      </div>
      
      <div className="overflow-y-auto" style={{ maxHeight: '300px' }}>
        <table className="w-full text-sm">
          <thead className="bg-gray-700 sticky top-0">
            <tr>
              <th className="p-2 text-left font-medium">License Plate</th>
              <th className="p-2 text-right font-medium">Speed</th>
              <th className="p-2 text-center font-medium">Status</th>
            </tr>
          </thead>
          <tbody>
            {sortedVehicles.map(vehicle => (
              <tr key={vehicle.id} className="border-b border-gray-700 hover:bg-gray-750">
                <td className="p-2">
                  <div className="flex items-center">
                    <div 
                      className="w-3 h-3 rounded-full mr-2" 
                      style={{ backgroundColor: vehicle.color }}
                    ></div>
                    <span>{vehicle.licensePlate}</span>
                  </div>
                </td>
                <td className="p-2 text-right font-mono">
                  {vehicle.speed} km/h
                </td>
                <td className="p-2">
                  <div className="flex justify-center">
                    {vehicle.speed > speedLimit ? (
                      <span className="px-2 py-0.5 bg-red-900/60 text-red-200 rounded-full text-xs">
                        Speeding
                      </span>
                    ) : (
                      <span className="px-2 py-0.5 bg-green-900/60 text-green-200 rounded-full text-xs">
                        Normal
                      </span>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <div className="p-3 border-t border-gray-700 text-xs text-gray-400">
        Tracked vehicles: {vehicles.length} | Updated: just now
      </div>
    </div>
  );
};

export default SpeedMonitor;