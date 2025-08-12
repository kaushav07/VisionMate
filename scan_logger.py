import datetime
import os
from typing import List, Dict, Any, Optional

# In-memory storage for scan history
scan_history: List[Dict[str, Any]] = []

# Log file configuration
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "scan_history.log")

# Create logs directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

def log_scan(caption: str, user_command: str) -> None:
    """
    Log a scan entry with timestamp, caption, and user command.
    
    Args:
        caption (str): Description of the scanned content
        user_command (str): The command that triggered the scan
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = {
        "timestamp": timestamp,
        "caption": caption,
        "user_command": user_command
    }
    
    # Add to in-memory history
    scan_history.append(entry)
    
    # Log to file
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} | {caption} | {user_command}\n")
    except Exception as e:
        print(f"⚠️ Failed to write to log file: {e}")

def log_error(error_msg: str, context: Optional[Dict] = None) -> None:
    """
    Log an error message with optional context.
    
    Args:
        error_msg (str): Error message to log
        context (Dict, optional): Additional context about the error
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    context_str = f" | {context}" if context else ""
    log_entry = f"[ERROR] {timestamp} | {error_msg}{context_str}\n"
    
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"⚠️ Failed to write error to log file: {e}")

def show_history(limit: int = 10) -> None:
    """
    Display recent scan history.
    
    Args:
        limit (int): Maximum number of entries to show (default: 10)
    """
    if not scan_history:
        print("\n📭 No scan history available.")
        return

    print(f"\n📜 Last {min(limit, len(scan_history))} Scans:")
    for i, entry in enumerate(scan_history[-limit:], start=1):
        print(f"\n🔹 Entry {i}")
        print(f"   🕒 Time: {entry['timestamp']}")
        print(f"   🖼️ Caption: {entry['caption']}")
        print(f"   💬 User Command: {entry['user_command']}")

def get_recent_scans(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get recent scan entries.
    
    Args:
        limit (int): Maximum number of entries to return (default: 5)
        
    Returns:
        List[Dict[str, Any]]: List of recent scan entries
    """
    return scan_history[-limit:]

# Example usage
if __name__ == "__main__":
    # Test logging
    log_scan("A man passing the main road", "Alert User")
    log_scan("A family roaming in a busy market", "Describe the surroundings")
    log_error("Failed to process image", {"error": "Network timeout", "retry_count": 3})
    
    # Display history
    show_history()
