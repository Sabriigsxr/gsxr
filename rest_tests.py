#!/usr/bin/env python3
import os, urllib.request, json, ssl
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE
TARGET = os.environ.get('TARGET', 'https://www.visiwise.co')

def req(path, method="GET", headers=None, data=None):
    url = TARGET + path
    h = {"User-Agent": "Mozilla/5.0"}
    if headers: h.update(headers)
    d = json.dumps(data).encode() if data else None
    r = urllib.request.Request(url, data=d, headers=h, method=method)
    try:
        resp = urllib.request.urlopen(r, timeout=15, context=ssl_ctx)
        return resp.getcode(), resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

results = {
    "target": TARGET,
    "timestamp": "2026-10-24",
    "endpoints": []
}

print("=== REST API TESTS ===")
endpoints = ["/api/v1/containers/", "/api/v1/shipments/", "/api/openapi.json"]
methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]

for ep in endpoints:
    for m in methods:
        code, body = req(ep, m)
        result = {
            "endpoint": ep,
            "method": m,
            "http_code": code,
            "interesting": code not in [401, 404, 405],
            "response_preview": body[:200]
        }
        results["endpoints"].append(result)
        if code not in [401, 404, 405]:
            print(f"  {m} {ep} -> HTTP {code}: {body[:100]}")
        else:
            print(f"  {m} {ep} -> HTTP {code}")

# Save results
os.makedirs("results", exist_ok=True)
with open("results/rest_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n=== Results saved to results/rest_results.json ===")