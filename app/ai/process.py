import requests
import logging
import traceback
import time
import os
from sqlalchemy.orm import Session
from app.crud import submission as crud_submission
from app.models.submission_model import Submission, ReviewResults
from app.schemas.submission_schema import ReviewResultCreate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ollama configuration
OLLAMA_HOST = os.environ.get('OLLAMA_HOST', 'ollama')
OLLAMA_PORT = os.environ.get('OLLAMA_PORT', '11434')
OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'tinyllama')
OLLAMA_TIMEOUT = int(os.environ.get('OLLAMA_TIMEOUT', '60'))

def check_ollama_service():
    """Check if Ollama service is available"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/version", timeout=5)
        if response.status_code == 200:
            logger.info(f"Ollama service is available: {response.json().get('version')}")
            return True
        else:
            logger.warning(f"Ollama service returned unexpected status: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error connecting to Ollama service: {str(e)}")
        return False

def check_model_availability(model_name):
    """Check if a model is available in Ollama"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if response.status_code != 200:
            logger.warning(f"Failed to list models: {response.status_code}")
            return False
            
        models = response.json().get('models', [])
        for model in models:
            if model.get('name') == model_name:
                logger.info(f"Model '{model_name}' is available")
                return True
                
        logger.warning(f"Model '{model_name}' is not available")
        return False
    except Exception as e:
        logger.error(f"Error checking model availability: {str(e)}")
        return False

def pull_model(model_name):
    """Pull a model from Ollama"""
    try:
        logger.info(f"Pulling model '{model_name}'...")
        response = requests.post(
            f"{OLLAMA_URL}/api/pull",
            json={"name": model_name},
            timeout=300  # 5 minutes timeout for model pulling
        )
        
        if response.status_code == 200:
            logger.info(f"Successfully pulled model '{model_name}'")
            return True
        else:
            logger.error(f"Failed to pull model '{model_name}': {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error pulling model: {str(e)}")
        return False

async def process_submission(submission_id: int, file_path: str, db: Session):
    # Update submission status to processing
    crud_submission.update_submission_status(db, submission_id, "PROCESSING")
    logger.info(f"Processing submission_id: {submission_id}, file: {file_path}")
    
    try:
        # Read the file content
        with open(file_path, 'r') as file:
            code_content = file.read()
        
        # Get the language from the submission
        submission = crud_submission.get_submission(db, submission_id)
        language = submission.language.lower()
        logger.info(f"Submission language: {language}")
        
        # Generate prompt for analysis
        prompt = f"Analyze this {language} code for quality, security, and performance issues:\n\n```{language}\n{code_content}\n```"
        
        try:
            # Check if Ollama service is available
            if not check_ollama_service():
                logger.error("Ollama service is not available")
                raise Exception("Ollama service is not available. Please check the service is running.")
                
            # Check if model exists and pull if needed
            model_name = OLLAMA_MODEL
            if not check_model_availability(model_name):
                logger.warning(f"Model '{model_name}' not found, attempting to pull it")
                if not pull_model(model_name):
                    raise Exception(f"Model '{model_name}' is not available and could not be pulled")
                    
                # Wait a moment for the model to be ready
                time.sleep(2)
            
            # Try to use Ollama for analysis
            logger.info(f"Sending code to Ollama for analysis with model: {model_name}")
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={"model": model_name, "prompt": prompt, "stream": False},
                timeout=OLLAMA_TIMEOUT
            )
            
            if response.status_code == 200:
                feedback = response.json().get("response", "Analysis failed")
                logger.info(f"Successfully analyzed code for submission_id: {submission_id}")
            else:
                error_msg = f"Could not analyze due to API error: {response.status_code}"
                if response.status_code == 404:
                    error_msg += f". Model '{model_name}' not found."
                logger.error(error_msg)
                feedback = error_msg
                
        except Exception as e:
            error_msg = f"Analysis could not be performed: {str(e)}"
            logger.error(f"Error during code analysis: {error_msg}")
            logger.debug(traceback.format_exc())
            feedback = error_msg
        
        # Save as a single result
        result = ReviewResultCreate(
            agent_type="Code Analysis",
            feedback=feedback,
            score=75 if "API error" not in feedback else 0
        )
        
        # Save to database
        crud_submission.create_review_result(db, result, submission_id)
        
        # Update submission status to completed
        crud_submission.update_submission_status(db, submission_id, "COMPLETED")
        logger.info(f"Completed processing submission_id: {submission_id}")
        
    except Exception as e:
        # Log the full stack trace for debugging
        logger.error(f"Error processing submission_id {submission_id}: {str(e)}")
        logger.debug(traceback.format_exc())
        
        # Record any error that occurred
        error_result = ReviewResultCreate(
            agent_type="System",
            feedback=f"Error during processing: {str(e)}",
            score=0
        )
        crud_submission.create_review_result(db, error_result, submission_id)
        
        # Update submission status to failed
        crud_submission.update_submission_status(db, submission_id, "FAILED")
        logger.info(f"Marked submission_id: {submission_id} as FAILED")