from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io
import base64
import os
from pathlib import Path

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
REPORTS_DIR = Path("reports")
GRAPHS_DIR = Path("graphs")
REPORTS_DIR.mkdir(exist_ok=True)
GRAPHS_DIR.mkdir(exist_ok=True)

# Mount static directories
app.mount("/reports", StaticFiles(directory="reports"), name="reports")
app.mount("/graphs", StaticFiles(directory="graphs"), name="graphs")

class Violation(BaseModel):
    timestamp: str
    violation_type: str
    plate_number: str
    image_path: str
    speed: Optional[float] = None

class Report(BaseModel):
    timestamp: str
    violations: Dict[str, Dict]
    summary: Dict[str, int]

# Store violations and reports
violations = []
reports = []

def generate_violation_graphs(report_data: Dict):
    """Generate graphs for the report"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Prepare data for plotting
    times = []
    helmet_counts = []
    speed_counts = []
    max_speeds = []
    
    # Sort violations by timestamp
    sorted_violations = []
    for plate, data in report_data['violations'].items():
        for helmet_time in data['helmet_violations']:
            # Parse string to datetime if needed
            if isinstance(helmet_time, str):
                helmet_time = datetime.fromisoformat(helmet_time)
            sorted_violations.append(('helmet', helmet_time))
        for speed_data in data['speed_violations']:
            speed_time = speed_data['timestamp']
            if isinstance(speed_time, str):
                speed_time = datetime.fromisoformat(speed_time)
            sorted_violations.append(('speed', speed_time, speed_data['speed']))
    
    sorted_violations.sort(key=lambda x: x[1])  # Sort by timestamp
    
    # Process sorted violations
    current_time = None
    helmet_count = 0
    speed_count = 0
    max_speed = 0
    
    for violation in sorted_violations:
        if violation[0] == 'helmet':
            time = violation[1]
            if current_time is None:
                current_time = time
            elif (time - current_time).total_seconds() > 60:  # New minute
                times.append(current_time.strftime('%H:%M:%S'))
                helmet_counts.append(helmet_count)
                speed_counts.append(speed_count)
                max_speeds.append(max_speed)
                current_time = time
                helmet_count = 1
                speed_count = 0
                max_speed = 0
            else:
                helmet_count += 1
        else:  # speed violation
            time = violation[1]
            speed = violation[2]
            if current_time is None:
                current_time = time
            elif (time - current_time).total_seconds() > 60:  # New minute
                times.append(current_time.strftime('%H:%M:%S'))
                helmet_counts.append(helmet_count)
                speed_counts.append(speed_count)
                max_speeds.append(max_speed)
                current_time = time
                helmet_count = 0
                speed_count = 1
                max_speed = speed
            else:
                speed_count += 1
                max_speed = max(max_speed, speed)
    
    # Add the last group if exists
    if current_time is not None:
        times.append(current_time.strftime('%H:%M:%S'))
        helmet_counts.append(helmet_count)
        speed_counts.append(speed_count)
        max_speeds.append(max_speed)
    
    # Plot helmet violations over time
    if times:
        ax1.plot(times, helmet_counts, 'ro-', label='Helmet Violations', marker='o')
        ax1.set_title('Helmet Violations Over Time')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Number of Violations')
        ax1.legend()
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        ax1.grid(True, linestyle='--', alpha=0.7)
        # Ensure at least one point is visible
        if len(times) == 1:
            ax1.set_xlim(times[0], times[0])
            ax1.set_ylim(0, max(1, helmet_counts[0]))
    else:
        ax1.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=16)
        ax1.set_title('Helmet Violations Over Time')
        ax1.axis('off')
    
    # Plot speed violations and max speeds over time
    if times:
        ax2.plot(times, speed_counts, 'bo-', label='Speed Violations', marker='o')
        ax2.plot(times, max_speeds, 'g--', label='Max Speed (km/h)', marker='s')
        ax2.set_title('Speed Violations and Max Speeds Over Time')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Number of Violations / Speed (km/h)')
        ax2.legend()
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        ax2.grid(True, linestyle='--', alpha=0.7)
        # Ensure at least one point is visible
        if len(times) == 1:
            ax2.set_xlim(times[0], times[0])
            ax2.set_ylim(0, max(1, speed_counts[0], max_speeds[0]))
    else:
        ax2.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=16)
        ax2.set_title('Speed Violations and Max Speeds Over Time')
        ax2.axis('off')
    
    # Adjust layout and save
    plt.tight_layout()
    graph_path = GRAPHS_DIR / f"violations_{timestamp}.png"
    plt.savefig(graph_path)
    plt.close()
    # Convert to POSIX path for web
    web_graph_path = str(graph_path).replace("\\", "/")
    return web_graph_path

@app.post("/log_violation")
async def log_violation(violation: Violation):
    violations.append(violation.dict())
    return {"status": "success"}

@app.post("/log_report")
async def log_report(report: Report):
    report_data = report.dict()
    reports.append(report_data)
    
    # Generate graphs
    graph_path = generate_violation_graphs(report_data)
    # Ensure forward slashes in the report JSON as well
    report_data['graph_path'] = graph_path.replace("\\", "/")
    
    # Save report to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = REPORTS_DIR / f"report_{timestamp}.json"
    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2, default=str)
    
    return {"status": "success", "graph_path": graph_path}

@app.get("/reports")
async def get_reports():
    return reports

@app.get("/violations")
async def get_violations():
    return violations

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Traffic Violation Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .violation-card { margin-bottom: 20px; }
            .graph-container { margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container mt-4">
            <h1>Traffic Violation Dashboard</h1>
            
            <div class="row mt-4">
                <div class="col-md-6">
                    <h2>Latest Report</h2>
                    <div id="latest-report"></div>
                </div>
                <div class="col-md-6">
                    <h2>Violation Graph</h2>
                    <div id="violation-graph" class="graph-container"></div>
                </div>
            </div>
            
            <div class="row mt-4">
                <div class="col-12">
                    <h2>Recent Violations</h2>
                    <div id="recent-violations"></div>
                </div>
            </div>
        </div>

        <script>
            function updateDashboard() {
                // Fetch latest report
                fetch('/reports')
                    .then(response => response.json())
                    .then(reports => {
                        if (reports.length > 0) {
                            const latestReport = reports[reports.length - 1];
                            const reportHtml = `
                                <div class="card">
                                    <div class="card-body">
                                        <h5 class="card-title">Report from ${new Date(latestReport.timestamp).toLocaleString()}</h5>
                                        <p>Total Violations: ${latestReport.summary.total_violations}</p>
                                        <p>Helmet Violations: ${latestReport.summary.helmet_violations}</p>
                                        <p>Speed Violations: ${latestReport.summary.speed_violations}</p>
                                    </div>
                                </div>
                            `;
                            document.getElementById('latest-report').innerHTML = reportHtml;
                            
                            // Display graph
                            if (latestReport.graph_path) {
                                document.getElementById('violation-graph').innerHTML = `
                                    <img src="${latestReport.graph_path}" class="img-fluid" alt="Violation Graph">
                                `;
                            }
                        }
                    });

                // Fetch recent violations
                fetch('/violations')
                    .then(response => response.json())
                    .then(violations => {
                        const recentViolations = violations.slice(-10).reverse();
                        const violationsHtml = recentViolations.map(v => `
                            <div class="card violation-card">
                                <div class="card-body">
                                    <h5 class="card-title">${v.violation_type} Violation</h5>
                                    <p>Plate: ${v.plate_number}</p>
                                    <p>Time: ${new Date(v.timestamp).toLocaleString()}</p>
                                    ${v.speed ? `<p>Speed: ${v.speed} km/h</p>` : ''}
                                    <img src="${v.image_path}" class="img-fluid" style="max-width: 200px;">
                                </div>
                            </div>
                        `).join('');
                        document.getElementById('recent-violations').innerHTML = violationsHtml;
                    });
            }

            // Update dashboard every 5 seconds
            updateDashboard();
            setInterval(updateDashboard, 5000);
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000) 