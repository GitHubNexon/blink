"""Replicate API wrapper for AI model interactions"""

import json
import requests
from typing import Optional
from src.config import MODEL
from src.token_manager import get_api_token


class ReplicateClient:
    """Client for interacting with Replicate API"""

    def __init__(self, api_token: str = None, model: str = MODEL):
        """
        Initialize Replicate client
        
        Args:
            api_token: Replicate API token (will prompt if not provided)
            model: Model identifier (e.g., "anthropic/claude-3.5-sonnet")
        """
        # Get token from parameter or prompt user
        if api_token is None:
            api_token = get_api_token()
        
        self.api_token = api_token
        self.model = model
        self.base_url = "https://api.replicate.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate text using the Replicate API
        
        Args:
            prompt: User prompt
            system_prompt: System prompt for the model
            max_tokens: Maximum tokens in response
            temperature: Temperature for sampling (0-1)
            
        Returns:
            Generated text
        """
        # Combine system and user prompts
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        try:
            # Create prediction using version hash for anthropic/claude-4.5-sonnet
            payload = {
                "version": "459655107e29a683cb6deb73a9640cf9aeae39ea7c87803a2ae81c311f6ef44f",  # Claude 4.5 Sonnet latest
                "input": {
                    "prompt": full_prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                }
            }
            
            response = requests.post(
                f"{self.base_url}/predictions",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code != 201:
                raise RuntimeError(f"API error: {response.status_code} - {response.text}")
            
            prediction = response.json()
            prediction_id = prediction["id"]
            
            # Poll for completion
            return self._wait_for_prediction(prediction_id)
                
        except Exception as e:
            raise RuntimeError(f"Error calling Replicate API: {e}")


    def _wait_for_prediction(self, prediction_id: str, max_wait: int = 300) -> str:
        """Wait for prediction to complete"""
        import time
        
        start_time = time.time()
        while time.time() - start_time < max_wait:
            response = requests.get(
                f"{self.base_url}/predictions/{prediction_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Error getting prediction: {response.status_code}")
            
            prediction = response.json()
            
            if prediction["status"] == "succeeded":
                output = prediction.get("output", "")
                # Output might be a string or list
                if isinstance(output, list):
                    return "".join(output)
                return str(output)
            
            elif prediction["status"] == "failed":
                raise RuntimeError(f"Prediction failed: {prediction.get('error', 'Unknown error')}")
            
            # Still processing, wait a bit
            time.sleep(1)
        
        raise RuntimeError("Prediction timeout")

    def analyze_code(self, code: str, instruction: str) -> str:
        """
        Analyze and modify code based on instruction
        
        Args:
            code: Code to analyze
            instruction: What to do with the code
            
        Returns:
            Modified or analyzed code
        """
        prompt = f"""You are an expert code analyzer and refactorer.

Instruction: {instruction}

Code to analyze:
```
{code}
```

Provide only the modified code or analysis result, without additional explanation."""
        
        return self.generate(prompt, max_tokens=2048)

    def generate_code(self, specification: str) -> str:
        """
        Generate code based on specification
        
        Args:
            specification: Code specification/requirements
            
        Returns:
            Generated code
        """
        prompt = f"""You are an expert Python developer. Generate clean, well-documented Python code based on the following specification:

{specification}

Provide only the code, without explanations or markdown formatting."""
        
        return self.generate(prompt, max_tokens=2048)

    def plan_tasks(self, objective: str) -> list[str]:
        """
        Create a step-by-step plan for an objective
        
        Args:
            objective: The objective to plan for
            
        Returns:
            List of planned tasks/steps
        """
        prompt = f"""You are a project planning expert. Create a detailed step-by-step plan for the following objective:

{objective}

Return ONLY a JSON array of steps, like this format:
["Step 1: Description", "Step 2: Description", ...]

No other text, just the JSON array."""
        
        result = self.generate(prompt, max_tokens=1024)
        
        try:
            # Try to parse as JSON
            return json.loads(result)
        except json.JSONDecodeError:
            # Fallback: split by newlines if JSON parsing fails
            return [s.strip() for s in result.split("\n") if s.strip()]
