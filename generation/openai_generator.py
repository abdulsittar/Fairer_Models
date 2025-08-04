"""
OpenAI-based synthetic data generator.
Adapted from proven synthetic_data_creation pipeline with enhanced prompts.

Supports GPT-4o, GPT-4 Turbo, and other OpenAI models with optimized rate limiting
and robust error handling.
"""

import openai
import os
import json
import time
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import yaml

from fact_schemas import get_fact_schema, validate_fact_schema

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FactExtractionResult:
    """Structure for fact extraction results."""
    original_text: str
    extracted_facts: List[Dict[str, Any]]
    model_used: Optional[str] = None
    processing_time: Optional[float] = None

@dataclass
class SyntheticDataResult:
    """Complete result structure for synthetic data generation."""
    original_text: str
    extracted_facts: List[Dict[str, Any]]
    modified_facts: List[Dict[str, Any]] 
    synthetic_text: str
    metadata: Dict[str, Any]

def clean_json_response(response_text: str) -> str:
    """Clean JSON response by removing markdown code blocks."""
    if "```json" in response_text:
        start = response_text.find("```json") + 7
        end = response_text.find("```", start)
        if end != -1:
            response_text = response_text[start:end].strip()
    elif "```" in response_text:
        start = response_text.find("```") + 3  
        end = response_text.find("```", start)
        if end != -1:
            response_text = response_text[start:end].strip()
    
    return response_text.strip()

class OpenAIGenerator:
    """
    OpenAI-powered synthetic data generator using proven prompts and methodology.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-4o",
        api_key: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        config_path: Optional[str] = None
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.logger = logger
        
        # Load configuration if provided
        self.config = self._load_config(config_path) if config_path else {}
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        
        # Apply config overrides if available
        if self.config and "openai" in self.config:
            model_config = self._get_model_config()
            if model_config:
                self.temperature = model_config.get("temperature", temperature)
                self.max_tokens = model_config.get("max_tokens", max_tokens)
                self.rate_limit = model_config.get("rate_limit", {})
        
        self.logger.info(f"Initialized OpenAI generator with model: {self.model_name}")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load YAML configuration file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.warning(f"Could not load config from {config_path}: {e}")
            return {}
    
    def _get_model_config(self) -> Dict:
        """Get configuration for the current model."""
        if not self.config or "openai" not in self.config:
            return {}
        
        # Map model names to config keys (Updated August 2025)
        model_mapping = {
            "gpt-4.5": "gpt4_5",
            "o4": "o4", 
            "gpt-4o": "gpt4o",
            "gpt-4-turbo": "gpt4_turbo",
            "gpt-3.5-turbo": "gpt3_5_turbo",
            "gpt-4o-mini": "gpt4o_mini"
        }
        
        config_key = model_mapping.get(self.model_name)
        return self.config["openai"].get(config_key, {}) if config_key else {}
    
    def extract_structured_facts(
        self, 
        text: str, 
        fact_schema: Optional[List[Dict]] = None,
        max_facts: Optional[int] = None,
        domain: str = "general"
    ) -> FactExtractionResult:
        """
        Extract structured facts using the proven prompt methodology.
        
        Args:
            text: Input text to extract facts from
            fact_schema: Custom fact schema (if None, uses domain default)
            max_facts: Maximum number of facts to extract
            domain: Domain for schema selection ("general", "health", "social")
        """
        start_time = time.time()
        
        # Get fact schema
        if fact_schema is None:
            fact_schema = get_fact_schema(content_type="news", domain=domain)
        
        if not validate_fact_schema(fact_schema):
            raise ValueError("Invalid fact schema provided")
        
        # Create schema description for prompt
        schema_desc = ""
        for fact in fact_schema:
            schema_desc += f"- {fact['name']}: {fact['description']} (Examples: {fact['common_examples']})\\n"
        
        # Proven prompt from synthetic_data_creation testing
        prompt = f"""Extract facts from the following text using the specified fact types. 
