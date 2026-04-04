"""
Gmail Authentication - OAuth2 flow for Gmail API.

Usage:
    python src/gmail/gmail_auth.py --authenticate
    python src/gmail/gmail_auth.py --test
"""

import os
import sys
import argparse
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.send']

# Paths
VAULT_ROOT = Path(os.environ.get('VAULT_ROOT', 'E:/hackathon_0_digital_fte/AI_Employee_vault'))
CREDENTIALS_PATH = VAULT_ROOT / 'credentials.json'


def authenticate_gmail():
    """Authenticate Gmail API and save credentials."""
    print("=" * 60)
    print("Gmail API Authentication")
    print("=" * 60)
    print()
    
    # Force new authentication by deleting token.json if it exists
    token_path = VAULT_ROOT / 'token.json'
    if token_path.exists():
        print(f"[Auth] Deleting existing token.json to force new authentication...")
        token_path.unlink()
        print(f"[Auth] Deleted: {token_path}")
        print()
    
    creds = None
    
    # Check if credentials file exists (from Google Cloud Console)
    if not CREDENTIALS_PATH.exists():
        print("ERROR: credentials.json not found!")
        print()
        print("Please follow these steps:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select existing")
        print("3. Enable Gmail API")
        print("4. Create OAuth2 credentials (Desktop app)")
        print("5. Download credentials.json")
        print("6. Place it in:", VAULT_ROOT)
        print()
        return False
    
    # Try to load existing credentials
    if CREDENTIALS_PATH.exists():
        try:
            creds = Credentials.from_authorized_user_file(CREDENTIALS_PATH, SCOPES)
            print("Found existing credentials file")
        except Exception as e:
            print(f"Warning: Could not load existing credentials: {e}")
    
    # Validate or refresh credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired credentials...")
            try:
                from google.auth.transport.requests import Request
                creds.refresh(Request())
                print("Credentials refreshed successfully!")
                
                # Save refreshed credentials
                with open(CREDENTIALS_PATH, 'w') as f:
                    f.write(creds.to_json())
                print("Saved refreshed credentials")
                return True
            except Exception as e:
                print(f"Failed to refresh credentials: {e}")
                print("Please re-authenticate...")
        else:
            # Need to authenticate from scratch
            print("Starting OAuth2 authentication flow...")
            print("This will open a browser window for Google login")
            print()
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
                
                # Save credentials
                with open(CREDENTIALS_PATH, 'w') as f:
                    f.write(creds.to_json())
                
                print()
                print("✓ Authentication successful!")
                print("✓ Credentials saved to:", CREDENTIALS_PATH)
                return True
                
            except Exception as e:
                print()
                print(f"✗ Authentication failed: {e}")
                return False
    
    # Credentials are valid
    print("Credentials are valid and up-to-date")
    return True


def test_gmail_connection():
    """Test Gmail API connectivity."""
    print()
    print("=" * 60)
    print("Testing Gmail API Connection")
    print("=" * 60)
    print()
    
    # First authenticate
    if not authenticate_gmail():
        print()
        print("✗ Test failed: Could not authenticate")
        return False
    
    try:
        # Load credentials
        creds = Credentials.from_authorized_user_file(CREDENTIALS_PATH, SCOPES)
        
        # Build Gmail service
        service = build('gmail', 'v1', credentials=creds)
        
        # Get user profile
        profile = service.users().getProfile().execute()
        print(f"✓ Connected to Gmail account: {profile['emailAddress']}")
        
        # Check unread count
        results = service.users().messages().list(
            userId='me',
            q='is:unread',
            maxResults=1
        ).execute()
        
        unread_count = len(results.get('messages', []))
        print(f"✓ Found {unread_count} unread emails")
        
        print()
        print("=" * 60)
        print("Gmail API Test: PASSED")
        print("=" * 60)
        return True
        
    except Exception as e:
        print()
        print(f"✗ Test failed: {e}")
        print()
        print("Troubleshooting:")
        print("1. Ensure credentials.json is valid")
        print("2. Check that Gmail API is enabled in Google Cloud Console")
        print("3. Verify internet connection")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Gmail API Authentication')
    parser.add_argument('--authenticate', action='store_true', 
                       help='Authenticate Gmail API')
    parser.add_argument('--test', action='store_true',
                       help='Test Gmail API connection')
    
    args = parser.parse_args()
    
    if args.test:
        success = test_gmail_connection()
    elif args.authenticate:
        success = authenticate_gmail()
    else:
        # Default: run authentication
        success = authenticate_gmail()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
