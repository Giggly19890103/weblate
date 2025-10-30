"""
OpenRouter API Translation for Weblate
Batch translation using OpenRouter API via OpenAI SDK
"""

import time
from openai import OpenAI


class OpenRouterTranslator:
    def __init__(self, api_key: str, model: str):
        """
        Initialize the OpenRouter translator using OpenAI SDK
        
        Args:
            api_key: OpenRouter API key (required)
            model: Model name to use (required)
        """
        if not api_key:
            raise ValueError("OpenRouter API key is required.")
        if not model:
            raise ValueError("Model name is required.")
        
        # Initialize OpenAI client with OpenRouter endpoint
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        self.model = model
        
        # Rate limiting
        self.request_delay = 1.0  # seconds between requests
        self.max_retries = 5  # maximum number of retries for 429 errors
    
    def translate_batch_json(self, json_string: str, source_lang: str = "English", target_lang: str = "Chinese") -> str:
        """
        Translate a batch of units provided as JSON string
        
        Args:
            json_string: JSON object with unit IDs as keys and source strings as values
                        Example: {"1": "Hello", "2": "World", "3": "Welcome"}
            source_lang: Source language name (e.g., "English", "Chinese")
            target_lang: Target language name (e.g., "Chinese", "Japanese")
            
        Returns:
            JSON object with unit IDs as keys and translated strings as values
                        Example: {"1": "你好", "2": "世界", "3": "欢迎"}
        """
        # Prepare the prompt for batch translation
        system_prompt = f"""You are a professional technical documentation translator specialized in translating from {source_lang} to {target_lang}.

        CRITICAL REQUIREMENTS:
        1. INPUT: You will receive a JSON object where keys are unit IDs and values are {source_lang} source strings
        2. OUTPUT: You MUST return a VALID JSON OBJECT with the EXACT same keys - this is MANDATORY
        3. BATCH CONTEXT: This is a BATCH translation where all strings are related and from the same document. Ensure terminology consistency and contextual coherence across ALL translations in the batch.
        
        TRANSLATION GUIDELINES:
        - Maintain CONSISTENT terminology and style across all translations in the batch
        - Use the SAME {target_lang} translation for recurring technical terms across all strings
        - Maintain technical accuracy and formatting across all strings
        - Preserve code blocks, links, and markdown syntax in all strings
        - Use standard {target_lang} technical terminology for C++ and Boost libraries CONSISTENTLY

        JSON FORMAT (NON-NEGOTIABLE):
        INPUT:  {{"1": "{source_lang} text 1", "2": "{source_lang} text 2", "3": "{source_lang} text 3"}}
        OUTPUT: {{"1": "{target_lang} translation 1", "2": "{target_lang} translation 2", "3": "{target_lang} translation 3"}}

        CRITICAL: Return ONLY the raw JSON object. NO markdown code fences, NO explanations, NO extra formatting.
        The response MUST be parseable as valid JSON or the entire batch will fail."""

        user_prompt = f"""Translate the following strings from {source_lang} to {target_lang}. Return ONLY a valid JSON object with the same keys but translated values:
        {json_string}"""
        
        # Retry logic with exponential backoff for 429 errors
        retry_delay = self.request_delay
        consecutive_429_errors = 0
        
        for attempt in range(self.max_retries + 1):
            try:
                completion = self.client.chat.completions.create(
                    extra_headers={
                        "X-Title": "Documentation Batch Translation"
                    },
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0,
                    max_tokens=60000
                )
                
                response_text = completion.choices[0].message.content.strip()
                
                # Clean up response - remove markdown code fences if present
                if response_text.startswith('```'):
                    # Remove markdown code fences
                    lines = response_text.split('\n')
                    # Remove first line if it's ```json or ```
                    if lines[0].startswith('```'):
                        lines = lines[1:]
                    # Remove last line if it's ```
                    if lines and lines[-1].strip() == '```':
                        lines = lines[:-1]
                    response_text = '\n'.join(lines).strip()
                
                # Reset consecutive 429 error counter on success
                consecutive_429_errors = 0
                
                # Add delay to respect rate limits
                time.sleep(self.request_delay)
                
                return response_text
                
            except Exception as e:
                error_str = str(e)
                
                # Check if it's a 429 rate limit error
                if "429" in error_str and "rate" in error_str.lower():
                    consecutive_429_errors += 1
                    
                    if attempt < self.max_retries:
                        # Calculate exponential backoff delay
                        backoff_delay = retry_delay * (2 ** consecutive_429_errors)
                        print(f"Rate limit error (429) - attempt {attempt + 1}/{self.max_retries + 1}. Retrying in {backoff_delay:.1f} seconds...")
                        time.sleep(backoff_delay)
                        continue
                    else:
                        print(f"Max retries ({self.max_retries}) exceeded for 429 errors. Returning original JSON.")
                        return json_string  # Return original if all retries fail
                else:
                    # For non-429 errors, raise immediately
                    print(f"Batch translation API request failed: {e}")
                    raise