For each fact found, provide:
1. "name_of_fact": the category name
2. "description_of_fact": description of what this fact represents  
3. "specific_data": the exact value/information from the text
4. "common_examples": similar examples for this fact type

Fact Types to Look For:
{schema_desc}

Text: {text}

Return ONLY a valid JSON array of facts found, like:
[
    {{
        "name_of_fact": "Entity",
        "description_of_fact": "Main organization mentioned",
        "specific_data": "World Health Organization",
        "common_examples": "WHO, CDC, government agencies"
    }}
]

Facts:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            facts_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                clean_text = clean_json_response(facts_text)
                facts_json = json.loads(clean_text)
                if not isinstance(facts_json, list):
                    facts_json = []
            except json.JSONDecodeError:
                self.logger.warning(f"Failed to parse JSON response: {facts_text}")
                facts_json = []
            
            # Limit facts if specified
            if max_facts and len(facts_json) > max_facts:
                facts_json = facts_json[:max_facts]
            
            processing_time = time.time() - start_time
            
            return FactExtractionResult(
                original_text=text,
                extracted_facts=facts_json,
                model_used=self.model_name,
                processing_time=processing_time
            )
            
        except Exception as e:
            self.logger.error(f"Error extracting structured facts: {e}")
            return FactExtractionResult(
                original_text=text, 
                extracted_facts=[],
                model_used=self.model_name,
                processing_time=time.time() - start_time
            )
    
    def modify_facts(self, extracted_facts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Modify extracted facts to create plausible but false information.
        Uses proven prompt from synthetic_data_creation pipeline.
        """
        if not extracted_facts:
            return []
        
        facts_json = json.dumps(extracted_facts, indent=2)
        
        # Proven modification prompt
        prompt = f"""Modify the following extracted facts to create plausible but FALSE information.
Keep the same structure and fact types, but change the specific data to be incorrect.
Make subtle but clearly false changes to numbers, dates, locations, names, etc.

Important:
- Keep the same JSON structure
- Only modify the "specific_data" field
- Make changes that are plausible but definitely false
- Maintain the same data type (if it's a number, keep it a number)

Original facts:
{facts_json}

Return ONLY a valid JSON array with the same structure but modified specific_data:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            modified_text = response.choices[0].message.content.strip()
            
            try:
                clean_text = clean_json_response(modified_text)
                modified_facts = json.loads(clean_text)
                if not isinstance(modified_facts, list):
                    modified_facts = extracted_facts
            except json.JSONDecodeError:
                self.logger.warning(f"Failed to parse modified facts JSON: {modified_text}")
                modified_facts = extracted_facts
            
            return modified_facts
            
        except Exception as e:
            self.logger.error(f"Error modifying facts: {e}")
            return extracted_facts
    
    def generate_synthetic_content(
        self, 
        original_text: str, 
        modified_facts: List[Dict],
        style_preservation: bool = True
    ) -> str:
        """
        Generate synthetic content incorporating modified facts.
        Uses enhanced prompt with retry logic from proven pipeline.
        """
        if not modified_facts:
            return original_text
        
        facts_to_incorporate = []
        for fact in modified_facts:
            facts_to_incorporate.append(f"- {fact.get('name_of_fact', 'Unknown')}: {fact.get('specific_data', 'N/A')}")
        
        facts_str = "\\n".join(facts_to_incorporate)
        
        # Enhanced prompt from proven testing
        style_instruction = "Maintain the same writing style, tone, and structure." if style_preservation else "You may adapt the writing style as needed."
        
        prompt = f"""You are tasked with rewriting text to incorporate specific modified facts. You MUST replace the original facts in the text with the modified versions.

Instructions:
1. Find each piece of original information that corresponds to the modified facts below
2. Replace the original information with the modified version 
3. {style_instruction}
4. Ensure the text flows naturally after the replacements
5. Keep the content length approximately the same
6. Make sure ALL modified facts are incorporated into the rewritten text

Original text:
{original_text}

Replace these facts in the text:
{facts_str}

Return ONLY the rewritten text, no explanations:"""
        
        # Retry logic for robustness
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                
                result = response.choices[0].message.content.strip()
                
                # Clean up response
                result = self._clean_synthetic_response(result)
                
                # Verify the result is different from original
                if result != original_text.strip():
                    return result
                else:
                    self.logger.warning(f"Generated content identical to original, attempt {attempt + 1}")
                    
            except Exception as e:
                self.logger.error(f"Error generating synthetic content (attempt {attempt + 1}): {e}")
                if "rate_limit" in str(e).lower() and attempt < max_retries - 1:
                    # Rate limit hit, wait before retry
                    wait_time = 30 * (attempt + 1)  # Progressive backoff
                    self.logger.info(f"Rate limit hit, waiting {wait_time}s before retry {attempt + 2}")
                    time.sleep(wait_time)
                    continue
                elif attempt == max_retries - 1:
                    self.logger.error("All attempts failed, returning original content")
                    break
        
        return original_text
    
    def _clean_synthetic_response(self, text: str) -> str:
        """Clean up LLM response to return only the rewritten content."""
        cleanup_patterns = [
            "I have carefully replaced",
            "Here's the step-by-step process", 
            "The resulting rewritten",
            "I followed:",
            "Here is the rewritten",
            "The rewritten text:"
        ]
        
        lines = text.split('\\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip explanatory lines
            if any(pattern in line for pattern in cleanup_patterns):
                continue
            # Skip numbered instruction lines
            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.')):
                continue
            cleaned_lines.append(line)
        
        return '\\n'.join(cleaned_lines).strip()
    
    def generate_complete(
        self,
        text: str,
        fact_schema: Optional[List[Dict]] = None,
        max_facts: int = 3,
        domain: str = "general",
        include_metadata: bool = True
    ) -> SyntheticDataResult:
        """
        Complete synthetic data generation pipeline.
        
        Args:
            text: Original text to process
            fact_schema: Custom fact schema (optional)
            max_facts: Maximum facts to extract and modify
            domain: Domain for schema selection
            include_metadata: Include processing metadata
            
        Returns:
            Complete synthetic data result
        """
        start_time = time.time()
        
        # Step 1: Extract facts
        extraction_result = self.extract_structured_facts(
            text, fact_schema, max_facts, domain
        )
        
        # Step 2: Modify facts  
        modified_facts = self.modify_facts(extraction_result.extracted_facts)
        
        # Step 3: Generate synthetic content
        synthetic_text = self.generate_synthetic_content(text, modified_facts)
        
        # Prepare metadata
        metadata = {
            "model": self.model_name,
            "processing_time": time.time() - start_time,
            "facts_extracted": len(extraction_result.extracted_facts),
            "facts_modified": len(modified_facts),
            "domain": domain,
            "content_changed": synthetic_text != text.strip()
        } if include_metadata else {}
        
        return SyntheticDataResult(
            original_text=text,
            extracted_facts=extraction_result.extracted_facts,
            modified_facts=modified_facts,
            synthetic_text=synthetic_text,
            metadata=metadata
        )

# Factory function for easy initialization
def create_openai_generator(
    model: str = "gpt-4.5",  # Updated to latest GPT-4.5
    config_path: str = None,
    **kwargs
) -> OpenAIGenerator:
    """
    Factory function to create OpenAI generator with configuration.
    
    Args:
        model: OpenAI model name ("gpt-4.5", "o4", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o-mini")
        config_path: Path to YAML configuration file
        **kwargs: Additional parameters for generator
        
    Returns:
        Configured OpenAI generator instance
    """
    return OpenAIGenerator(
        model_name=model,
        config_path=config_path,
        **kwargs
    )
