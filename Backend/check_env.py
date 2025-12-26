import os

# Check .env file encoding
try:
    with open('.env', 'rb') as f:
        raw = f.read()
        print(f'First 10 bytes: {raw[:10]}')
        if raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
            print('File has UTF-16 BOM')
        elif raw.startswith(b'\xef\xbb\xbf'):
            print('File has UTF-8 BOM')
        else:
            print('No BOM detected')
except Exception as e:
    print(f'Error reading .env: {e}')

# Try loading dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
    print('dotenv loaded successfully')
except Exception as e:
    print(f'Error loading dotenv: {e}')