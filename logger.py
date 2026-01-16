"""
Logging and Error Recovery System for Modern_USA_News
Provides centralized logging with file output and recovery mechanisms
"""

import os
import sys
import logging
import traceback
from datetime import datetime
from typing import Optional, Callable, Any
from functools import wraps

# Log directory
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Log file names
LOG_FILE = os.path.join(LOG_DIR, f"automation_{datetime.now().strftime('%Y-%m-%d')}.log")
ERROR_LOG = os.path.join(LOG_DIR, f"errors_{datetime.now().strftime('%Y-%m-%d')}.log")
RECOVERY_LOG = os.path.join(LOG_DIR, "recovery.log")


class NewsLogger:
    """
    Centralized logging for the automation system
    Features:
    - Console + File output
    - Error tracking
    - Daily log rotation
    - Structured logging
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._setup_loggers()
        self.run_start = datetime.now()
        self.errors = []
        self.warnings = []
        self.stats = {
            'rss_fetched': 0,
            'articles_added': 0,
            'posts_generated': 0,
            'images_created': 0,
            'errors': 0,
            'recovered': 0
        }
    
    def _setup_loggers(self):
        """Setup logging handlers"""
        
        # Main logger
        self.logger = logging.getLogger('ModernUSANews')
        self.logger.setLevel(logging.DEBUG)
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Console handler (INFO level)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(message)s'
        )
        console_handler.setFormatter(console_format)
        
        # File handler (DEBUG level)
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(module)-15s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        
        # Error file handler
        error_handler = logging.FileHandler(ERROR_LOG, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_format = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(module)s | %(message)s\n%(exc_info)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        error_handler.setFormatter(error_format)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
    
    def info(self, message: str, module: str = None):
        """Log info message"""
        if module:
            message = f"[{module}] {message}"
        self.logger.info(message)
    
    def debug(self, message: str, module: str = None):
        """Log debug message (file only)"""
        if module:
            message = f"[{module}] {message}"
        self.logger.debug(message)
    
    def warning(self, message: str, module: str = None):
        """Log warning message"""
        if module:
            message = f"[{module}] {message}"
        self.logger.warning(f"⚠️  {message}")
        self.warnings.append({
            'time': datetime.now().isoformat(),
            'message': message,
            'module': module
        })
    
    def error(self, message: str, exc: Exception = None, module: str = None):
        """Log error message with optional exception"""
        if module:
            message = f"[{module}] {message}"
        
        if exc:
            full_message = f"{message}: {str(exc)}"
            self.logger.error(f"❌ {full_message}", exc_info=exc)
        else:
            self.logger.error(f"❌ {message}")
        
        self.errors.append({
            'time': datetime.now().isoformat(),
            'message': message,
            'exception': str(exc) if exc else None,
            'module': module,
            'traceback': traceback.format_exc() if exc else None
        })
        self.stats['errors'] += 1
    
    def success(self, message: str, module: str = None):
        """Log success message"""
        if module:
            message = f"[{module}] {message}"
        self.logger.info(f"✅ {message}")
    
    def section(self, title: str):
        """Log section header"""
        separator = "=" * 60
        self.logger.info(f"\n{separator}")
        self.logger.info(f"  {title}")
        self.logger.info(f"{separator}")
    
    def step(self, step_num: int, description: str):
        """Log a numbered step"""
        self.logger.info(f"\n📌 STEP {step_num}: {description}")
    
    def update_stat(self, stat_name: str, value: int = 1):
        """Update a statistic counter"""
        if stat_name in self.stats:
            self.stats[stat_name] += value
    
    def get_run_summary(self) -> dict:
        """Get summary of current run"""
        run_duration = (datetime.now() - self.run_start).total_seconds()
        
        return {
            'start_time': self.run_start.isoformat(),
            'duration_seconds': run_duration,
            'duration_human': f"{int(run_duration // 60)}m {int(run_duration % 60)}s",
            'stats': self.stats.copy(),
            'error_count': len(self.errors),
            'warning_count': len(self.warnings),
            'status': 'completed_with_errors' if self.errors else 'completed_successfully'
        }
    
    def print_summary(self):
        """Print run summary to console and log"""
        summary = self.get_run_summary()
        
        self.section("RUN SUMMARY")
        self.info(f"  Duration: {summary['duration_human']}")
        self.info(f"  Articles collected: {self.stats['articles_added']}")
        self.info(f"  Posts generated: {self.stats['posts_generated']}")
        self.info(f"  Images created: {self.stats['images_created']}")
        self.info(f"  Errors: {len(self.errors)}")
        self.info(f"  Warnings: {len(self.warnings)}")
        self.info(f"  Status: {summary['status']}")
        
        if self.errors:
            self.logger.info("\n  Recent Errors:")
            for err in self.errors[-3:]:  # Last 3 errors
                self.logger.info(f"    - {err['message']}")
    
    def save_recovery_state(self, state: dict):
        """Save recovery state for crash recovery"""
        try:
            import json
            with open(RECOVERY_LOG, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'state': state

                }, f, indent=2)
        except Exception as e:
            self.warning(f"Could not save recovery state: {e}")
    
    def load_recovery_state(self) -> Optional[dict]:
        """Load recovery state if available"""
        try:
            import json
            if os.path.exists(RECOVERY_LOG):
                with open(RECOVERY_LOG, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data.get('state')
        except Exception as e:
            self.warning(f"Could not load recovery state: {e}")
        return None
    
    def clear_recovery_state(self):
        """Clear recovery state after successful completion"""
        try:
            if os.path.exists(RECOVERY_LOG):
                os.remove(RECOVERY_LOG)
        except:
            pass


def safe_execute(fallback_value: Any = None, log_error: bool = True):
    """
    Decorator for safe execution with error recovery
    
    Usage:
        @safe_execute(fallback_value=[])
        def risky_function():
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = NewsLogger()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_error:
                    logger.error(
                        f"Error in {func.__name__}", 
                        exc=e, 
                        module=func.__module__
                    )
                logger.stats['recovered'] += 1
                return fallback_value
        return wrapper
    return decorator


def retry_on_failure(max_attempts: int = 3, delay_seconds: float = 1.0):
    """
    Decorator for automatic retry with exponential backoff
    
    Usage:
        @retry_on_failure(max_attempts=3)
        def flaky_api_call():
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            logger = NewsLogger()
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts:
                        wait_time = delay_seconds * (2 ** (attempt - 1))
                        logger.debug(
                            f"Attempt {attempt} failed for {func.__name__}, "
                            f"retrying in {wait_time}s..."
                        )
                        time.sleep(wait_time)
            
            logger.error(
                f"All {max_attempts} attempts failed for {func.__name__}",
                exc=last_exception
            )
            raise last_exception
        return wrapper
    return decorator


# Global logger instance
def get_logger() -> NewsLogger:
    """Get the global logger instance"""
    return NewsLogger()


if __name__ == "__main__":
    # Test logging
    logger = get_logger()
    
    logger.section("TESTING LOGGING SYSTEM")
    logger.info("This is an info message")
    logger.debug("This is a debug message (file only)")
    logger.warning("This is a warning")
    logger.success("This is a success message")
    
    # Test step logging
    logger.step(1, "Collecting RSS feeds")
    logger.info("   Fetching from CNN...")
    logger.update_stat('rss_fetched', 5)
    
    logger.step(2, "Generating content")
    logger.info("   Processing articles...")
    logger.update_stat('posts_generated', 5)
    
    # Test error logging
    try:
        raise ValueError("Test error")
    except Exception as e:
        logger.error("Something went wrong", exc=e, module="test")
    
    # Test summary
    logger.print_summary()
    
    print(f"\n📁 Log files saved to: {LOG_DIR}")
