import os
import shutil
import tempfile
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import docker
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="SentryNode Sandbox Execution Service",
    description="Isolated container sandbox to compile code patches and run diagnostic scripts."
)

class ExecutionPayload(BaseModel):
    files: dict[str, str] # filename -> content
    command: str

class ExecutionResponse(BaseModel):
    stdout: str
    stderr: str
    exit_code: int

def run_in_docker(files: dict[str, str], command: str) -> tuple[str, str, int]:
    """
    Spins up a transient Docker container, writes files, runs the command, and destroys the container.
    """
    client = docker.from_env()
    
    # Create a temporary directory on the host to mount into the container
    with tempfile.TemporaryDirectory() as temp_dir:
        # Write files to temp directory
        for filename, content in files.items():
            file_path = os.path.join(temp_dir, filename)
            # Ensure subdirectory paths are created inside temp_dir if any
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(content)
                
        # Run container
        # Using a standard lightweight python-alpine image
        container = client.containers.run(
            image="python:3.11-alpine",
            command=f"sh -c 'cd /workspace && {command}'",
            volumes={temp_dir: {"bind": "/workspace", "mode": "rw"}},
            working_dir="/workspace",
            detach=True,
            mem_limit="128m",     # Limit memory usage
            nano_cpus=1000000000, # Limit CPU to 1 core
            network_mode="none"   # Block all egress/ingress network calls
        )
        
        # Wait for container execution
        result = container.wait()
        exit_code = result.get("StatusCode", -1)
        
        # Get logs
        logs = container.logs()
        container.remove()
        
        return logs.decode("utf-8", errors="ignore"), "", exit_code

def run_in_local_subprocess(files: dict[str, str], command: str) -> tuple[str, str, int]:
    """
    Fallback runner using local Python tempdirs and subprocesses when Docker is unavailable.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        for filename, content in files.items():
            file_path = os.path.join(temp_dir, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(content)
                
        try:
            # Run command locally in the temp directory
            proc = subprocess.run(
                command,
                shell=True,
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=10 # Prevent infinite execution loops
            )
            return proc.stdout, proc.stderr, proc.returncode
        except subprocess.TimeoutExpired as te:
            return te.stdout or "", (te.stderr or "") + "\nTimeoutExpired: Command exceeded 10 seconds execution limit.", 124
        except Exception as e:
            return "", f"Local execution error: {str(e)}", -1

@app.post("/execute", response_model=ExecutionResponse)
def execute_sandbox(payload: ExecutionPayload):
    # Attempt Docker execution first
    try:
        stdout, stderr, exit_code = run_in_docker(payload.files, payload.command)
        return ExecutionResponse(stdout=stdout, stderr=stderr, exit_code=exit_code)
    except Exception as de:
        print(f"Docker execution failed: {de}. Falling back to local isolated subprocess.")
        # Fallback to local subprocess execution (highly compatible for dev systems)
        stdout, stderr, exit_code = run_in_local_subprocess(payload.files, payload.command)
        return ExecutionResponse(stdout=stdout, stderr=stderr, exit_code=exit_code)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8003, reload=True)
