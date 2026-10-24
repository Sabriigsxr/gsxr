#!/usr/bin/env python3
import os, urllib.request, json, ssl, subprocess
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE
TARGET = os.environ.get('TARGET', 'https://www.visiwise.co')

print("=== RECON TESTS ===")

# Subdomain enum
print("\n--- Subdomains ---")
try:
    result = subprocess.run(['subfinder', '-d', 'visiwise.co', '-silent'], capture_output=True, text=True, timeout=60)
    for line in result.stdout.strip().split('\n'):
        if line:
            print(f"  {line}")
except Exception as e:
    print(f"  subfinder error: {e}")

# Check live hosts
print("\n--- Live Hosts ---")
subdomains = ['www.visiwise.co', 'app.visiwise.co', 'api.visiwise.co', 'tracking.visiwise.co', 'mail.visiwise.co', 'grafana.visiwise.co', 'git.visiwise.co']
for sub in subdomains:
    try:
        result = subprocess.run(['curl', '-sk', '-m', '5', '-o', '/dev/null', '-w', '%{http_code}', f'https://{sub}/'], capture_output=True, text=True, timeout=10)
        print(f"  {sub}: HTTP {result.stdout.strip()}")
    except Exception as e:
        print(f"  {sub}: ERROR {e}")

# OpenAPI spec
print("\n--- OpenAPI Spec ---")
try:
    req = urllib.request.Request(TARGET + '/api/openapi.json', headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=15, context=ssl_ctx)
    data = json.loads(resp.read().decode())
    print(f"  Title: {data.get('info', {}).get('title')}")
    print(f"  Version: {data.get('info', {}).get('version')}")
    print(f"  Endpoints: {list(data.get('paths', {}).keys())}")
except Exception as e:
    print(f"  Error: {e}")