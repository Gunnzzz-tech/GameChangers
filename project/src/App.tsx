import React, { useState, useEffect } from 'react';
import { 
  Car, AlertTriangle, Shield, Activity, 
  Calendar, Filter, BarChart3, Download,
  Clock, Camera, FileText, Search
} from 'lucide-react';

// Types
interface Violation {
  id: number;
  timestamp: string;
  violationType: 'Helmet' | 'Speed' | 'Ambulance' | 'Other';
  plateNumber: string;
  imagePath: string;
  speed: number | null;
}

// Mock data for demonstration
const mockViolations: Violation[] = [
  {
    id: 1,
    timestamp: '2025-06-15T08:23:45',
    violationType: 'Helmet',
    plateNumber: 'MH04AB1234',
    imagePath: 'https://images.pexels.com/photos/2519374/pexels-photo-2519374.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
    speed: null
  },
  {
    id: 2,
    timestamp: '2025-06-15T09:45:12',
    violationType: 'Speed',
    plateNumber: 'DL05CD5678',
    imagePath: 'https://images.pexels.com/photos/1213294/pexels-photo-1213294.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
    speed: 78
  },
  {
    id: 3,
    timestamp: '2025-06-15T10:12:33',
    violationType: 'Ambulance',
    plateNumber: 'KA01EF9012',
    imagePath: 'https://images.pexels.com/photos/1383834/pexels-photo-1383834.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
    speed: null
  },
  {
    id: 4,
    timestamp: '2025-06-15T11:05:22',
    violationType: 'Speed',
    plateNumber: 'TN02GH3456',
    imagePath: 'https://images.pexels.com/photos/1592384/pexels-photo-1592384.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
    speed: 92
  },
  {
    id: 5,
    timestamp: '2025-06-15T12:30:18',
    violationType: 'Helmet',
    plateNumber: 'UP03IJ7890',
    imagePath: 'https://images.pexels.com/photos/2393821/pexels-photo-2393821.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
    speed: null
  }
];

// Utility functions
const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const getViolationIcon = (type: string) => {
  switch (type) {
    case 'Helmet':
      return <Shield className="text-orange-500" />;
    case 'Speed':
      return <Activity className="text-red-500" />;
    case 'Ambulance':
      return <AlertTriangle className="text-purple-500" />;
    default:
      return <AlertTriangle className="text-gray-500" />;
  }
};

