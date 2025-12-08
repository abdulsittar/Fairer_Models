"""
DeepMind/Google AI (Gemini) synthetic data generator.
Adapted from proven synthetic_data_creation pipeline for Gemini 2.0 Flash and Gemini 1.5 models.

Supports Gemini 2.0 Flash, Gemini 1.5 Pro, and Gemini 1.5 Flash with optimized 
prompts and robust error handling.
"""

import google.generativeai as genai
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

class DeepMindGenerator:
    """
    DeepMind Gemini-powered synthetic data generator using proven prompts and methodology.
    """
    
    def __init__(
        self,
        model_name: str = "gemini-2.5",  # Updated to latest Gemini 2.5
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
        
        # Configure Gemini API (Updated August 2025)
        api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Gemini API key not found. Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable.")
        
        genai.configure(api_key=api_key)
        
        # Apply config overrides if available
        if self.config and "deepmind" in self.config:
            model_config = self._get_model_config()
            if model_config:
                self.temperature = model_config.get("temperature", temperature)
                self.max_tokens = model_config.get("max_tokens", max_tokens)
                self.rate_limit = model_config.get("rate_limit", {})
        
        # Initialize the Gemini model (Updated API usage)
        self.model = genai.GenerativeModel(self.model_name)
        
        self.logger.info(f"Initialized DeepMind generator with model: {self.model_name}")
    
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
        if not self.config or "deepmind" not in self.config:
            return {}
        
        # Map model names to config keys (Updated August 2025)
        model_mapping = {
            "gemini-2.5": "gemini_2_5",
            "gemini-2.0-flash": "gemini_2_flash",
            "gemini-1.5-pro": "gemini_1_5_pro",
            "gemini-1.5-flash": "gemini_1_5_flash",
            # Legacy support
            "gemini-2.0-flash-exp": "gemini_2_flash"
        }
        
        config_key = model_mapping.get(self.model_name)
        return self.config["deepmind"].get(config_key, {}) if config_key else {}
    
    def _generate_with_retry(self, prompt: str, max_retries: int = 3) -> str:
        """Generate content with retry logic using updated Gemini API."""
        for attempt in range(max_retries):
            try:
                # Updated API usage following Google's documentation
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=self.temperature,
                        max_output_tokens=self.max_tokens,
                    )
                )
                
                if response.text:
                    return response.text.strip()
                else:
                    self.logger.warning(f"Empty response on attempt {attempt + 1}")
                    
            except Exception as e:
                self.logger.error(f"Error generating content (attempt {attempt + 1}): {e}")
                if "quota" in str(e).lower() or "rate" in str(e).lower():
                    if attempt < max_retries - 1:
                        wait_time = 30 * (attempt + 1)  # Progressive backoff
                        self.logger.info(f"Rate limit hit, waiting {wait_time}s before retry {attempt + 2}")
                        time.sleep(wait_time)
                        continue
                elif attempt == max_retries - 1:
                    self.logger.error("All attempts failed")
                    raise
        
        return ""
    
    def extract_structured_facts(
        self, 
        text: str, 
        fact_schema: Optional[List[Dict]] = None,
        max_facts: Optional[int] = None,
        domain: str = "general"
    ) -> FactExtractionResult:
        """
        Extract structured facts using the proven prompt methodology adapted for Gemini.
        
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
        
        # Proven prompt adapted for Gemini's strengths
        prompt = f"""You are a precise fact extraction system. Extract facts from the text using the specified categories.

For each fact found, return a JSON object with:
- "name_of_fact": the category name from the schema
- "description_of_fact": what this fact represents  
- "specific_data": the exact information from the text
- "common_examples": examples of this fact type

FACT CATEGORIES TO FIND:
{schema_desc}

INPUT TEXT:
{text}

INSTRUCTIONS:
1. Only extract facts that are explicitly mentioned in the text
2. Use the exact category names provided
3. Be precise with the specific_data field
4. Return valid JSON array format only

OUTPUT FORMAT:
[
    {{
        "name_of_fact": "Entity",
        "description_of_fact": "Main organization mentioned",
        "specific_data": "World Health Organization",
        "common_examples": "WHO, CDC, government agencies"
    }}
]

