"""
Metadata generation for Digital FTE Vault.
Handles YAML frontmatter creation and parsing for task files.
"""

import yaml
from datetime import datetime
from typing import Dict, Any, Optional


def generate_frontmatter(metadata: Dict[str, Any]) -> str:
    """
    Generate YAML frontmatter string from metadata dictionary.
    
    Args:
        metadata: Dictionary of metadata fields
        
    Returns:
        YAML frontmatter string (including --- delimiters)
    """
    yaml_content = yaml.dump(metadata, sort_keys=False, allow_unicode=True, default_flow_style=False)
    return f"---\n{yaml_content}---\n"


def parse_frontmatter(content: str) -> Optional[Dict[str, Any]]:
    """
    Parse YAML frontmatter from Markdown content.
    
    Args:
        content: Full Markdown file content
        
    Returns:
        Dictionary of metadata fields, or None if no frontmatter
    """
    if not content.startswith('---'):
        return None
    
    end = content.find('---', 3)
    if end == -1:
        return None
    
    yaml_content = content[3:end].strip()
    try:
        return yaml.safe_load(yaml_content)
    except yaml.YAMLError:
        return None


def create_task_metadata(
    task_type: str,
    original_name: str,
    status: str = 'Needs_Action',
    priority: Optional[str] = None,
    tags: Optional[list] = None,
    assigned_to: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create standard task metadata dictionary.
    
    Args:
        task_type: Type of task (file_drop, email, whatsapp, manual)
        original_name: Original filename or identifier
        status: Task status (Needs_Action, In_Progress, Approved, Done)
        priority: Task priority (urgent, normal, low)
        tags: List of tags for categorization
        assigned_to: Agent identifier if claimed
        
    Returns:
        Complete metadata dictionary with required fields
    """
    metadata = {
        'status': status,
        'type': task_type,
        'original_name': original_name,
        'received_timestamp': datetime.now().isoformat() + 'Z',
    }
    
    if priority:
        metadata['priority'] = priority
    
    if tags:
        metadata['tags'] = tags
    
    if assigned_to:
        metadata['assigned_to'] = assigned_to
        metadata['claimed_at'] = datetime.now().isoformat() + 'Z'
    
    return metadata


def generate_markdown_content(frontmatter: Dict[str, Any], body: str = '') -> str:
    """
    Generate complete Markdown file with YAML frontmatter.
    
    Args:
        frontmatter: Metadata dictionary
        body: Markdown body content
        
    Returns:
        Complete Markdown file content
    """
    return generate_frontmatter(frontmatter) + '\n' + body


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe filesystem use.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename (no spaces, special chars, .md extension removed)
    """
    # Remove .md extension if present
    if filename.lower().endswith('.md'):
        filename = filename[:-3]
    
    # Replace spaces and special chars
    sanitized = filename.replace(' ', '_').replace('/', '_').replace('\\', '_')
    sanitized = ''.join(c for c in sanitized if c.isalnum() or c in '_-')
    
    # Limit length
    if len(sanitized) > 50:
        sanitized = sanitized[:50]
    
    return sanitized


def generate_unique_filename(original_name: str) -> str:
    """
    Generate unique filename with timestamp prefix.
    
    Args:
        original_name: Original filename
        
    Returns:
        Unique filename in format YYYYMMDD_HHMMSS_{sanitized_name}.md
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    sanitized = sanitize_filename(original_name)
    return f"{timestamp}_{sanitized}.md"
