"""
Unified utilities for synthetic data generation.
Adapted from proven synthetic_data_creation pipeline.

This module provides:
- Factory functions for creating generators
- Batch processing utilities
- Progress tracking and saving
- Quality assessment tools
"""

import os
import json
import time
import yaml
from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass

@dataclass
class ProcessingProgress:
    """Track processing progress for batch operations."""
    total_items: int
    processed_items: int
    successful_items: int
    failed_items: int
    start_time: datetime
    current_batch: int
    estimated_completion: Optional[datetime] = None

@dataclass
class QualityMetrics:
    """Quality assessment metrics for synthetic data."""
    content_changed_ratio: float  # Proportion of items where content actually changed
    avg_fact_incorporation: float  # Average facts incorporated per item
    avg_processing_time: float    # Average processing time per item
    success_rate: float          # Overall success rate
    
def load_config(config_path: str) -> Dict:
    """Load YAML configuration file with error handling."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML configuration: {e}")

def create_generator(
    provider: str,
    model: str = None,
    config_path: str = None,
    **kwargs
):
    """
    Factory function to create the appropriate generator.
    
    Args:
        provider: "openai" or "deepmind"
        model: Specific model name (optional, uses defaults if not provided)
        config_path: Path to configuration file
        **kwargs: Additional parameters
        
    Returns:
        Configured generator instance
    """
    if provider.lower() == "openai":
        from openai_generator import create_openai_generator
        default_model = model or "gpt-4.5"  # Updated to latest GPT-4.5
        return create_openai_generator(
            model=default_model,
            config_path=config_path,
            **kwargs
        )
    elif provider.lower() in ["deepmind", "google", "gemini"]:
        from deepmind_generator import create_deepmind_generator
        default_model = model or "gemini-2.5"  # Updated to latest Gemini 2.5
        return create_deepmind_generator(
            model=default_model,
            config_path=config_path,
            **kwargs
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}. Use 'openai' or 'deepmind'")

def batch_process(
    generator,
    texts: List[str],
    max_facts: int = 3,
    domain: str = "general",
    batch_size: int = 10,
    save_progress: bool = True,
    output_dir: str = "results",
    progress_callback: Optional[callable] = None
) -> List[Dict]:
    """
    Process multiple texts in batches with progress tracking.
    
    Args:
        generator: OpenAI or DeepMind generator instance
        texts: List of texts to process
        max_facts: Maximum facts per item
        domain: Domain for fact schema
        batch_size: Items to process before saving progress
        save_progress: Whether to save intermediate progress
        output_dir: Directory for saving results
        progress_callback: Optional callback for progress updates
        
    Returns:
        List of processing results
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize progress tracking
    progress = ProcessingProgress(
        total_items=len(texts),
        processed_items=0,
        successful_items=0,
        failed_items=0,
        start_time=datetime.now(),
        current_batch=1
    )
    
    results = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    progress_file = os.path.join(output_dir, f"batch_progress_{timestamp}.json")
    
    for i, text in enumerate(texts):
        try:
            # Process single item
            result = generator.generate_complete(
                text=text,
                max_facts=max_facts,
                domain=domain,
                include_metadata=True
            )
            
            # Convert to serializable format
            result_dict = {
                "index": i,
                "original_text": result.original_text,
                "extracted_facts": result.extracted_facts,
                "modified_facts": result.modified_facts,
                "synthetic_text": result.synthetic_text,
                "metadata": result.metadata,
                "timestamp": datetime.now().isoformat()
            }
            
            results.append(result_dict)
            progress.successful_items += 1
            
        except Exception as e:
            print(f"Error processing item {i}: {e}")
            results.append({
                "index": i,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            progress.failed_items += 1
        
        progress.processed_items += 1
        
        # Save progress periodically
        if save_progress and (progress.processed_items % batch_size == 0 or progress.processed_items == len(texts)):
            save_batch_progress(results, progress, progress_file)
        
        # Update progress callback
        if progress_callback:
            progress_callback(progress)
        
        # Calculate ETA
        if progress.processed_items > 0:
            elapsed = datetime.now() - progress.start_time
            avg_time_per_item = elapsed.total_seconds() / progress.processed_items
            remaining_items = progress.total_items - progress.processed_items
            progress.estimated_completion = datetime.now().timestamp() + (remaining_items * avg_time_per_item)
    
    # Final save
    if save_progress:
        final_file = os.path.join(output_dir, f"batch_final_{timestamp}.json")
        with open(final_file, 'w') as f:
            json.dump({
                "results": results,
                "progress": {
                    "total_items": progress.total_items,
                    "successful_items": progress.successful_items,
                    "failed_items": progress.failed_items,
                    "success_rate": progress.successful_items / progress.total_items,
                    "processing_time": str(datetime.now() - progress.start_time)
                }
            }, f, indent=2)
    
    return results

def save_batch_progress(results: List[Dict], progress: ProcessingProgress, filename: str):
    """Save current batch progress to file."""
    progress_data = {
        "timestamp": datetime.now().isoformat(),
        "progress": {
            "total_items": progress.total_items,
            "processed_items": progress.processed_items,
            "successful_items": progress.successful_items,
            "failed_items": progress.failed_items,
            "current_batch": progress.current_batch,
            "start_time": progress.start_time.isoformat(),
            "estimated_completion": progress.estimated_completion
        },
        "results": results
    }
    
    with open(filename, 'w') as f:
        json.dump(progress_data, f, indent=2)

def assess_quality(results: List[Dict]) -> QualityMetrics:
    """
    Assess the quality of batch processing results.
    
    Args:
        results: List of processing results
        
    Returns:
        Quality metrics
    """
    successful_results = [r for r in results if "error" not in r]
    
    if not successful_results:
        return QualityMetrics(0, 0, 0, 0)
    
    # Calculate content change ratio
    content_changed = sum(
        1 for r in successful_results 
        if r.get("metadata", {}).get("content_changed", False)
    )
    content_changed_ratio = content_changed / len(successful_results)
    
    # Calculate average fact incorporation
    total_facts_extracted = sum(
        r.get("metadata", {}).get("facts_extracted", 0)
        for r in successful_results
    )
    avg_fact_incorporation = total_facts_extracted / len(successful_results) if successful_results else 0
    
    # Calculate average processing time
    total_processing_time = sum(
        r.get("metadata", {}).get("processing_time", 0)
        for r in successful_results
    )
    avg_processing_time = total_processing_time / len(successful_results) if successful_results else 0
    
    # Calculate success rate
    success_rate = len(successful_results) / len(results)
    
    return QualityMetrics(
        content_changed_ratio=content_changed_ratio,
        avg_fact_incorporation=avg_fact_incorporation,
        avg_processing_time=avg_processing_time,
        success_rate=success_rate
    )

def progressive_batch_processor(
    generator,
    texts: List[str],
    batch_size: int = 10,
    max_items: int = 100,
    output_dir: str = "results",
    resume_file: Optional[str] = None,
    **kwargs
) -> Dict:
    """
    Progressive batch processor that resumes from where it left off.
    Adapted from the proven synthetic_data_creation notebook implementation.
    
    Args:
        generator: Generator instance
        texts: Full list of texts to process
        batch_size: Items per batch (default 10)
        max_items: Maximum items to process total (default 100)
        output_dir: Output directory
        resume_file: File to resume from (optional)
        **kwargs: Additional arguments for generate_complete
        
    Returns:
        Dictionary with results and progress information
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Load existing progress if available
    all_results = []
    start_index = 0
    
    if resume_file and os.path.exists(resume_file):
        try:
            with open(resume_file, 'r') as f:
                progress_data = json.load(f)
                all_results = progress_data.get('results', [])
                start_index = len(all_results)
        except Exception as e:
            print(f"Could not load resume file: {e}")
    
    # Check completion status
    if start_index >= max_items:
        return {
            "status": "completed",
            "message": f"Maximum items ({max_items}) already processed",
            "total_processed": start_index,
            "results_file": resume_file
        }
    
    if start_index >= len(texts):
        return {
            "status": "dataset_complete", 
            "message": f"All {len(texts)} texts processed",
            "total_processed": start_index,
            "results_file": resume_file
        }
    
    # Determine current batch
    batch_number = (start_index // batch_size) + 1
    end_index = min(start_index + batch_size, len(texts), max_items)
    current_batch = texts[start_index:end_index]
    
    print(f"Processing Batch {batch_number}: items {start_index + 1} to {end_index}")
    print(f"Progress: {start_index}/{max_items} → {end_index}/{max_items}")
    
    # Process current batch
    batch_results = []
    start_time = datetime.now()
    
    for i, text in enumerate(current_batch):
        global_index = start_index + i
        print(f"Processing item {global_index + 1}/{min(len(texts), max_items)}")
        
        try:
            result = generator.generate_complete(text=text, **kwargs)
            
            result_dict = {
                "index": global_index,
                "batch_number": batch_number,
                "original_text": result.original_text,
                "extracted_facts": result.extracted_facts,
                "modified_facts": result.modified_facts,
                "synthetic_text": result.synthetic_text,
                "metadata": result.metadata,
                "timestamp": datetime.now().isoformat()
            }
            
            batch_results.append(result_dict)
            all_results.append(result_dict)
            
            # Save progress after each item
            timestamp = datetime.now().strftime("%Y%m%d")
            progress_file = os.path.join(output_dir, f"progressive_batch_{timestamp}.json")
            
            progress_data = {
                'last_updated': datetime.now().isoformat(),
                'total_processed': len(all_results),
                'current_batch': batch_number,
                'next_start_index': len(all_results),
                'results': all_results
            }
            
            with open(progress_file, 'w') as f:
                json.dump(progress_data, f, indent=2)
                
        except Exception as e:
            print(f"Error processing item {global_index + 1}: {e}")
    
    # Return batch summary
    total_processed = len(all_results)
    processing_time = datetime.now() - start_time
    
    return {
        "status": "batch_completed",
        "batch_number": batch_number,
        "items_processed": len(batch_results),
        "total_processed": total_processed,
        "max_items": max_items,
        "processing_time": str(processing_time),
        "next_batch_ready": total_processed < max_items and total_processed < len(texts),
        "results_file": progress_file,
        "quality_metrics": assess_quality(batch_results)
    }

# Convenience functions for common workflows
def quick_test(provider: str, text: str, model: str = None, config_path: str = None) -> Dict:
    """Quick test of a single text with the specified provider."""
    generator = create_generator(provider, model, config_path)
    result = generator.generate_complete(text)
    
    return {
        "provider": provider,
        "model": generator.model_name,
        "original_length": len(result.original_text),
        "synthetic_length": len(result.synthetic_text), 
        "facts_extracted": len(result.extracted_facts),
        "facts_modified": len(result.modified_facts),
        "content_changed": result.metadata.get("content_changed", False),
        "processing_time": result.metadata.get("processing_time", 0)
    }

def compare_providers(text: str, config_path: str = None) -> Dict:
    """Compare OpenAI and DeepMind on the same text."""
    results = {}
    
    for provider in ["openai", "deepmind"]:
        try:
            result = quick_test(provider, text, config_path=config_path)
            results[provider] = result
        except Exception as e:
            results[provider] = {"error": str(e)}
    
    return results