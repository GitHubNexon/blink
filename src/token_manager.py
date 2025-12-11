"""Token Manager - Secure API Token Handling for EXE Distribution"""

import os
import sys
import requests
from pathlib import Path
from typing import Optional


class TokenManager:
    """Manages API token prompts and validation"""
    
    def __init__(self):
        self.token: Optional[str] = None
        self.model = "anthropic/claude-4.5-sonnet"
    
    def prompt_for_token(self) -> str:
        """Prompt user for their Replicate API token"""
        print("\n" + "="*70)
        print("[BLINK] API Token Configuration")
        print("="*70)
        print("\nBlink needs your Replicate API token to work.")
        print("This token is:\n")
        print("  ✓ NOT saved to disk")
        print("  ✓ ONLY stored in memory while app is running")
        print("  ✓ CLEARED when you exit")
        print("  ✓ NEVER transmitted except to Replicate API")
        print("\nGet your FREE token at:")
        print("  👉 https://replicate.com/signin\n")
        
        while True:
            token = input("Enter your REPLICATE_API_TOKEN: ").strip()
            
            if not token:
                print("[ERROR] Token cannot be empty.\n")
                continue
            
            if len(token) < 20:
                print("[ERROR] Token appears too short. Check your token.\n")
                continue
            
            # Validate token
            print("\n[VALIDATING] Checking token with Replicate API...")
            if self.validate_token(token):
                print("[OK] Token validated successfully!\n")
                self.token = token
                return token
            else:
                print("[ERROR] Invalid token. Please check and try again.\n")
    
    def validate_token(self, token: str) -> bool:
        """Validate token by making a test API call"""
        try:
            headers = {
                "Authorization": f"Token {token}",
                "Content-Type": "application/json"
            }
            
            # Simple test - check if we can access the account API
            response = requests.get(
                "https://api.replicate.com/v1/account",
                headers=headers,
                timeout=5
            )
            
            return response.status_code == 200
        except Exception as e:
            return False
    
    def get_token(self) -> str:
        """Get token, prompt if not set"""
        if not self.token:
            self.prompt_for_token()
        return self.token
    
    def clear_token(self):
        """Clear token from memory"""
        self.token = None
        print("[INFO] API token cleared from memory.")


# Global token manager instance
_token_manager = None


def get_token_manager() -> TokenManager:
    """Get or create token manager instance"""
    global _token_manager
    if _token_manager is None:
        _token_manager = TokenManager()
    return _token_manager


def get_api_token() -> str:
    """Get API token (prompts if needed)"""
    manager = get_token_manager()
    return manager.get_token()


def clear_api_token():
    """Clear token from memory"""
    manager = get_token_manager()
    manager.clear_token()
