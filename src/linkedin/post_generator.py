"""
LinkedIn Post Generator - Creates draft posts with proper metadata.

Usage:
    python src/linkedin/post_generator.py --create "Your post content here"
    python src/linkedin/post_generator.py --template
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
import yaml

# Paths
VAULT_ROOT = Path(os.environ.get(
    'VAULT_ROOT',
    'E:/hackathon_0_digital_fte/AI_Employee_vault'
))
IN_PROGRESS_PATH = VAULT_ROOT / 'In_Progress' / 'linkedin-agent'


def generate_post_metadata(content: str, media_path: str = None, 
                          scheduled_time: str = None, tags: list = None):
    """
    Generate metadata for LinkedIn post.
    
    Args:
        content: Post text content
        media_path: Optional path to image/media file
        scheduled_time: Optional scheduled time (ISO 8601)
        tags: Optional list of tags
    
    Returns:
        Dictionary with post metadata
    """
    metadata = {
        'status': 'draft',
        'platform': 'linkedin',
        'content': content,
        'created_at': datetime.now().isoformat() + 'Z',
        'created_by': 'user',
        'hitl_approved': False,
    }
    
    if media_path:
        metadata['media_path'] = media_path
    
    if scheduled_time:
        metadata['scheduled_time'] = scheduled_time
    
    if tags:
        metadata['tags'] = tags
    
    return metadata


def create_draft_post(content: str, media_path: str = None,
                     scheduled_time: str = None, tags: list = None,
                     filename: str = None):
    """
    Create a draft LinkedIn post in /In_Progress/linkedin-agent/.
    
    Args:
        content: Post text content
        media_path: Optional path to image/media
        scheduled_time: Optional scheduled time
        tags: Optional list of tags
        filename: Optional custom filename
    
    Returns:
        Path to created draft file
    """
    # Generate metadata
    metadata = generate_post_metadata(content, media_path, scheduled_time, tags)
    
    # Generate filename
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"linkedin_draft_{timestamp}.md"
    
    # Ensure directory exists
    IN_PROGRESS_PATH.mkdir(parents=True, exist_ok=True)
    
    # Generate content
    yaml_content = yaml.dump(metadata, sort_keys=False, allow_unicode=True, 
                            default_flow_style=False)
    
    post_content = f"---\n{yaml_content}---\n\n"
    post_content += "## Post Preview\n\n"
    post_content += f"**Platform**: LinkedIn\n"
    post_content += f"**Status**: Draft\n"
    if scheduled_time:
        post_content += f"**Scheduled**: {scheduled_time}\n"
    if media_path:
        post_content += f"**Media**: {media_path}\n"
    post_content += "\n---\n\n"
    post_content += "## HITL Approval\n\n"
    post_content += "**To Approve**: Move this file to `/Approved/` folder\n\n"
    post_content += "**To Reject**: Move this file to `/Rejected/` folder with feedback\n\n"
    post_content += "- [ ] Approved (move to /Approved)\n"
    post_content += "- [ ] Rejected (move to /Rejected with feedback)\n\n"
    post_content += "**Feedback**: \n"
    
    # Write file
    draft_path = IN_PROGRESS_PATH / filename
    with open(draft_path, 'w', encoding='utf-8') as f:
        f.write(post_content)
    
    print(f"[LinkedIn] Created draft post: {filename}")
    print(f"[LinkedIn] Location: {draft_path}")
    print()
    print("Next steps:")
    print("1. Review the draft in:", draft_path)
    print("2. If approved, move to /Approved/")
    print("3. LinkedIn poster will automatically publish")
    
    return draft_path


def create_template():
    """Create a post template file."""
    template_content = """---
status: draft
platform: linkedin
content: |
  [Your post content here]
  
  [Add your message, announcement, or update]
  
  [Include a call-to-action if applicable]
  
  #Hashtag1 #Hashtag2 #Hashtag3
media_path: ./media/post-image.png  # Optional - remove if no image
scheduled_time: 2026-03-29T09:00:00Z  # Optional - remove for immediate posting
created_at: 2026-03-28T14:00:00Z
created_by: user
hitl_approved: false
tags:
  - draft
  - linkedin
---

## Post Preview

**Platform**: LinkedIn
**Status**: Draft
**Scheduled**: Upon approval
**Media**: None (optional)

---

## HITL Approval

**To Approve**: Move this file to `/Approved/` folder

**To Reject**: Move this file to `/Rejected/` folder with feedback below

- [ ] Approved (move to /Approved)
- [ ] Rejected (move to /Rejected with feedback)

**Feedback**: 

---

## Minimalist Design Rules

For posts with images:
- **Theme**: Dark background (#1a1a1a or darker)
- **Typography**: Clean, readable fonts (Arial, Helvetica, Inter)
- **Colors**: Monochrome + single accent color
- **Images**: No human icons/avatars
- **Text on Image**: Minimal (headline only)
"""
    
    # Ensure directory exists
    IN_PROGRESS_PATH.mkdir(parents=True, exist_ok=True)
    
    # Write template
    template_path = IN_PROGRESS_PATH / 'linkedin_post_template.md'
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    print(f"[LinkedIn] Created template: {template_path}")
    return template_path


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='LinkedIn Post Generator')
    parser.add_argument('--create', type=str, help='Create a draft post with given content')
    parser.add_argument('--media', type=str, help='Path to media file (optional)')
    parser.add_argument('--schedule', type=str, help='Scheduled time (ISO 8601 format)')
    parser.add_argument('--tags', type=str, help='Comma-separated tags')
    parser.add_argument('--filename', type=str, help='Custom filename')
    parser.add_argument('--template', action='store_true', help='Create post template')
    
    args = parser.parse_args()
    
    if args.template:
        create_template()
    elif args.create:
        # Parse tags
        tags = None
        if args.tags:
            tags = [tag.strip() for tag in args.tags.split(',')]
        
        # Create draft
        create_draft_post(
            content=args.create,
            media_path=args.media,
            scheduled_time=args.schedule,
            tags=tags,
            filename=args.filename
        )
    else:
        # Default: show help
        parser.print_help()
        print()
        print("Examples:")
        print("  python src/linkedin/post_generator.py --template")
        print("  python src/linkedin/post_generator.py --create \"Excited to announce...\"")
        print("  python src/linkedin/post_generator.py --create \"Post content\" --tags \"announcement,ai\"")
    
    sys.exit(0)


if __name__ == '__main__':
    main()
