"""
Utility functions for the application
"""
import os
import json
from datetime import datetime
from pathlib import Path


def ensure_dir_exists(directory):
    """Ensure directory exists, create if not"""
    Path(directory).mkdir(parents=True, exist_ok=True)


def format_file_size(bytes_size):
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"


def format_duration(seconds):
    """Format duration in HH:MM:SS"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def sanitize_filename(filename):
    """Sanitize filename to remove invalid characters"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def load_json_file(filepath):
    """Load JSON file safely"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_json_file(filepath, data):
    """Save data to JSON file"""
    ensure_dir_exists(os.path.dirname(filepath))
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def get_file_metadata(filepath):
    """Get file metadata"""
    if not os.path.exists(filepath):
        return None
    
    stat = os.stat(filepath)
    return {
        'size': stat.st_size,
        'size_formatted': format_file_size(stat.st_size),
        'created': datetime.fromtimestamp(stat.st_ctime),
        'modified': datetime.fromtimestamp(stat.st_mtime)
    }


def truncate_text(text, max_length=100, suffix='...'):
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def parse_time_string(time_str):
    """Parse various time string formats"""
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%d/%m/%Y',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%S.%f',
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(time_str, fmt)
        except ValueError:
            continue
    
    return None


def cleanup_old_files(directory, days_old=30):
    """Delete files older than specified days"""
    from datetime import timedelta
    
    cutoff_date = datetime.now() - timedelta(days=days_old)
    deleted_count = 0
    
    for filepath in Path(directory).glob('*'):
        if filepath.is_file():
            modified_time = datetime.fromtimestamp(filepath.stat().st_mtime)
            if modified_time < cutoff_date:
                filepath.unlink()
                deleted_count += 1
    
    return deleted_count

