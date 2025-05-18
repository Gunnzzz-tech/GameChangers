export interface VehicleData {
  id: string;
  x: number;
  y: number;
  direction: 'left' | 'right';
  speed: number;
  color: string;
  licensePlate: string;
  alerted: boolean;
  speedHistory: number[];
  lastUpdated: Date;
}

export interface Alert {
  id: string;
  vehicleId: string;
  licensePlate: string;
  speed: number;
  duration: string;
  timestamp: Date;
  location: string;
}