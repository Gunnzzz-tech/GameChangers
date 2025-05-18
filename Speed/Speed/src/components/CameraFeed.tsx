import React, { useRef, useEffect } from 'react';
import { VehicleData } from '../types';

interface CameraFeedProps {
  vehicles: VehicleData[];
  speedLimit: number;
}

const CameraFeed: React.FC<CameraFeedProps> = ({ vehicles, speedLimit }) => {
  const feedRef = useRef<HTMLDivElement>(null);
  
  // Draw road markings on canvas
  useEffect(() => {
    const drawRoadMarkings = () => {
      if (!feedRef.current) return;
      const canvas = document.createElement('canvas');
      const container = feedRef.current;
      const width = container.clientWidth;
      const height = container.clientHeight;
      
      canvas.width = width;
      canvas.height = height;
      canvas.style.position = 'absolute';
      canvas.style.top = '0';
      canvas.style.left = '0';
      canvas.style.zIndex = '1';
      
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      
      // Draw road
      ctx.fillStyle = '#333';
      ctx.fillRect(0, 0, width, height);
      
      // Draw road markings
      ctx.strokeStyle = '#FFF';
      ctx.setLineDash([20, 20]);
      ctx.lineWidth = 4;
      
      // Center line
      ctx.beginPath();
      ctx.moveTo(0, height / 2);
      ctx.lineTo(width, height / 2);
      ctx.stroke();
      
      // Shoulder lines
      ctx.beginPath();
      ctx.moveTo(0, height * 0.25);
      ctx.lineTo(width, height * 0.25);
      ctx.stroke();
      
      ctx.beginPath();
      ctx.moveTo(0, height * 0.75);
      ctx.lineTo(width, height * 0.75);
      ctx.stroke();
      
      // Add canvas to container
      container.innerHTML = '';
      container.appendChild(canvas);
    };
    
    drawRoadMarkings();
    window.addEventListener('resize', drawRoadMarkings);
    
    return () => window.removeEventListener('resize', drawRoadMarkings);
  }, []);
  
  return (
    <div className="bg-gray-800 rounded-lg overflow-hidden shadow-lg">
      <div className="p-3 bg-gray-700 border-b border-gray-600 flex justify-between items-center">
        <h2 className="font-semibold text-lg">Live Camera Feed</h2>
        <div className="flex items-center">
          <div className="h-2 w-2 bg-red-500 rounded-full animate-pulse mr-2"></div>
          <span className="text-xs text-gray-300">LIVE</span>
        </div>
      </div>
      
      <div className="camera-feed bg-gray-900" ref={feedRef}>
        {vehicles.map(vehicle => (
          <div
            key={vehicle.id}
            className={`vehicle ${vehicle.speed > speedLimit ? 'vehicle-fast' : 'vehicle-normal'}`}
            style={{
              left: `${vehicle.x}%`,
              top: `${vehicle.y}%`,
              width: '50px',
              height: '30px',
              background: vehicle.color,
              borderRadius: '4px',
              zIndex: 2,
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              fontSize: '10px',
              transform: `rotate(${vehicle.direction === 'right' ? 0 : 180}deg)`
            }}
          >
            {vehicle.speed > speedLimit && !vehicle.alerted && (
              <div className="absolute -top-4 px-2 py-0.5 bg-red-500 text-white text-xs rounded-sm">
                {vehicle.speed} km/h
              </div>
            )}
            {vehicle.alerted && (
              <div className="absolute -top-4 px-2 py-0.5 bg-red-500 text-white text-xs rounded-sm alert-pulse">
                ALERT
              </div>
            )}
          </div>
        ))}
      </div>
      
      <div className="p-3 bg-gray-700 border-t border-gray-600 flex justify-between text-sm">
        <span>Camera #1 - Main Highway</span>
        <span>Speed Limit: {speedLimit} km/h</span>
      </div>
    </div>
  );
};

export default CameraFeed;