const getViolationColor = (type: string): string => {
  switch (type) {
    case 'Helmet':
      return 'bg-orange-100 text-orange-800';
    case 'Speed':
      return 'bg-red-100 text-red-800';
    case 'Ambulance':
      return 'bg-purple-100 text-purple-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

// Chart data preparation
const prepareChartData = (violations: Violation[]) => {
  const counts = {
    Helmet: 0,
    Speed: 0,
    Ambulance: 0,
    Other: 0
  };
  
  violations.forEach(v => {
    counts[v.violationType] += 1;
  });
  
  return counts;
};

function App() {
  const [violations, setViolations] = useState<Violation[]>(mockViolations);
  const [filteredViolations, setFilteredViolations] = useState<Violation[]>(mockViolations);
  const [filter, setFilter] = useState<string>('All');
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [showChart, setShowChart] = useState<boolean>(false);
  
  // Apply filters
  useEffect(() => {
    let result = violations;
    
    // Type filter
    if (filter !== 'All') {
      result = result.filter(v => v.violationType === filter);
    }
    
    // Search filter
    if (searchTerm) {
      result = result.filter(v => 
        v.plateNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
        v.violationType.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    setFilteredViolations(result);
  }, [violations, filter, searchTerm]);
  
  // In a real app, this would fetch from the API
  useEffect(() => {
    // Simulating API fetch
    const fetchViolations = async () => {
      try {
        // In a real app: const response = await fetch('/api/get_violations');
        // const data = await response.json();
        // setViolations(data);
        setViolations(mockViolations);
      } catch (error) {
        console.error('Error fetching violations:', error);
      }
    };
    
    fetchViolations();
  }, []);
  
  const chartData = prepareChartData(violations);
  
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-blue-600 text-white shadow-lg">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <Car size={28} />
            <h1 className="text-2xl font-bold">Smart Traffic AI</h1>
          </div>
          <div className="flex items-center space-x-4">
            <button className="bg-blue-700 hover:bg-blue-800 px-4 py-2 rounded-md flex items-center space-x-2">
              <Download size={18} />
              <span>Export Data</span>
            </button>
          </div>
        </div>
      </header>
      
      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-gray-500 text-sm">Total Violations</p>
                <h2 className="text-3xl font-bold">{violations.length}</h2>
              </div>
              <div className="bg-blue-100 p-3 rounded-full">
                <AlertTriangle className="text-blue-600" />
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-gray-500 text-sm">Helmet Violations</p>
                <h2 className="text-3xl font-bold">{violations.filter(v => v.violationType === 'Helmet').length}</h2>
              </div>
              <div className="bg-orange-100 p-3 rounded-full">
                <Shield className="text-orange-600" />
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-gray-500 text-sm">Speed Violations</p>
                <h2 className="text-3xl font-bold">{violations.filter(v => v.violationType === 'Speed').length}</h2>
              </div>
              <div className="bg-red-100 p-3 rounded-full">
                <Activity className="text-red-600" />
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-gray-500 text-sm">Ambulance Violations</p>
                <h2 className="text-3xl font-bold">{violations.filter(v => v.violationType === 'Ambulance').length}</h2>
              </div>
              <div className="bg-purple-100 p-3 rounded-full">
                <AlertTriangle className="text-purple-600" />
              </div>
            </div>
          </div>
        </div>
        
        {/* Filters and Controls */}
        <div className="bg-white rounded-lg shadow mb-8">
          <div className="p-6">
            <div className="flex flex-col md:flex-row justify-between items-center mb-6">
              <h2 className="text-xl font-bold mb-4 md:mb-0">Traffic Violations</h2>
              
              <div className="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4 w-full md:w-auto">
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Search size={18} className="text-gray-400" />
                  </div>
                  <input
                    type="text"
                    placeholder="Search plate number..."
                    className="pl-10 pr-4 py-2 border rounded-md w-full md:w-64"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
                
                <div className="flex space-x-2">
                  <button 
                    className={`px-4 py-2 rounded-md flex items-center space-x-2 ${filter === 'All' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100'}`}
                    onClick={() => setFilter('All')}
                  >
                    <Filter size={18} />
                    <span>All</span>
                  </button>
                  
                  <button 
                    className={`px-4 py-2 rounded-md flex items-center space-x-2 ${filter === 'Helmet' ? 'bg-orange-100 text-orange-800' : 'bg-gray-100'}`}
                    onClick={() => setFilter('Helmet')}
                  >
                    <Shield size={18} />
                    <span>Helmet</span>
                  </button>
                  
                  <button 
                    className={`px-4 py-2 rounded-md flex items-center space-x-2 ${filter === 'Speed' ? 'bg-red-100 text-red-800' : 'bg-gray-100'}`}
                    onClick={() => setFilter('Speed')}
                  >
                    <Activity size={18} />
                    <span>Speed</span>
                  </button>
                  
                  <button 
                    className={`px-4 py-2 rounded-md flex items-center space-x-2 ${filter === 'Ambulance' ? 'bg-purple-100 text-purple-800' : 'bg-gray-100'}`}
                    onClick={() => setFilter('Ambulance')}
                  >
                    <AlertTriangle size={18} />
                    <span>Ambulance</span>
                  </button>
                </div>
                
                <button 
                  className="px-4 py-2 bg-gray-100 rounded-md flex items-center space-x-2"
                  onClick={() => setShowChart(!showChart)}
                >
                  <BarChart3 size={18} />
                  <span>{showChart ? 'Hide Chart' : 'Show Chart'}</span>
                </button>
              </div>
            </div>
            
            {/* Chart View */}
            {showChart && (
              <div className="mb-8 p-4 bg-gray-50 rounded-lg">
                <h3 className="text-lg font-semibold mb-4">Violations by Type</h3>
                <div className="flex justify-around h-64">
                  {Object.entries(chartData).map(([type, count]) => (
                    <div key={type} className="flex flex-col items-center justify-end">
                      <div 
                        className={`w-16 ${getViolationColor(type).split(' ')[0]}`} 
                        style={{ height: `${(count / violations.length) * 200}px` }}
                      ></div>
                      <p className="mt-2 font-medium">{type}</p>
                      <p className="text-gray-500">{count}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
            
            {/* Table View */}
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Time
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Violation Type
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Plate Number
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Image
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Speed
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredViolations.length > 0 ? (
                    filteredViolations.map((violation) => (
                      <tr key={violation.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <Clock size={16} className="text-gray-400 mr-2" />
                            <span>{formatDate(violation.timestamp)}</span>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getViolationColor(violation.violationType)}`}>
                            {getViolationIcon(violation.violationType)}
                            <span className="ml-1">{violation.violationType}</span>
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap font-medium">
                          {violation.plateNumber}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="h-12 w-20 bg-gray-100 rounded overflow-hidden">
                            <img 
                              src={violation.imagePath} 
                              alt={`Violation ${violation.id}`} 
                              className="h-full w-full object-cover"
                            />
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          {violation.speed ? (
                            <span className="text-red-600 font-medium">{violation.speed} km/h</span>
                          ) : (
                            <span className="text-gray-400">N/A</span>
                          )}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                          <div className="flex space-x-2">
                            <button className="text-blue-600 hover:text-blue-800">
                              <Camera size={18} />
                            </button>
                            <button className="text-gray-600 hover:text-gray-800">
                              <FileText size={18} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={6} className="px-6 py-4 text-center text-gray-500">
                        No violations found matching your criteria
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
        
        {/* System Status */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">System Status</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="border rounded-lg p-4">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                <h3 className="font-medium">Helmet Detection</h3>
              </div>
              <p className="text-gray-500 text-sm mt-2">YOLOv8 model running</p>
            </div>
            
            <div className="border rounded-lg p-4">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                <h3 className="font-medium">Speed Detection</h3>
              </div>
              <p className="text-gray-500 text-sm mt-2">OpenCV tracking active</p>
            </div>
            
            <div className="border rounded-lg p-4">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                <h3 className="font-medium">Ambulance Detection</h3>
              </div>
              <p className="text-gray-500 text-sm mt-2">YOLOv8 model running</p>
            </div>
            
            <div className="border rounded-lg p-4">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                <h3 className="font-medium">Plate Reader</h3>
              </div>
              <p className="text-gray-500 text-sm mt-2">EasyOCR active</p>
            </div>
            
            <div className="border rounded-lg p-4">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                <h3 className="font-medium">Traffic Signal Control</h3>
              </div>
              <p className="text-gray-500 text-sm mt-2">Density-based algorithm active</p>
            </div>
            
            <div className="border rounded-lg p-4">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                <h3 className="font-medium">Violation Logger</h3>
              </div>
              <p className="text-gray-500 text-sm mt-2">API server running</p>
            </div>
          </div>
        </div>
      </main>
      
      {/* Footer */}
      <footer className="bg-gray-800 text-white py-6">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <Car size={20} />
              <span className="font-bold">Smart Traffic AI</span>
            </div>
            <div className="text-gray-400 text-sm">
              © 2025 Smart Traffic AI. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;