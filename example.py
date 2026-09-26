"""
Example usage of tkweb - Token-aware Web Scraper.
"""

from tkweb import TokenAwareScraper, quick_scrape
from tkweb.processor import process_for_ai_consumption
from tkweb.utils import calculate_token_savings

def example_basic_scraping():
    """Demonstrate basic scraping functionality."""
    print("=== Basic Scraping Example ===")

    # Initialize scraper
    scraper = TokenAwareScraper()

    # Example with a simple URL (using httpbin for testing)
    try:
        result = scraper.scrape_url('https://httpbin.org/html', max_tokens=500)

        print(f"URL: {result['url']}")
        print(f"Original length: {result['original_length']} characters")
        print(f"Cleaned length: {result['cleaned_length']} characters")
        print(f"Token count: {result['token_count']} tokens")
        print(f"Compression ratio: {result['compression_ratio']:.1%}")
        print("\nFirst 300 characters of content:")
        print(result['content'][:300] + ("..." if len(result['content']) > 300 else ""))
        print()

    except Exception as e:
        print(f"Error scraping: {e}")
        print("Note: This might fail if there's no internet connection or the URL is inaccessible.")
        print()

def example_quick_scrape():
    """Demonstrate the quick scrape convenience function."""
    print("=== Quick Scrape Example ===")

    try:
        # Quick scrape with token limit
        content = quick_scrape('https://httpbin.org/html', max_tokens=300)

        print(f"Quick scraped content ({len(content)} characters):")
        print(content[:200] + ("..." if len(content) > 200 else ""))
        print()

    except Exception as e:
        print(f"Error in quick scrape: {e}")
        print()

def example_content_processing():
    """Demonstrate content processing capabilities."""
    print("=== Content Processing Example ===")

    # Sample text with boilerplate and extra whitespace
    sample_text = """


    Welcome to our website!


    Home About Products Contact


    This is the main content of our article. It discusses important topics
    that users might find valuable. The quick brown fox jumps over the lazy dog.


    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod
    tempor incididunt ut labore et dolore magna aliqua.


    Cookie Policy: We use cookies to enhance your browsing experience.
    By continuing to use this site, you accept our use of cookies.


    Copyright 2023 Example Company. All rights reserved.
    Follow us on social media!
    """

    print("Original text:")
    print(repr(sample_text[:100]) + "...")
    print(f"Length: {len(sample_text)} characters")
    print()

    # Process for AI consumption
    result = process_for_ai_consumption(sample_text, max_tokens=100)

    print("Processed text:")
    print(repr(result['processed_text'][:100]) + "...")
    print(f"Length: {len(result['processed_text'])} characters")
    print()

    print("Processing Statistics:")
    print(f"Original token estimate: {result['original_token_estimate']}")
    print(f"Processed token estimate: {result['processed_token_estimate']}")
    print(f"Token savings: {result['token_savings_ratio']:.1%}")
    print(f"Compression ratio: {result['compression_ratio']:.1%}")
    print()

def example_token_savings_calculation():
    """Demonstrate token savings calculation."""
    print("=== Token Savings Calculation Example ===")

    original = "This is a test sentence. " * 50  # Repeated content
    processed = "This is a test sentence. " * 10   # Reduced version

    savings = calculate_token_savings(original, processed)

    print(f"Original tokens: {savings['original_tokens']}")
    print(f"Processed tokens: {savings['processed_tokens']}")
    print(f"Tokens saved: {savings['tokens_saved']}")
    print(f"Savings percentage: {savings['savings_percentage']:.1f}%")
    print()

def main():
    """Run all examples."""
    print("tkweb - Token-aware Web Scraper Examples")
    print("=" * 50)
    print()

    example_basic_scraping()
    example_quick_scrape()
    example_content_processing()
    example_token_savings_calculation()

    print("Examples complete!")

if __name__ == '__main__':
    main()