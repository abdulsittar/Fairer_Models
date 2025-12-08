"""
Configurable fact characterization schemas for synthetic data generation.
Adapted from proven synthetic_data_creation pipeline.

This module provides flexible fact schemas that can be customized for different domains
while maintaining the proven 3-step methodology:
1. Extract facts using structured schema
2. Modify facts to create plausible but false information  
3. Generate synthetic content incorporating modified facts
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class FactSchema:
    """Structure for defining fact extraction schemas."""
    name: str
    description: str
    common_examples: str
    domain: Optional[str] = None

# Base configurable schema template
CONFIGURABLE_FACT_SCHEMA = [
    FactSchema(
        name="Entity",
        description="Main entity, organization, or actor mentioned",
        common_examples="Companies, organizations, people, institutions",
        domain="general"
    ),
    FactSchema(
        name="Location", 
        description="Geographic location or place mentioned",
        common_examples="Cities, countries, regions, specific venues",
        domain="general"
    ),
    FactSchema(
        name="Timeframe",
        description="Date, time period, or temporal reference",
        common_examples="Specific dates, periods, durations, relative time",
        domain="general"
    ),
    FactSchema(
        name="Statistics",
        description="Numerical data, percentages, or quantitative measurements", 
        common_examples="Numbers, percentages, quantities, measurements",
        domain="general"
    ),
    FactSchema(
        name="Topic",
        description="Main subject or theme being discussed",
        common_examples="Primary focus, subject matter, key themes",
        domain="general"
    )
]

# Example domain-specific schema (COVID/Health) - from proven pipeline
COVID_FACT_SCHEMA = [
    FactSchema(
        name="Type",
        description="The type of vaccine or medical intervention discussed",
        common_examples="COVID vaccine, Pfizer-BioNTech, Moderna, Johnson & Johnson, treatments",
        domain="health"
    ),
    FactSchema(
        name="Actor", 
        description="Entity offering, promoting, or involved with the intervention",
        common_examples="Pfizer-BioNTech, Moderna, WHO, CDC, government health agencies",
        domain="health"
    ),
    FactSchema(
        name="Location",
        description="Geographic location mentioned in health context",
        common_examples="New York City, United States, Europe, hospitals, vaccination centers",
        domain="health"
    ),
    FactSchema(
        name="Timeframe", 
        description="Date, time period, or temporal reference for health events",
        common_examples="January 2024, within two weeks, over 6 months, today, past week",
        domain="health"
    ),
    FactSchema(
        name="Statistics",
        description="Health-related numerical data, effectiveness, or measurements",
        common_examples="95% effectiveness, 150 patients, 50,000 participants, 25% increase",
        domain="health"
    ),
    FactSchema(
        name="Medical_Effect",
        description="Health outcomes, side effects, or medical impacts",
        common_examples="severe illness protection, transmission reduction, side effects, immunity",
        domain="health"
    ),
    FactSchema(
        name="Topic",
        description="Main health-related topic or focus",
        common_examples="vaccination campaign, variant detection, clinical trial, public health policy",
        domain="health"
    )
]

# Tweet-optimized schema (for shorter content)
TWEET_FACT_SCHEMA = [
    FactSchema(
        name="Entity",
        description="Main entity or actor mentioned in the tweet",
        common_examples="Organizations, people, brands, institutions", 
        domain="social"
    ),
    FactSchema(
        name="Location",
        description="Geographic location mentioned",
        common_examples="Cities, countries, venues, online platforms",
        domain="social"
    ),
    FactSchema(
        name="Statistics", 
        description="Numbers, percentages, or quantitative data",
        common_examples="Follower counts, percentages, quantities, rankings",
        domain="social"
    ),
    FactSchema(
        name="Topic",
        description="Main topic or hashtag theme discussed",
        common_examples="Trending topics, themes, subjects, hashtags",
        domain="social"
    )
]

def get_fact_schema(content_type: str = "news", domain: str = "general") -> List[Dict[str, str]]:
    """
    Get appropriate fact schema based on content type and domain.
    
    Args:
        content_type: Type of content ("news", "tweets", "articles", "social")
        domain: Domain focus ("general", "health", "finance", "politics", etc.)
    
    Returns:
        List of fact definitions compatible with LLM prompts
    """
    # Select base schema
    if content_type.lower() in ['tweet', 'tweets', 'social']:
        if domain == "health":
            # Use COVID schema but limited for tweets
            base_schema = COVID_FACT_SCHEMA[:4]  # Limit for tweet length
        else:
            base_schema = TWEET_FACT_SCHEMA
    elif domain == "health":
        base_schema = COVID_FACT_SCHEMA
    else:
        base_schema = CONFIGURABLE_FACT_SCHEMA
    
    # Convert to dict format expected by LLM prompts
    return [
        {
            "name": fact.name,
            "description": fact.description,
            "common_examples": fact.common_examples
        }
        for fact in base_schema
    ]

def create_custom_schema(facts: List[Dict[str, str]], domain: str = "custom") -> List[Dict[str, str]]:
    """
    Create a custom fact schema from user-defined facts.
    
    Args:
        facts: List of dicts with 'name', 'description', 'common_examples'
        domain: Domain identifier for the custom schema
        
    Returns:
        Validated fact schema ready for use
    """
    validated_facts = []
    required_fields = ['name', 'description', 'common_examples']
    
    for fact in facts:
        if all(field in fact for field in required_fields):
            validated_facts.append({
                "name": fact['name'],
                "description": fact['description'], 
                "common_examples": fact['common_examples']
            })
        else:
            raise ValueError(f"Fact missing required fields {required_fields}: {fact}")
    
    return validated_facts

def validate_fact_schema(schema: List[Dict]) -> bool:
    """Validate that fact schema has required fields."""
    required_fields = ['name', 'description', 'common_examples']
    
    for fact in schema:
        if not all(field in fact for field in required_fields):
            return False
    
    return len(schema) > 0

# Schema registry for easy access
SCHEMA_REGISTRY = {
    "general": CONFIGURABLE_FACT_SCHEMA,
    "health": COVID_FACT_SCHEMA,
    "social": TWEET_FACT_SCHEMA
}

def list_available_schemas() -> Dict[str, str]:
    """Return available schemas with descriptions."""
    return {
        "general": "General-purpose fact schema for news and articles",
        "health": "Health/medical domain schema (proven with COVID data)",
        "social": "Social media optimized schema for tweets and short content"
    }

def get_schema_info(schema_name: str) -> Dict[str, Any]:
    """Get detailed information about a specific schema."""
    if schema_name not in SCHEMA_REGISTRY:
        raise ValueError(f"Schema '{schema_name}' not found. Available: {list(SCHEMA_REGISTRY.keys())}")
    
    schema = SCHEMA_REGISTRY[schema_name]
    return {
        "name": schema_name,
        "fact_count": len(schema),
        "facts": [{"name": f.name, "description": f.description} for f in schema],
        "domain": schema[0].domain if schema else "unknown"
    }
