"""
Quick test: Does the Anthropic API key work?
Usage: ANTHROPIC_API_KEY=sk-ant-... python test_anthropic.py
"""
import os
import sys

key = os.environ.get("ANTHROPIC_API_KEY", "")

if not key:
    print("ERROR: No ANTHROPIC_API_KEY set.")
    print("Run like this:")
    print('  ANTHROPIC_API_KEY="sk-ant-..." python test_anthropic.py')
    sys.exit(1)

print(f"Key: {key[:12]}...{key[-4:]} (length: {len(key)})")

try:
    import anthropic
    print(f"SDK version: {anthropic.__version__}")

    client = anthropic.Anthropic(api_key=key)
    print("Calling Claude...")

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[{"role": "user", "content": "Say 'API key works!' and nothing else."}],
    )

    print(f"SUCCESS: {message.content[0].text}")
    print(f"Model: {message.model}")
    print(f"Tokens used: {message.usage.input_tokens} in, {message.usage.output_tokens} out")

except anthropic.AuthenticationError as e:
    print(f"AUTH ERROR: {e}")
    print("The API key is invalid or expired.")

except anthropic.PermissionDeniedError as e:
    print(f"PERMISSION ERROR: {e}")
    print("The API key doesn't have access to this model.")

except anthropic.RateLimitError as e:
    print(f"RATE LIMIT: {e}")
    print("Key works but you've hit the rate limit.")

except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
