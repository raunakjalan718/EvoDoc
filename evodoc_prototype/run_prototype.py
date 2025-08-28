import os
import subprocess
import sys
import time

def run_command(command, cwd=None):
    """Run a command and print output"""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        cwd=cwd
    )
    
    for line in process.stdout:
        print(line.decode().strip())
    
    process.wait()
    return process.returncode

def setup_environment():
    """Set up the environment"""
    print("Setting up environment...")
    
    # Create data directories
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("data/synthetic", exist_ok=True)
    os.makedirs("models/trained", exist_ok=True)
    os.makedirs("models/evaluation", exist_ok=True)
    
    print("Environment set up successfully!")

def setup_database():
    """Set up the database"""
    print("Setting up database...")
    
    # Create database
    run_command("python -m src.db.initialize")
    
    print("Database set up successfully!")

def generate_data():
    """Generate synthetic data"""
    print("Generating data...")
    
    # Generate synthetic data
    run_command("python -m src.data.synthetic")
    
    # Download and preprocess data
    run_command("python -m src.data.download")
    run_command("python -m src.data.preprocess")
    
    print("Data generated successfully!")

def train_models():
    """Train ML models"""
    print("Training models...")
    
    # Train models
    run_command("python -m src.ml.train")
    
    print("Models trained successfully!")

def start_api_server():
    """Start API server"""
    print("Starting API server...")
    
    # Start API server in a new process
    api_process = subprocess.Popen(
        [sys.executable, "-m", "src.api.run"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    
    # Wait a bit for the server to start
    time.sleep(2)
    
    return api_process

def start_frontend_server():
    """Start frontend server"""
    print("Starting frontend servers...")
    
    # In a real implementation, you would start the frontend servers here
    # For the prototype, we'll just provide instructions
    
    print("Patient portal: http://localhost:5000")
    print("Doctor portal: http://localhost:5001")
    
    print("""
    Frontend servers would be started here in a real implementation.
    For the prototype presentation, please use the API directly via:
    - Swagger UI: http://localhost:8000/docs
    - ReDoc: http://localhost:8000/redoc
    """)

def main():
    """Run the entire prototype setup"""
    setup_environment()
    setup_database()
    generate_data()
    train_models()
    api_process = start_api_server()
    start_frontend_server()
    
    print("Prototype is running! Press Ctrl+C to stop.")
    
    try:
        # Keep the main process running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping prototype...")
        api_process.terminate()
        print("Prototype stopped!")

if __name__ == "__main__":
    main()
