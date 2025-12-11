"""Entry point for the AI Agent CLI"""

import sys

if __name__ == "__main__":
    try:
        from src.simplified_cli import main
        main()
    except ValueError as e:
        if "REPLICATE_API_TOKEN" in str(e):
            print("\n" + "="*70)
            print("[SETUP REQUIRED]")
            print("="*70)
            print("\nTo set up your API token, run:")
            print("  python setup.py")
            print("\nOr manually create a .env file with:")
            print("  REPLICATE_API_TOKEN=your_token_here")
            print("  MODEL=anthropic/claude-4.5-sonnet")
            print("\nGet your free token at: https://replicate.com/signin")
            print("="*70 + "\n")
            sys.exit(1)
        else:
            raise
    except Exception as e:
        print(f"\n[ERROR] {e}\n")
        sys.exit(1)

