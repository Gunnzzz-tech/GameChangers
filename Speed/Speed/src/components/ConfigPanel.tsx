import React, { useState } from 'react';
import { Sliders, Send } from 'lucide-react';

interface ConfigPanelProps {
  speedLimit: number;
  onSpeedLimitChange: (limit: number) => void;
}

const ConfigPanel: React.FC<ConfigPanelProps> = ({ speedLimit, onSpeedLimitChange }) => {
  const [tempSpeedLimit, setTempSpeedLimit] = useState(speedLimit);
  const [alertThreshold, setAlertThreshold] = useState(5);
  const [isOcrEnabled, setIsOcrEnabled] = useState(true);
  const [autoAlert, setAutoAlert] = useState(true);
  
  const handleApply = () => {
    onSpeedLimitChange(tempSpeedLimit);
  };
  
  const handleLicensePlateDemo = () => {
    const demoContainer = document.getElementById('ocr-demo');
    if (demoContainer) {
      demoContainer.classList.add('scanning');
      setTimeout(() => {
        if (document.getElementById('plate-text')) {
          document.getElementById('plate-text')!.textContent = 'ABC-1234';
          document.getElementById('ocr-status')!.textContent = 'Recognized';
          document.getElementById('ocr-status')!.className = 'text-xs text-green-400';
        }
        
        setTimeout(() => {
          demoContainer.classList.remove('scanning');
        }, 1500);
      }, 1500);
    }
  };
  
  return (
    <div className="bg-gray-800 rounded-lg shadow-lg overflow-hidden">
      <div className="p-3 bg-gray-700 border-b border-gray-600 flex items-center">
        <Sliders className="h-4 w-4 mr-2" />
        <h2 className="font-semibold">System Configuration</h2>
      </div>
      
      <div className="p-4 space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">Speed Limit (km/h)</label>
          <div className="flex items-center">
            <input
              type="range"
              min="30"
              max="120"
              value={tempSpeedLimit}
              onChange={(e) => setTempSpeedLimit(parseInt(e.target.value))}
              className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
            />
            <span className="ml-2 w-10 text-center">{tempSpeedLimit}</span>
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">Alert Threshold (minutes)</label>
          <div className="flex items-center">
            <input
              type="range"
              min="1"
              max="10"
              value={alertThreshold}
              onChange={(e) => setAlertThreshold(parseInt(e.target.value))}
              className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
            />
            <span className="ml-2 w-10 text-center">{alertThreshold}</span>
          </div>
        </div>
        
        <div className="flex flex-col space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-sm font-medium text-gray-300">OCR License Plate Recognition</label>
            <div className="relative inline-block w-10 h-5 select-none">
              <input
                type="checkbox"
                checked={isOcrEnabled}
                onChange={() => setIsOcrEnabled(!isOcrEnabled)}
                className="sr-only"
              />
              <div 
                className={`block w-10 h-5 rounded-full ${isOcrEnabled ? 'bg-blue-600' : 'bg-gray-600'} transition`}
              ></div>
              <div 
                className={`absolute left-0.5 top-0.5 bg-white w-4 h-4 rounded-full transition-transform ${isOcrEnabled ? 'transform translate-x-5' : ''}`}
              ></div>
            </div>
          </div>
          
          <div className="flex items-center justify-between">
            <label className="text-sm font-medium text-gray-300">Automatic Alerts</label>
            <div className="relative inline-block w-10 h-5 select-none">
              <input
                type="checkbox"
                checked={autoAlert}
                onChange={() => setAutoAlert(!autoAlert)}
                className="sr-only"
              />
              <div 
                className={`block w-10 h-5 rounded-full ${autoAlert ? 'bg-blue-600' : 'bg-gray-600'} transition`}
              ></div>
              <div 
                className={`absolute left-0.5 top-0.5 bg-white w-4 h-4 rounded-full transition-transform ${autoAlert ? 'transform translate-x-5' : ''}`}
              ></div>
            </div>
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">License Plate OCR Demo</label>
          <div 
            id="ocr-demo"
            className="h-16 bg-gray-700 rounded p-2 flex items-center justify-center relative overflow-hidden"
          >
            <div className="bg-yellow-100 text-black px-4 py-2 rounded border-2 border-black font-mono">
              <span id="plate-text">??-????</span>
            </div>
          </div>
          <div className="flex items-center justify-between mt-1">
            <span id="ocr-status" className="text-xs text-gray-400">Waiting for scan</span>
            <button 
              onClick={handleLicensePlateDemo}
              className="text-xs bg-blue-600 hover:bg-blue-700 text-white px-2 py-1 rounded flex items-center"
            >
              <span>Scan Plate</span>
            </button>
          </div>
        </div>
        
        <div className="pt-2">
          <button
            onClick={handleApply}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded flex items-center justify-center transition"
          >
            <Send className="h-4 w-4 mr-2" />
            Apply Settings
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfigPanel;