"""
Advanced logging utility with multiple output levels and formatting.
Supports both console and file logging.
"""

import sys
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime


class Logger:
    """
    Configurable logger with color-coded console output and file logging support.
    Supports both instance methods (modern) and static methods (legacy).
    
    Instance API (Modern - Recommended):
        logger = Logger(__name__)
        logger.info("Processing started")
        logger.success("Task completed")
        logger.warning("Check this")
        logger.error("Something failed")
        logger.debug("Detailed info")
        logger.section("My Section")
    
    Static API (Legacy - For Backwards Compatibility):
        Logger.print_section("My Section")
        Logger.print_info("Some info")
        Logger.print_success("Task done!")
        Logger.print_error("An error occurred")
        Logger.print_warning("Warning message")
    """
    
    # Color codes for terminal output
    COLORS = {
        'reset': '\033[0m',
        'bold': '\033[1m',
        'gray': '\033[90m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'blue': '\033[94m',
        'cyan': '\033[96m',
    }
    
    SYMBOLS = {
        'info': 'ℹ️ ',
        'success': '✅',
        'warning': '⚠️ ',
        'error': '❌',
        'debug': '🔧',
        'section': '═',
    }
    
    def __init__(self, name: str = 'FDA-FIS', log_file: Optional[str] = None):
        """
        Initialize logger.
        
        Args:
            name: Module/script name for logging
            log_file: Optional path to log file for persistence
        """
        self.name = name
        self.log_file = log_file
        self._setup_file_logging()
    
    def _setup_file_logging(self):
        """Configure file logging if path provided."""
        if self.log_file:
            log_path = Path(self.log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            self.file_handle = open(log_path, 'a', encoding='utf-8')
        else:
            self.file_handle = None
    
    def _write_to_file(self, message: str, level: str):
        """Write message to log file if configured."""
        if self.file_handle:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_line = f"[{timestamp}] [{level:8s}] {message}\n"
            self.file_handle.write(log_line)
            self.file_handle.flush()
    
    def _format_message(self, message: str, level: str, symbol: str, color: str) -> str:
        """Format console message with color and symbol."""
        if sys.stdout.isatty():  # Check if terminal supports colors
            colored_symbol = f"{self.COLORS[color]}{self.COLORS['bold']}{symbol}{self.COLORS['reset']}"
            return f"{colored_symbol} {message}"
        else:  # Plain text for non-terminal output
            return f"{symbol} {message}"
    
    def _log(self, message: str, level: str, symbol: str, color: str):
        """Internal logging method."""
        formatted_msg = self._format_message(message, level, symbol, color)
        print(formatted_msg)
        self._write_to_file(message, level)
    
    # Public logging methods
    
    def info(self, message: str):
        """Log info message (blue)."""
        self._log(message, 'INFO', self.SYMBOLS['info'], 'blue')
    
    def success(self, message: str):
        """Log success message (green)."""
        self._log(message, 'SUCCESS', self.SYMBOLS['success'], 'green')
    
    def warning(self, message: str):
        """Log warning message (yellow)."""
        self._log(message, 'WARNING', self.SYMBOLS['warning'], 'yellow')
    
    def error(self, message: str):
        """Log error message (red)."""
        self._log(message, 'ERROR', self.SYMBOLS['error'], 'red')
    
    def debug(self, message: str):
        """Log debug message (gray)."""
        self._log(message, 'DEBUG', self.SYMBOLS['debug'], 'gray')
    
    def section(self, title: str, width: int = 80, char: str = "="):
        """
        Print formatted section header.
        
        Args:
            title: Section title
            width: Total width of the line
            char: Character to repeat
        """
        line = char * width
        self.info(line)
        self.info(f"  {title}")
        self.info(line)
    
    def subsection(self, title: str, width: int = 60, char: str = "-"):
        """Print formatted subsection header."""
        self.info(f"\n{char * width}")
        self.info(f"  {title}")
        self.info(f"{char * width}\n")
    
    def table_row(self, *values, widths: Optional[list] = None, separator: str = " | "):
        """
        Print a formatted table row.
        
        Args:
            values: Values to print in row
            widths: Optional column widths
            separator: Column separator
        """
        if widths:
            formatted_row = separator.join(
                str(val).ljust(width) for val, width in zip(values, widths)
            )
        else:
            formatted_row = separator.join(str(val) for val in values)
        
        self.info(formatted_row)
    
    # ========== STATIC METHODS (Legacy API for backwards compatibility) ==========
    
    @staticmethod
    def print_section(title: str, char: str = "="):
        """Print a formatted section header (static method for legacy code)."""
        width = 60
        line = char * width
        print(f"\n{line}")
        print(f"  {title}")
        print(f"{line}\n")
    
    @staticmethod
    def print_success(message: str):
        """Print success message (static method for legacy code)."""
        print(f"✓ {message}")
    
    @staticmethod
    def print_error(message: str):
        """Print error message (static method for legacy code)."""
        print(f"✗ {message}")
    
    @staticmethod
    def print_info(message: str):
        """Print info message (static method for legacy code)."""
        print(f"ℹ {message}")
    
    @staticmethod
    def print_warning(message: str):
        """Print warning message (static method for legacy code)."""
        print(f"⚠️  {message}")
    
    def close(self):
        """Close file handle if open."""
        if self.file_handle:
            self.file_handle.close()
    
    def __del__(self):
        """Cleanup on deletion."""
        self.close()
