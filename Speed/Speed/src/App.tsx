import React from 'react';
import { Gauge, Car, Bell, Settings } from 'lucide-react';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  return (
    <div className="flex flex-col min-h-screen bg-gray-900 text-white">
      <header className="bg-gray-800 p-4 border-b border-gray-700">
        <div className="container mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Car className="h-8 w-8 text-blue-500" />
            <h1 className="text-xl md:text-2xl font-bold">SpeedGuard Pro</h1>
          </div>
          <div className="flex items-center space-x-4">
            <button className="p-2 rounded-full hover:bg-gray-700 transition">
              <Bell className="h-5 w-5 text-gray-300" />
            </button>
            <button className="p-2 rounded-full hover:bg-gray-700 transition">
              <Settings className="h-5 w-5 text-gray-300" />
            </button>
          </div>
        </div>
      </header>
      
      <main className="flex-grow">
        <Dashboard />
      </main>
      
      <footer className="bg-gray-800 p-3 text-center text-sm text-gray-500">
        <div className="container mx-auto">
          <p>© 2025 SpeedGuard Pro - Real-Time Vehicle Speed Monitoring System</p>
        </div>
      </footer>
    </div>
  );
}

export default App;