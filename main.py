import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from pathlib import Path

from agentlab.agents.generic_agent import USER_BEHAVIOR_AGENT, AGENT_4o_VISION
from browsergym.experiments.loop import EnvArgs, ExpArgs
import boto3
import os
from agentlab.experiments.exp_utils import RESULTS_DIR
from agentlab.agents import dynamic_prompting as dp
from agentlab.agents.generic_agent.generic_agent_prompt import GenericPromptFlags
import shutil
import bgym
from agentlab.ui_assistant import make_exp_args


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
        "height": 720
    },
    "tablet": {
        "width": 800,
        "height": 720
    },
    "mobile": {
        "width": 380,
        "height": 720
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
                wait_for_user_message=True,
                viewport=deviceViewports.get(task.device, deviceViewports["desktop"]),
                slow_mo=10,
            ),
        )
        

        # use AGENT_4o_VISION instead with make_exp_args


#         exp_args = ExpArgs(
#             agent_args=AGENT_4o_VISION,
#             env_args=EnvArgs(
#                 max_steps=1000,
#                 task_seed=None,
#                 task_name="openended", 
#                 task_kwargs={
#                     "start_url": task.url,
#                 },
#                 headless=False,
#                 record_video=True,  # Enable recording
#             ),
#         )
        
#         # Set goal (not instruction) in task kwargs 
#         exp_args.env_args.task_kwargs["goal"] = f"""{task.instruction}

# Act like a real user browsing this website:
# - Take time to read content
# - Move mouse naturally between actions
# - Hover over items of interest
# - Type at human speed with occasional typos
# - React to visual feedback
# - Scroll naturally through content
# Once you finished following the instructions, you may finish.
# """
        
        # Prepare experiment
        exp_args.prepare(results_dir / "tasks")

        # set goal
        exp_args.env_args.task_kwargs["goal"] = f"""{task.instruction}

Act like a real user browsing this website and once the instructions are followed (no need to do extra browsing), you may finish."""
        
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

run_task(TaskRequest(instruction="Find problems in the navigation bar", url="https://couch.com", device="desktop"))