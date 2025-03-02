import re
import logging
import time
from typing import Dict, Any, List, Optional, Callable, TypeVar, Union
import traceback
import functools

# Configure logging
logger = logging.getLogger(__name__)

# Type variable for generic functions
T = TypeVar('T')

def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0, 
          exceptions: tuple = (Exception,)) -> Callable:
    """
    Retry decorator with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries (in seconds)
        backoff: Backoff multiplier
        exceptions: Tuple of exceptions to catch and retry
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            mtries, mdelay = max_attempts, delay
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.warning(f"Retrying {func.__name__} due to {e}, "
                                  f"{mtries-1} attempts left")
                    mtries -= 1
                    time.sleep(mdelay)
                    mdelay *= backoff
            return func(*args, **kwargs)
        return wrapper
    return decorator

def sanitize_code(code: str, language: str) -> str:
    """
    Sanitize code by removing Markdown code blocks if present.
    
    Args:
        code: Code string potentially with Markdown formatting
        language: Programming language
        
    Returns:
        Sanitized code
    """
    # Check if the code is wrapped in markdown code blocks
    if "```" in code:
        code_blocks = code.split("```")
        for i, block in enumerate(code_blocks):
            if i % 2 == 1:  # Odd-indexed blocks are code
                # Remove language identifier if present
                lines = block.split("\n")
                if lines and lines[0].strip().lower() == language.lower():
                    return "\n".join(lines[1:])
                return block.strip()
        
        # If no code block was found, return the original code
        return code.strip()
    
    return code.strip()

def extract_code_from_response(response: str, language: str) -> str:
    """
    Extract code from an AI response.
    
    Args:
        response: AI response potentially containing code
        language: Programming language to look for
        
    Returns:
        Extracted code
    """
    # Pattern to match markdown code blocks
    pattern = r"```(?:" + language + r")?\s*([\s\S]*?)```"
    matches = re.findall(pattern, response, re.IGNORECASE)
    
    if matches:
        # Return the first code block that matches
        return matches[0].strip()
    
    # If no code block found, return the original response
    return response.strip()

def measure_execution_time(func: Callable) -> Callable:
    """
    Decorator to measure and log function execution time.
    
    Args:
        func: Function to measure
        
    Returns:
        Decorated function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Function {func.__name__} executed in {execution_time:.4f} seconds")
        return result
    return wrapper

def safe_execute(func: Callable[..., T]) -> Callable[..., Union[T, None]]:
    """
    Decorator to safely execute a function and handle exceptions.
    
    Args:
        func: Function to execute safely
        
    Returns:
        Decorated function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in function {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            return None
    return wrapper


    