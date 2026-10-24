#!/usr/bin/env python3
import urllib.request
import json
import ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

BASE = "https://www.visiwise.co/graphql/"

def req(payload):
    data = json.dumps(payload).encode()
    h = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    r = urllib.request.Request(BASE, data=data, headers=h, method="POST")
    try:
        resp = urllib.request.urlopen(r, timeout=15, context=ssl_ctx)
        return resp.getcode(), resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()
    except Exception as e:
        return 0, str(e)

print("=== INVESTIGATING 'register' MUTATION ===\n")

# Test register mutation with various inputs
tests = [
    ("register empty", {"query": "mutation { register { __typename } }"}),
    ("register with email", {"query": "mutation { register(email: \"test@test.com\") { __typename } }"}),
    ("register with input", {"query": "mutation { register(input: {email: \"test@test.com\", password: \"test\"}) { __typename } }"}),
    ("registerUser", {"query": "mutation { registerUser { __typename } }"}),
    ("createAccount", {"query": "mutation { createAccount { __typename } }"}),
    ("signUp", {"query": "mutation { signUp { __typename } }"}),
    ("createUser", {"query": "mutation { createUser { __typename } }"}),
]

for name, payload in tests:
    code, body = req(payload)
    print(f"{name}: HTTP {code}: {body[:200]}")

# Try to get schema hints via field suggestions (typo-based enumeration)
print("\n=== FIELD SUGGESTION ENUMERATION ===")
typo_fields = [
    "usre", "usrs", "uer", "shippment", "contianer", "trcking",
    "mutaiton", "mutaitons", "querry", "querries"
]
for field in typo_fields:
    code, body = req({"query": f"{{ {field} }}"})
    if "did you mean" in body.lower() or "suggestion" in body.lower():
        print(f"  SUGGESTION for '{field}': {body[:200]}")

# Try __type introspection for specific types
print("\n=== TYPE INTROSPECTION ===")
type_names = ["User", "Shipment", "Container", "Tracking", "Query", "Mutation", "Auth", "AuthPayload"]
for t in type_names:
    code, body = req({"query": f"{{ __type(name: \"{t}\") {{ name kind fields {{ name }} }} }}"})
    if "null" not in body or len(body) > 100:
        print(f"  {t}: HTTP {code}: {body[:300]}")