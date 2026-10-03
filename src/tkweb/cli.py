"""
Command-line interface for tkweb - Token-aware Web Scraper.
"""

import argparse
import sys
import json
from .scraper import TokenAwareScraper, quick_scrape
from .processor import process_for_ai_consumption
from .utils import calculate_token_savings, format_content_for_ai
import logging

logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Token-aware web scraper - Extract web content optimized for AI consumption"
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Scrape command
    scrape_parser = subparsers.add_parser('scrape', help='Scrape a URL')
    scrape_parser.add_argument('url', help='URL to scrape')
    scrape_parser.add_argument('--max-tokens', type=int, help='Maximum tokens to return')
    scrape_parser.add_argument('--remove', nargs='+', default=['nav', 'footer', 'header', '.sidebar', '.ads'],
                              help='CSS selectors to remove')
    scrape_parser.add_argument('--output', '-o', help='Output file (default: stdout)')
    scrape_parser.add_argument('--format', choices=['text', 'json', 'metadata'], default='text',
                              help='Output format')
    scrape_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')

    # Process command
    process_parser = subparsers.add_parser('process', help='Process text content')
    process_parser.add_argument('input_file', nargs='?', type=argparse.FileType('r'),
                               default=sys.stdin, help='Input file (default: stdin)')
    process_parser.add_argument('--max-tokens', type=int, help='Maximum tokens to aim for')
    process_parser.add_argument('--aggressive', action='store_true', help='Use aggressive summarization')
    process_parser.add_argument('--output', '-o', help='Output file (default: stdout)')
    process_parser.add_argument('--format', choices=['text', 'json'], default='text',
                              help='Output format')
    process_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')

    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run a demonstration')
    demo_parser.add_argument('--urls', nargs='+',
                            default=['https://httpbin.org/html', 'https://example.com'],
                            help='URLs to demo with')
    demo_parser.add_argument('--max-tokens', type=int, default=500,
                            help='Maximum tokens per URL')
    demo_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')

    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')

    if args.command == 'scrape':
        handle_scrape(args)
    elif args.command == 'process':
        handle_process(args)
    elif args.command == 'demo':
        handle_demo(args)
    else:
        parser.print_help()


def handle_scrape(args):
    """Handle the scrape command."""
    try:
        scraper = TokenAwareScraper()

        logger.info(f"Scraping {args.url}...")
        result = scraper.scrape_url(
            args.url,
            remove_selectors=args.remove,
            max_tokens=args.max_tokens
        )

        if args.format == 'json':
            output = json.dumps(result, indent=2)
        elif args.format == 'metadata':
            # This would require fetching the HTML again for metadata
            # For now, just output basic info
            metadata = {
                'url': result['url'],
                'token_count': result['token_count'],
                'compression_ratio': result['compression_ratio'],
                'original_length': result['original_length'],
                'cleaned_length': result['cleaned_length']
            }
            output = json.dumps(metadata, indent=2)
        else:  # text format
            output = result['content']

        _output_result(output, args.output)

        if args.verbose:
            print(f"\n--- Statistics ---", file=sys.stderr)
            print(f"URL: {result['url']}", file=sys.stderr)
            print(f"Original length: {result['original_length']} chars", file=sys.stderr)
            print(f"Cleaned length: {result['cleaned_length']} chars", file=sys.stderr)
            print(f"Token count: {result['token_count']}", file=sys.stderr)
            print(f"Compression ratio: {result['compression_ratio']:.2%}", file=sys.stderr)

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


def handle_process(args):
    """Handle the process command."""
    try:
        # Read input text
        input_text = args.input_file.read()

        logger.info("Processing content...")
        result = process_for_ai_consumption(
            input_text,
            max_tokens=args.max_tokens,
            aggressive=args.aggressive
        )

        if args.format == 'json':
            output = json.dumps(result, indent=2)
        else:  # text format
            output = result['processed_text']

        _output_result(output, args.output)

        if args.verbose:
            print(f"\n--- Processing Statistics ---", file=sys.stderr)
            print(f"Original token estimate: {result['original_token_estimate']}", file=sys.stderr)
            print(f"Processed token estimate: {result['processed_token_estimate']}", file=sys.stderr)
            print(f"Token savings: {result['token_savings_ratio']:.1%}", file=sys.stderr)
            print(f"Compression ratio: {result['compression_ratio']:.2%}", file=sys.stderr)

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


def handle_demo(args):
    """Handle the demo command."""
    print("Running tkweb demonstration...")
    print("=" * 50)

    scraper = TokenAwareScraper()

    for i, url in enumerate(args.urls, 1):
        print(f"\n[{i}/{len(args.urls)}] Scraping: {url}")
        try:
            result = scraper.scrape_url(url, max_tokens=args.max_tokens)

            print(f"  Original length: {result['original_length']:,} chars")
            print(f"  Cleaned length: {result['cleaned_length']:,} chars")
            print(f"  Token count: {result['token_count']:,} tokens")
            print(f"  Compression: {result['compression_ratio']:.1%}")

            # Show first 200 chars of content
            preview = result['content'][:200].replace('\n', ' ').strip()
            if len(result['content']) > 200:
                preview += "..."
            print(f"  Preview: {preview}")

        except Exception as e:
            print(f"  Error: {str(e)}")

    print(f"\nDemo complete!")


def _output_result(content: str, output_file: str = None):
    """Output content to file or stdout."""
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Output written to {output_file}")
    else:
        print(content)


if __name__ == '__main__':
    main()
