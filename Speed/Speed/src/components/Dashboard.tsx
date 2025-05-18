import React, { useState, useEffect } from 'react';
import CameraFeed from './CameraFeed';
import SpeedMonitor from './SpeedMonitor';
import AlertsPanel from './AlertsPanel';
import StatsPanel from './StatsPanel';
import ConfigPanel from './ConfigPanel';
import { VehicleData, Alert } from '../types';
import { generateVehicleData, updateVehiclePositions } from '../utils/simulation';

const Dashboard: React.FC = () => {
  const [vehicles, setVehicles] = useState<VehicleData[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [speedLimit, setSpeedLimit] = useState<number>(80);
  const [overspeededVehicles, setOverspeededVehicles] = useState<{[key: string]: number}>({});
  const [stats, setStats] = useState({
    totalVehicles: 0,
    currentViolations: 0,
    averageSpeed: 0,
    alertsGenerated: 0
  });
  
  // Generate initial vehicles
  useEffect(() => {
    const initialVehicles = generateVehicleData(6);
    setVehicles(initialVehicles);
    setStats(prev => ({...prev, totalVehicles: initialVehicles.length}));
    
    // Update vehicle positions and speeds every 100ms
    const intervalId = setInterval(() => {
      setVehicles(prevVehicles => {
        const updatedVehicles = updateVehiclePositions(prevVehicles);
        
        // Calculate current stats
        const totalSpeed = updatedVehicles.reduce((sum, v) => sum + v.speed, 0);
        const avgSpeed = updatedVehicles.length ? Math.round(totalSpeed / updatedVehicles.length) : 0;
        const speeding = updatedVehicles.filter(v => v.speed > speedLimit).length;
        
        setStats(prev => ({
          ...prev, 
          averageSpeed: avgSpeed,
          currentViolations: speeding
        }));
        
        // Track overspeeding vehicles
        const overspeeding: {[key: string]: number} = {...overspeededVehicles};
        
        updatedVehicles.forEach(vehicle => {
          if (vehicle.speed > speedLimit) {
            overspeeding[vehicle.id] = (overspeeding[vehicle.id] || 0) + 1;
            
            // If vehicle has been overspeeding for "5 minutes" (300 simulation ticks)
            if (overspeeding[vehicle.id] >= 300 && !vehicle.alerted) {
              const newAlert: Alert = {
                id: `alert-${Date.now()}`,
                vehicleId: vehicle.id,
                licensePlate: vehicle.licensePlate,
                speed: vehicle.speed,
                duration: "5+ minutes",
                timestamp: new Date(),
                location: "Main Highway - Camera #1"
              };
              
              setAlerts(prev => [newAlert, ...prev]);
              setStats(prev => ({...prev, alertsGenerated: prev.alertsGenerated + 1}));
              
              // Mark vehicle as alerted
              vehicle.alerted = true;
            }
          } else {
            // Reset counter if vehicle is no longer speeding
            delete overspeeding[vehicle.id];
          }
        });
        
        setOverspeededVehicles(overspeeding);
        return updatedVehicles;
      });
    }, 100);
    
    return () => clearInterval(intervalId);
  }, [speedLimit]);
  
  const handleSpeedLimitChange = (newLimit: number) => {
    setSpeedLimit(newLimit);
  };
  
  return (
    <div className="container mx-auto p-4 grid grid-cols-1 md:grid-cols-3 gap-4">
      <div className="md:col-span-2 space-y-4">
        <CameraFeed vehicles={vehicles} speedLimit={speedLimit} />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <StatsPanel stats={stats} />
        </div>
      </div>
      
      <div className="space-y-4">
        <SpeedMonitor vehicles={vehicles} speedLimit={speedLimit} />
        <AlertsPanel alerts={alerts} />
        <ConfigPanel speedLimit={speedLimit} onSpeedLimitChange={handleSpeedLimitChange} />
      </div>
    </div>
  );
};

export default Dashboard;