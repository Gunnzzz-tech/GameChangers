import React from 'react';
import { Car, AlertTriangle, Activity, Gauge } from 'lucide-react';

interface StatsPanelProps {
  stats: {
    totalVehicles: number;
    currentViolations: number;
    averageSpeed: number;
    alertsGenerated: number;
  };
}

const StatsPanel: React.FC<StatsPanelProps> = ({ stats }) => {
  return (
    <>
      <StatCard 
        title="Total Vehicles" 
        value={stats.totalVehicles}
        icon={<Car className="h-5 w-5 text-blue-400" />}
        color="blue"
      />
      
      <StatCard 
        title="Speed Violations" 
        value={stats.currentViolations}
        icon={<AlertTriangle className="h-5 w-5 text-yellow-400" />}
        color="yellow"
      />
      
      <StatCard 
        title="Avg. Speed" 
        value={`${stats.averageSpeed} km/h`}
        icon={<Gauge className="h-5 w-5 text-green-400" />}
        color="green"
      />
    </>
  );
};

interface StatCardProps {
  title: string;
  value: number | string;
  icon: React.ReactNode;
  color: 'blue' | 'yellow' | 'green' | 'red';
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon, color }) => {
  const getColorClass = () => {
    switch (color) {
      case 'blue': return 'from-blue-500/20 to-blue-600/5 border-blue-500/30';
      case 'yellow': return 'from-yellow-500/20 to-yellow-600/5 border-yellow-500/30';
      case 'green': return 'from-green-500/20 to-green-600/5 border-green-500/30';
      case 'red': return 'from-red-500/20 to-red-600/5 border-red-500/30';
    }
  };

  return (
    <div className={`bg-gradient-to-br ${getColorClass()} border border-opacity-50 rounded-lg p-4 shadow-lg`}>
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-sm font-medium text-gray-400 mb-1">{title}</h3>
          <p className="text-2xl font-bold">{value}</p>
        </div>
        <div className="p-2 bg-gray-800 rounded-lg">
          {icon}
        </div>
      </div>
    </div>
  );
};

export default StatsPanel;