EXTRACTED FACTS:"""
        
        try:
            response_text = self._generate_with_retry(prompt)
            
            # Parse JSON response
            try:
                clean_text = clean_json_response(response_text)
                facts_json = json.loads(clean_text)
                if not isinstance(facts_json, list):
                    facts_json = []
            except json.JSONDecodeError:
                self.logger.warning(f"Failed to parse JSON response: {response_text}")
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
        Uses proven prompt adapted for Gemini's capabilities.
        """
        if not extracted_facts:
            return []
        
        facts_json = json.dumps(extracted_facts, indent=2)
        
        # Enhanced modification prompt for Gemini
        prompt = f"""You are a precise fact modification system. Your task is to create plausible but FALSE versions of the given facts.

RULES:
1. Keep the exact same JSON structure
2. Only modify the "specific_data" field
3. Make changes that are believable but definitively incorrect
4. Maintain data types (numbers stay numbers, dates stay dates)
5. Make subtle but clear alterations

EXAMPLES OF GOOD MODIFICATIONS:
- "95% effective" → "87% effective" 
- "January 2024" → "March 2024"
- "New York" → "Philadelphia"
- "1000 participants" → "850 participants"

ORIGINAL FACTS:
{facts_json}

INSTRUCTIONS:
1. Analyze each fact's specific_data
2. Create a plausible but false alternative
3. Ensure the modification is clearly different from the original
4. Return the complete JSON structure with only specific_data changed

MODIFIED FACTS:"""
        
        try:
            response_text = self._generate_with_retry(prompt)
            
            try:
                clean_text = clean_json_response(response_text)
                modified_facts = json.loads(clean_text)
                if not isinstance(modified_facts, list):
                    modified_facts = extracted_facts
            except json.JSONDecodeError:
                self.logger.warning(f"Failed to parse modified facts JSON: {response_text}")
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
        Uses enhanced prompt optimized for Gemini's text generation capabilities.
        """
        if not modified_facts:
            return original_text
        
        facts_to_incorporate = []
        for fact in modified_facts:
            fact_name = fact.get('name_of_fact', 'Unknown')
            fact_data = fact.get('specific_data', 'N/A')
            facts_to_incorporate.append(f"• {fact_name}: {fact_data}")
        
        facts_str = "\\n".join(facts_to_incorporate)
        
        # Enhanced prompt optimized for Gemini
        style_instruction = "maintaining the exact same writing style, tone, and structure" if style_preservation else "adapting the writing style as appropriate"
        
        prompt = f"""You are a precise text rewriting system. Your task is to rewrite the given text by replacing original facts with modified versions.

REWRITING RULES:
1. Find facts in the original text that correspond to the modified facts below
2. Replace ONLY those specific factual elements with the modified versions
3. Keep everything else identical: {style_instruction}
4. Ensure natural flow and readability after modifications
5. Maintain approximately the same text length
6. ALL modified facts must be incorporated into the final text

ORIGINAL TEXT:
{original_text}

FACTS TO INCORPORATE:
{facts_str}

REWRITING PROCESS:
1. Identify each original fact in the text
2. Replace with the corresponding modified version
3. Ensure smooth integration
4. Verify all modified facts are included

REWRITTEN TEXT:"""
        
        try:
            result = self._generate_with_retry(prompt)
            
            # Clean up response
            result = self._clean_synthetic_response(result)
            
            # Verify the result is different from original
            if result and result != original_text.strip():
                return result
            else:
                self.logger.warning("Generated content identical to original or empty")
                return original_text
                
        except Exception as e:
            self.logger.error(f"Error generating synthetic content: {e}")
            return original_text
    
    def _clean_synthetic_response(self, text: str) -> str:
        """Clean up Gemini response to return only the rewritten content."""
        cleanup_patterns = [
            "I have rewritten",
            "Here's the rewritten", 
            "The rewritten text is:",
            "Here is the modified",
            "Following the instructions",
            "Based on the requirements"
        ]
        
        lines = text.split('\\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip explanatory lines
            if any(pattern.lower() in line.lower() for pattern in cleanup_patterns):
                continue
            # Skip lines that look like instructions
            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', 'Step', 'REWRITTEN')):
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
def create_deepmind_generator(
    model: str = "gemini-2.5",  # Updated to latest Gemini 2.5
    config_path: str = None,
    **kwargs
) -> DeepMindGenerator:
    """
    Factory function to create DeepMind generator with configuration.
    
    Args:
        model: Gemini model name ("gemini-2.5", "gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash")
        config_path: Path to YAML configuration file
        **kwargs: Additional parameters for generator
        
    Returns:
        Configured DeepMind generator instance
    """
    return DeepMindGenerator(
        model_name=model,
        config_path=config_path,
        **kwargs
    )
