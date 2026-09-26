"""
Content processor module for token-aware web scraping.

Provides additional processing capabilities to further optimize content
for AI consumption.
"""

import re
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ContentProcessor:
    """
    Processes scraped content to optimize for token efficiency.
    """

    @staticmethod
    def remove_extra_whitespace(text: str) -> str:
        """
        Remove extra whitespace and normalize spacing.

        Args:
            text: Input text

        Returns:
            Text with normalized whitespace
        """
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        # Replace multiple newlines with double newline (paragraph separation)
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Remove leading/trailing spaces from each line
        lines = text.split('\n')
        lines = [line.strip() for line in lines]
        text = '\n'.join(lines)
        # Strip leading/trailing whitespace from entire text
        return text.strip()

    @staticmethod
    def extract_key_sentences(text: str, max_sentences: int = 10) -> str:
        """
        Extract key sentences based on simple heuristics.
        This is a simplified version - in practice, you might use NLP techniques.

        Args:
            text: Input text
            max_sentences: Maximum number of sentences to return

        Returns:
            Text containing key sentences
        """
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) <= max_sentences:
            return '. '.join(sentences) + ('.' if sentences else '')

        # Score sentences by length and presence of key indicators
        scored_sentences = []
        for i, sentence in enumerate(sentences):
            score = 0
            # Prefer medium-length sentences (not too short, not too long)
            length = len(sentence)
            if 20 <= length <= 100:
                score += 2
            elif 10 <= length <= 150:
                score += 1

            # Boost for sentences with numbers or proper nouns
            if re.search(r'\d+', sentence):
                score += 1
            if re.search(r'[A-Z][a-z]+', sentence):
                score += 1

            # Slight penalty for very first and last sentences (often boilerplate)
            if i == 0 or i == len(sentences) - 1:
                score -= 0.5

            scored_sentences.append((score, i, sentence))  # Include index for uniqueness

        # Sort by score and take top sentences
        scored_sentences.sort(key=lambda x: x[0], reverse=True)
        top_scored = scored_sentences[:max_sentences]

        # Get the indices of top sentences and sort them to restore original order
        top_indices = sorted([idx for score, idx, sent in top_scored])
        top_sentences = [sentences[idx] for idx in top_indices]

        return '. '.join(top_sentences) + ('.' if top_sentences else '')

    @staticmethod
    def summarize_aggressively(text: str, ratio: float = 0.3) -> str:
        """
        Aggressively summarize text to reduce token count.
        This is a placeholder for more sophisticated summarization.

        Args:
            text: Input text
            ratio: Target ratio of original length to keep (0.0-1.0)

        Returns:
            Summarized text
        """
        if ratio >= 1.0:
            return text

        # Simple approach: take first and last portions
        # In practice, you'd use extractive or abstractive summarization
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) <= 2:
            return text

        # Calculate how many sentences to keep
        target_count = max(1, int(len(sentences) * ratio))

        # Take first, middle, and last sentences for better coverage
        if target_count >= 3:
            step = len(sentences) // (target_count - 1)
            indices = [0] + [i * step for i in range(1, target_count - 1)] + [len(sentences) - 1]
            selected = [sentences[i] for i in indices if i < len(sentences)]
        else:
            # Just take first few sentences
            selected = sentences[:target_count]

        return '. '.join(selected) + ('.' if selected else '')

    @staticmethod
    def remove_boilerplate(text: str) -> str:
        """
        Remove common boilerplate text from web pages.

        Args:
            text: Input text

        Returns:
            Text with boilerplate removed
        """
        # Common boilerplate patterns
        boilerplate_patterns = [
            r'(?i)cookie.*?policy',
            r'(?i)privacy.*?notice',
            r'(?i)terms.*?of.*?service',
            r'(?i)copyright.*?\d{4}',
            r'(?i)all.*?rights.*?reserved',
            r'(?i)sign.*?up.*?for.*?newsletter',
            r'(?i)follow.*?us.*?on.*?social',
            r'(?i)subscribe.*?to.*?our.*?newsletter',
            r'(?i)this.*?site.*?uses.*?cookies',
            r'(?i)we.*?use.*?cookies.*?to.*?improve',
            r'(?i)enable.*?javascript.*?to.*?view.*?this.*?page',
            r'(?i)please.*?enable.*?cookies',
        ]

        cleaned = text
        for pattern in boilerplate_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)

        # Clean up extra whitespace that might have been created
        cleaned = ContentProcessor.remove_extra_whitespace(cleaned)
        return cleaned

    @staticmethod
    def extract_main_content_hints(text: str) -> str:
        """
        Extract content that looks like main article/content based on hints.
        This is a heuristic approach.

        Args:
            text: Input text

        Returns:
            Text that appears to be main content
        """
        lines = text.split('\n')
        if len(lines) < 3:
            return text

        # Score each line
        scored_lines = []
        for line in lines:
            score = 0
            line_lower = line.lower().strip()

            # Boost for longer lines (likely content)
            if len(line) > 50:
                score += 2
            elif len(line) > 20:
                score += 1

            # Boost for lines with sentence-like punctuation
            if line.count(',') >= 2 or line.count(';') >= 1:
                score += 1

            # Boost for lines starting with capital letters
            if line and line[0].isupper():
                score += 1

            # Penalize lines that look like navigation/menu
            nav_indicators = ['home', 'about', 'contact', 'menu', 'nav', 'sidebar',
                            'footer', 'header', 'login', 'register', 'search']
            if any(indicator in line_lower for indicator in nav_indicators):
                score -= 2

            # Penalize very short lines (likely UI elements)
            if len(line.strip()) < 5:
                score -= 1

            scored_lines.append((score, line))

        # Sort by score and take top lines
        scored_lines.sort(key=lambda x: x[0], reverse=True)

        # Take top 70% of lines, but keep original order
        threshold_index = max(1, len(scored_lines) * 7 // 10)
        top_scores = set(line for score, line in scored_lines[:threshold_index] if score > 0)

        # Reconstruct in original order
        result_lines = [line for line in lines if line in top_scores]

        return '\n'.join(result_lines) if result_lines else text


def process_for_ai_consumption(text: str,
                             max_tokens: Optional[int] = None,
                             aggressive: bool = False) -> Dict[str, Any]:
    """
    Process text for optimal AI consumption with token efficiency.

    Args:
        text: Input text to process
        max_tokens: Maximum tokens to aim for (optional)
        aggressive: Whether to use aggressive summarization

    Returns:
        Dictionary with processed content and metrics
    """
    original_tokens = len(text) // 4  # Rough estimate

    # Apply processing pipeline
    processed = ContentProcessor.remove_boilerplate(text)
    processed = ContentProcessor.remove_extra_whitespace(processed)
    processed = ContentProcessor.extract_main_content_hints(processed)

    if aggressive or (max_tokens and len(processed) // 4 > max_tokens * 13):
        processed = ContentProcessor.summarize_aggressively(processed, ratio=0.25)
    elif max_tokens and len(processed) // 4 > max_tokens:
        # Try key sentence extraction first
        target_sentences = max(3, max_tokens // 20)  # Rough: 20 tokens per sentence
        processed = ContentProcessor.extract_key_sentences(processed, max_sentences=target_sentences)

    # Final cleanup
    processed = ContentProcessor.remove_extra_whitespace(processed)

    estimated_tokens = len(processed) // 4  # Rough estimate
    savings = max(0, (original_tokens - estimated_tokens) / original_tokens) if original_tokens > 0 else 0

    return {
        'original_text': text,
        'processed_text': processed,
        'original_token_estimate': original_tokens,
        'processed_token_estimate': estimated_tokens,
        'token_savings_ratio': savings,
        'compression_ratio': len(processed) / len(text) if len(text) > 0 else 0
    }