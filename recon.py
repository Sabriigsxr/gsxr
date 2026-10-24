#!/usr/bin/env python3
import os, urllib.request, json, ssl, subprocess
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE
TARGET = os.environ.get('TARGET', 'https://www.visiwise.co')

results = {
    "target": TARGET,
    "timestamp": "2026-10-24",
    "subdomains": [],
    "live_hosts": [],
    "openapi_spec": {}
}

print("=== RECON TESTS ===")

# Subdomain enum
print("\n--- Subdomains ---")
try:
    result = subprocess.run(['subfinder', '-d', 'visiwise.co', '-silent'], capture_output=True, text=True, timeout=60)
    for line in result.stdout.strip().split('\n'):
        if line:
            results["subdomains"].append(line)
            print(f"  {line}")
except Exception as e:
    print(f"  subfinder error: {e}")
    results["subfinder_error"] = str(e)

# Check live hosts
print("\n--- Live Hosts ---")
subdomains = [
    'www.visiwise.co', 'app.visiwise.co', 'api.visiwise.co',
    'tracking.visiwise.co', 'mail.visiwise.co', 'grafana.visiwise.co',
    'git.visiwise.co', 'mattermost.visiwise.co', 'registry.visiwise.co',
    'strapi.visiwise.co', 'gstrapi.visiwise.co', 'strapi.production.visiwise.co',
    'production.visiwise.co', 'app.production.visiwise.co', 'pages.visiwise.co',
    'flower.visiwise.co', 'gcore.visiwise.co'
]
for sub in subdomains:
    try:
        result = subprocess.run(['curl', '-sk', '-m', '5', '-o', '/dev/null', '-w', '%{http_code}', f'https://{sub}/'], capture_output=True, text=True, timeout=10)
        code = result.stdout.strip()
        results["live_hosts"].append({"subdomain": sub, "http_code": code})
        print(f"  {sub}: HTTP {code}")
    except Exception as e:
        print(f"  {sub}: ERROR {e}")
        results["live_hosts"].append({"subdomain": sub, "error": str(e)})

# OpenAPI spec
print("\n--- OpenAPI Spec ---")
try:
    req = urllib.request.Request(TARGET + '/api/openapi.json', headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=15, context=ssl_ctx)
    data = json.loads(resp.read().decode())
    results["openapi_spec"] = {
        "title": data.get('info', {}).get('title'),
        "version": data.get('info', {}).get('version'),
        "endpoints": list(data.get('paths', {}).keys())
    }
    print(f"  Title: {results['openapi_spec']['title']}")
    print(f"  Version: {results['openapi_spec']['version']}")
    print(f"  Endpoints: {results['openapi_spec']['endpoints']}")
except Exception as e:
    print(f"  Error: {e}")
    results["openapi_spec"]["error"] = str(e)

# Save results
os.makedirs("results", exist_ok=True)
with open("results/recon_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n=== Results saved to results/recon_results.json ===")