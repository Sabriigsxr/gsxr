#!/usr/bin/env python3
import urllib.request
import json
import ssl
import os

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

BASE = "https://www.visiwise.co/graphql/"

# Check for proxy env vars
proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
print(f"Proxy: {proxy}")

if proxy:
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': proxy, 'https': proxy}))
    urllib.request.install_opener(opener)

def req(payload):
    data = json.dumps(payload).encode()
    h = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    r = urllib.request.Request(BASE, data=data, headers=h, method="POST")
    try:
        resp = urllib.request.urlopen(r, timeout=30, context=ssl_ctx)
        return resp.getcode(), resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()
    except Exception as e:
        return 0, str(e)

print("Testing with proxy...")
code, body = req({"query": "{ __typename }"})
print(f"Result: HTTP {code}: {body[:200]}")