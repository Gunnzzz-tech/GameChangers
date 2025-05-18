import { VehicleData } from '../types';

// License plate generation
const generateLicensePlate = (): string => {
  const letters = 'ABCDEFGHJKLMNPQRSTUVWXYZ';
  const letter1 = letters[Math.floor(Math.random() * letters.length)];
  const letter2 = letters[Math.floor(Math.random() * letters.length)];
  const numbers = Math.floor(1000 + Math.random() * 9000);
  return `${letter1}${letter2}-${numbers}`;
};

// Vehicle colors
const vehicleColors = [
  '#3B82F6', // blue
  '#EF4444', // red
  '#10B981', // green
  '#F59E0B', // yellow
  '#8B5CF6', // purple
  '#EC4899', // pink
  '#6B7280', // gray
  '#FFFFFF', // white
  '#000000', // black
];

// Generate random vehicle data
export const generateVehicleData = (count: number): VehicleData[] => {
  const vehicles: VehicleData[] = [];
  
  for (let i = 0; i < count; i++) {
    const direction = Math.random() > 0.5 ? 'right' : 'left';
    const x = direction === 'right' ? 0 : 100;
    const lane = Math.random() > 0.5 ? 0.25 : 0.75;
    
    vehicles.push({
      id: `vehicle-${Date.now()}-${i}`,
      x,
      y: lane * 100,
      direction,
      speed: Math.floor(40 + Math.random() * 80), // 40-120 km/h
      color: vehicleColors[Math.floor(Math.random() * vehicleColors.length)],
      licensePlate: generateLicensePlate(),
      alerted: false,
      speedHistory: [],
      lastUpdated: new Date()
    });
  }
  
  return vehicles;
};

// Update vehicle positions based on their speed and direction
export const updateVehiclePositions = (vehicles: VehicleData[]): VehicleData[] => {
  const updatedVehicles = [...vehicles];
  const toRemove: string[] = [];
  
  updatedVehicles.forEach(vehicle => {
    // Update position based on direction and speed
    const speedFactor = vehicle.speed / 50; // Convert speed to movement units
    
    if (vehicle.direction === 'right') {
      vehicle.x += speedFactor;
      if (vehicle.x > 110) {
        toRemove.push(vehicle.id);
      }
    } else {
      vehicle.x -= speedFactor;
      if (vehicle.x < -10) {
        toRemove.push(vehicle.id);
      }
    }
    
    // Randomly vary speed a bit to simulate real traffic
    const speedVariation = Math.random() * 10 - 5; // -5 to +5
    vehicle.speed = Math.max(30, Math.min(130, vehicle.speed + speedVariation));
    
    // Keep speed history (for 5 minute/300 data point window)
    vehicle.speedHistory.push(vehicle.speed);
    if (vehicle.speedHistory.length > 300) {
      vehicle.speedHistory.shift();
    }
    
    vehicle.lastUpdated = new Date();
  });
  
  // Remove vehicles that are off-screen and add new ones to maintain count
  const newVehicles = updatedVehicles.filter(v => !toRemove.includes(v.id));
  const replacements = generateVehicleData(toRemove.length);
  
  return [...newVehicles, ...replacements];
};