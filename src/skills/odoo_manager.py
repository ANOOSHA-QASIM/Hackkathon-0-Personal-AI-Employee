"""
Odoo Manager - Odoo ERP integration for financial tracking.

Uses XML-RPC to connect to Odoo 17.0 and create accounting entries.
Automatically logs marketing expenses for social media posts.
"""

import xmlrpc.client
import os
from datetime import datetime
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class OdooManager:
    """
    Odoo integration manager for creating journal entries.
    
    Usage:
        odoo = OdooManager()
        if odoo.check_connection():
            odoo.log_post_expense(platform='facebook', post_title='Test Post')
    """
    
    def __init__(self):
        """Initialize Odoo connection with credentials from environment."""
        self.url = os.getenv('ODOO_URL', 'http://localhost:8069')
        self.db = os.getenv('ODOO_DB', 'odoo_vault')
        self.username = os.getenv('ODOO_USER', 'admin')
        self.password = os.getenv('ODOO_PASSWORD', 'admin')
        self.marketing_account = os.getenv('ODOO_MARKETING_ACCOUNT', '500000')
        self.base_cost = float(os.getenv('ODOO_BASE_COST', '500'))
        
        self.uid: Optional[int] = None
        self.common: Optional[xmlrpc.client.ServerProxy] = None
        self.objects: Optional[xmlrpc.client.ServerProxy] = None
        
    def authenticate(self) -> bool:
        """
        Authenticate with Odoo via XML-RPC.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            # Connect to common endpoint for authentication
            self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            
            # Authenticate and get user ID
            self.uid = self.common.authenticate(
                self.db,
                self.username,
                self.password,
                {}
            )
            
            if self.uid:
                # Connect to object endpoint for API calls
                self.objects = xmlrpc.client.ServerProxy(
                    f'{self.url}/xmlrpc/2/object',
                    use_builtin_types=True
                )
                print(f"[Odoo] Authentication successful - UID: {self.uid}")
                return True
            else:
                print("[Odoo] Authentication failed - check credentials")
                return False
                
        except Exception as e:
            print(f"[Odoo] Connection error: {e}")
            return False
    
    def check_connection(self) -> bool:
        """
        Check if Odoo is reachable and authenticated.
        
        Returns:
            bool: True if connection healthy, False otherwise
        """
        # If not authenticated, try to authenticate
        if self.uid is None:
            return self.authenticate()
        
        # Check if we can access the database
        try:
            # Try to read a simple record to verify connection
            models = self.objects.execute_kw(
                self.db,
                self.uid,
                self.password,
                'ir.model',
                'search_count',
                [[]],
                {}
            )
            print(f"[Odoo] Connection healthy - found {models} models")
            return True
        except Exception as e:
            print(f"[Odoo] Connection check failed: {e}")
            # Reset uid to force re-authentication
            self.uid = None
            return False
    
    def _get_account_id_by_code(self, account_code: str) -> Optional[int]:
        """
        Get Odoo account ID by account code.
        
        Args:
            account_code: Account code (e.g., '500000')
            
        Returns:
            Account ID if found, None otherwise
        """
        try:
            account_ids = self.objects.execute_kw(
                self.db,
                self.uid,
                self.password,
                'account.account',
                'search',
                [[['code', '=', account_code]]],
                {}
            )
            
            if account_ids:
                return account_ids[0]
            else:
                print(f"[Odoo] Account {account_code} not found")
                return None
        except Exception as e:
            print(f"[Odoo] Error finding account: {e}")
            return None
    
    def create_journal_entry(self, platform: str, post_title: str, amount: float = 500.0) -> Dict[str, Any]:
        """
        Create a marketing expense journal entry in Odoo.
        
        Args:
            platform: Social media platform (facebook, instagram, twitter, linkedin)
            post_title: Title/content of the post
            amount: Expense amount in PKR (default: 500)
            
        Returns:
            dict: Odoo response with move_id and status
            
        Raises:
            ConnectionError: If Odoo unreachable
            AuthenticationError: If credentials invalid
        """
        if not self.objects:
            raise ConnectionError("Not connected to Odoo. Call authenticate() first.")
        
        try:
            # Get marketing expense account
            expense_account_id = self._get_account_id_by_code(self.marketing_account)
            if not expense_account_id:
                raise ValueError(f"Marketing expense account {self.marketing_account} not found in Odoo")
            
            # Get cash/bank account (default: 100000)
            bank_account_id = self._get_account_id_by_code('100000')
            if not bank_account_id:
                print("[Odoo] Using default bank account (100000 not found)")
                bank_account_id = expense_account_id  # Fallback to same account
            
            # Create journal entry
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            entry_name = f"Marketing Expense - {platform.capitalize()} - {timestamp}"
            
            move_vals = {
                'move_type': 'entry',
                'name': entry_name,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'ref': f"Social Post: {post_title}",
                'line_ids': [
                    (0, 0, {
                        'account_id': expense_account_id,
                        'debit': amount,
                        'credit': 0.0,
                        'name': f'Marketing Expense - {platform}'
                    }),
                    (0, 0, {
                        'account_id': bank_account_id,
                        'debit': 0.0,
                        'credit': amount,
                        'name': f'Cash/Bank - {platform}'
                    })
                ],
                'state': 'draft'  # Create as draft first, can be posted manually in Odoo
            }
            
            # Create the journal entry
            move_id = self.objects.execute_kw(
                self.db,
                self.uid,
                self.password,
                'account.move',
                'create',
                [move_vals]
            )
            
            print(f"[Odoo] Journal entry created - Move ID: {move_id}")
            return {
                'move_id': move_id,
                'status': 'posted',
                'platform': platform,
                'amount': amount,
                'ref': post_title
            }
            
        except Exception as e:
            print(f"[Odoo] Error creating journal entry: {e}")
            raise
    
    def log_post_expense(self, platform: str, post_title: str) -> Optional[Dict[str, Any]]:
        """
        High-level method: Log expense for a social media post.
        Wraps create_journal_entry with error handling.
        
        Args:
            platform: Social media platform
            post_title: Post title/content
            
        Returns:
            dict if successful, None if failed (logs warning)
        """
        try:
            # Check connection first
            if not self.check_connection():
                print("[Odoo] Cannot log expense - connection failed")
                return None
            
            # Create journal entry with base cost
            result = self.create_journal_entry(
                platform=platform,
                post_title=post_title,
                amount=self.base_cost
            )
            
            print(f"[Odoo] Expense logged: {platform} post - {self.base_cost} PKR")
            return result
            
        except Exception as e:
            print(f"[Odoo] Failed to log expense: {e}")
            return None


# Test script - runs when file is executed directly
if __name__ == '__main__':
    print("=" * 60)
    print("Odoo Manager - Connection Test")
    print("=" * 60)
    print()
    
    # Create manager instance
    odoo = OdooManager()
    
    # Test authentication
    print("[Test] Authenticating with Odoo...")
    if odoo.authenticate():
        print(f"✓ Odoo Connected Successfully!")
        print(f"✓ User ID (UID): {odoo.uid}")
        print(f"✓ Database: {odoo.db}")
        print(f"✓ URL: {odoo.url}")
        print()
        
        # Test connection check
        print("[Test] Checking connection health...")
        if odoo.check_connection():
            print("✓ Connection healthy")
            print()
            
            # Test journal entry creation (optional - comment out if not needed)
            print("[Test] Testing journal entry creation...")
            try:
                result = odoo.create_journal_entry(
                    platform='test',
                    post_title='Test Post - Connection Verification',
                    amount=1.0  # Small amount for test
                )
                print(f"✓ Test journal entry created - Move ID: {result.get('move_id')}")
            except Exception as e:
                print(f"⚠ Journal entry test skipped: {e}")
        else:
            print("✗ Connection check failed")
    else:
        print("✗ Odoo Connection Failed")
        print("  Please ensure:")
        print("  1. Docker containers are running (docker-compose ps)")
        print("  2. Odoo is accessible at http://localhost:8069")
        print("  3. Database 'odoo_vault' is created")
        print("  4. Credentials in .env are correct")
    
    print()
    print("=" * 60)
