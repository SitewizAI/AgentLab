import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from pathlib import Path

from agentlab.agents.generic_agent import USER_BEHAVIOR_AGENT
from browsergym.experiments.loop import EnvArgs, ExpArgs
import boto3
import os
from agentlab.experiments.exp_utils import RESULTS_DIR
from agentlab.agents import dynamic_prompting as dp
from agentlab.agents.generic_agent.generic_agent_prompt import GenericPromptFlags
import shutil
import bgym



# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Web Agent API", version="1.0.0")

deviceViewports = {
    "desktop": {
        "width": 1280,
        "height": 1280
    },
    "tablet": {
        "width": 800,
        "height": 1280
    },
    "mobile": {
        "width": 380,
        "height": 1280
    }
}

class TaskRequest(BaseModel):
    instruction: str
    url: str = "https://www.google.com"
    device: Optional[str] = "desktop"
    agent_name: Optional[str] = "AGENT_4o_MINI"
    benchmark: Optional[str] = "miniwob_tiny_test" 
    n_jobs: Optional[int] = 4

# Store study states
studies = {}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

def upload_to_s3(video_path: Path, experiment_id: str):
    """Upload video file to S3"""
    s3 = boto3.client('s3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    
    bucket = os.getenv('AWS_BUCKET_NAME')
    s3_path = f"videos/{experiment_id}.webm"
    
    s3.upload_file(str(video_path), bucket, s3_path)
    return f"s3://{bucket}/{s3_path}"

def cleanup_exp_dir(exp_dir: Path):
    """Clean up experiment directory after task completion"""
    try:
        if exp_dir is not None and exp_dir.exists():
            shutil.rmtree(exp_dir)
            logger.info(f"Cleaned up experiment directory: {exp_dir}")
    except Exception as e:
        logger.error(f"Failed to clean up directory {exp_dir}: {e}")

@app.post("/run_task") 
def run_task(task: TaskRequest):
    exp_dir = None
    try:
        logger.info(f"Running task: {task}")

        results_dir = Path(os.getenv('AGENTLAB_EXP_ROOT', Path.home() / 'agentlab_results'))
        results_dir.mkdir(parents=True, exist_ok=True)

    
        # Create experiment args
        exp_args = ExpArgs(
            agent_args=USER_BEHAVIOR_AGENT,
            env_args=EnvArgs(
                max_steps=1000,
                task_seed=None,
                task_name="openended", 
                task_kwargs={
                    "start_url": task.url,
                    "goal": task.instruction
                },
                headless=False,
                record_video=True,
                wait_for_user_message=False,
                viewport=deviceViewports.get(task.device, deviceViewports["desktop"]),
                slow_mo=10,
            ),
        )
        
        # Prepare and run experiment
        exp_args.prepare(results_dir / "tasks")
        result = exp_args.run()
        if result is None:
            raise ValueError("Task execution failed")
        else:
            logger.info("results")
            logger.info(result)

        # Get video path from results directory
        exp_dir = results_dir / "tasks" / exp_args.exp_name
        video_path = next(exp_dir.glob("*.webm"))
        
        # Upload to S3
        s3_url = upload_to_s3(video_path, exp_args.exp_id)

        # Read logs
        log_file = exp_dir / "experiment.log"
        with open(log_file, 'r') as f:
            logs = f.readlines()

        return {
            "status": "success", 
            "result": result,
            "video_url": s3_url,
            "logs_dir": str(exp_dir),
            "logs": logs
        }
        
    except Exception as e:
        logger.error(f"Error running task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cleanup_exp_dir(exp_dir)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)