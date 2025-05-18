import React from 'react';
import { AlertTriangle, X } from 'lucide-react';
import { Alert } from '../types';

interface AlertsPanelProps {
  alerts: Alert[];
}

const AlertsPanel: React.FC<AlertsPanelProps> = ({ alerts }) => {
  return (
    <div className="bg-gray-800 rounded-lg shadow-lg overflow-hidden">
      <div className="p-3 bg-gray-700 border-b border-gray-600 flex justify-between items-center">
        <h2 className="font-semibold flex items-center">
          <AlertTriangle className="h-4 w-4 mr-2 text-yellow-500" />
          Speed Violation Alerts
        </h2>
        <span className="bg-red-500 text-white px-2 py-0.5 rounded-full text-xs">
          {alerts.length}
        </span>
      </div>
      
      <div className="overflow-y-auto" style={{ maxHeight: '300px' }}>
        {alerts.length === 0 ? (
          <div className="p-4 text-center text-gray-500 text-sm">
            No speed violation alerts
          </div>
        ) : (
          <div className="divide-y divide-gray-700">
            {alerts.map(alert => (
              <div key={alert.id} className="p-3 hover:bg-gray-750 transition">
                <div className="flex justify-between items-start mb-1">
                  <div className="flex items-center">
                    <div className="w-8 h-8 bg-red-500/20 rounded-full flex items-center justify-center mr-2">
                      <AlertTriangle className="h-4 w-4 text-red-500" />
                    </div>
                    <div>
                      <h3 className="font-medium">License: {alert.licensePlate}</h3>
                      <p className="text-xs text-gray-400">
                        {alert.location} • {alert.timestamp.toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                  <button className="text-gray-500 hover:text-gray-300">
                    <X className="h-4 w-4" />
                  </button>
                </div>
                
                <div className="ml-10 mt-2 grid grid-cols-3 gap-2 text-xs">
                  <div className="bg-gray-700 p-2 rounded">
                    <span className="block text-gray-400">Speed</span>
                    <span className="font-medium text-red-400">{alert.speed} km/h</span>
                  </div>
                  <div className="bg-gray-700 p-2 rounded">
                    <span className="block text-gray-400">Duration</span>
                    <span className="font-medium">{alert.duration}</span>
                  </div>
                  <div className="bg-gray-700 p-2 rounded">
                    <span className="block text-gray-400">Status</span>
                    <span className="font-medium text-yellow-400">Pending</span>
                  </div>
                </div>
                
                <div className="mt-2 ml-10">
                  <button className="bg-blue-600 hover:bg-blue-700 text-white text-xs px-3 py-1 rounded transition mr-2">
                    Send Alert
                  </button>
                  <button className="bg-gray-700 hover:bg-gray-600 text-white text-xs px-3 py-1 rounded transition">
                    Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      
      {alerts.length > 0 && (
        <div className="p-2 border-t border-gray-700 flex justify-between items-center text-xs">
          <button className="text-blue-400 hover:text-blue-300">
            View all alerts
          </button>
          <button className="text-gray-400 hover:text-gray-300">
            Clear all
          </button>
        </div>
      )}
    </div>
  );
};

export default AlertsPanel;