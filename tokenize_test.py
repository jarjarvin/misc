import json
import tiktoken
from toon import encode, decode

"""
Compact Serializer Format (CSF) Demo
--------------------------------------------
Simple reduce token usage when sending a known structured data to LLMs

JSON  – standard, self-describing format for APIs.
CSF   – ultra-compact, schema-based encoding for internal use.
TOON  – readable, token-efficient format for LLM prompts.

The script prints token counts and sample encodings for each layer.
"""

MODEL = "gpt-4o-mini"   
enc = tiktoken.encoding_for_model(MODEL)

# Schema and role mappings
SCHEMA_MAP = {
    "i": "id",
    "n": "name",
    "e": "email",
    "ia": "is_active",
    "a": "age",
    "ad": "address",
    "s": "street",
    "c": "city",
    "st": "state",
    "z": "zip_code",
    "pn": "phone_numbers",
    "r": "roles",
    "ca": "created_at",
}
REVERSE_MAP = {v: k for k, v in SCHEMA_MAP.items()}
ROLE_MAP = {"admin": 0, "editor": 1}
REVERSE_ROLE_MAP = {v: k for k, v in ROLE_MAP.items()}


# -----------------------------------------------------------
# CSF ENCODING FUNCTIONS
# -----------------------------------------------------------

def to_shortkey_json(full_json: dict) -> dict:
    """Convert full JSON → short-key JSON with numeric role mapping."""
    result = {}
    for k, v in full_json.items():
        if k == "address" and isinstance(v, dict):
            result["ad"] = {REVERSE_MAP[subk]: subv for subk, subv in v.items()}
        elif k == "roles":
            result["r"] = [ROLE_MAP.get(role, role) for role in v]
        else:
            short_key = REVERSE_MAP.get(k, k)
            result[short_key] = v
    return result


def to_delimited_string(short_json: dict) -> str:
    """Convert short-key JSON → compact CSF delimited string."""
    ad = short_json["ad"]
    fields = [
        str(short_json["i"]),
        short_json["n"].replace(" ", "_"),
        short_json["e"],
        "1" if short_json["ia"] else "0",
        str(short_json["a"]),
        ad["s"].replace(" ", "_"),
        ad["c"],
        ad["st"],
        ad["z"],
        ",".join(short_json["pn"]),
        ",".join(map(str, short_json["r"])),
        short_json["ca"],
    ]
    return "|".join(fields)


def token_count(text: str) -> int:
    """Return true token count for a given text."""
    return len(enc.encode(text))


# -----------------------------------------------------------
# EXAMPLES
# -----------------------------------------------------------

full_json = {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "is_active": True,
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "zip_code": "62704",
    },
    "phone_numbers": ["+1-555-123-4567", "+1-555-987-6543"],
    "roles": ["admin", "editor"],
    "created_at": "2025-11-11T10:00:00Z",
}

short_json = to_shortkey_json(full_json)
csf = to_delimited_string(short_json)
toon = encode(full_json)     # from the toon library

original_json = json.dumps(full_json, separators=(",", ":"))
short_json_str = json.dumps(short_json, separators=(",", ":"))

'''
print("Original JSON:\n", original_json)
print("\nShort-key JSON:\n", short_json_str)
print("\nCSF delimited string:\n", csf)
print("\nTOON example:\n", toon)
'''

# -----------------------------------------------------------
# Example CSF Prompt
# -----------------------------------------------------------

print("Token counts using", MODEL)
print("──────────────────────────────────────────────")
print(f"Original JSON:         {token_count(original_json):>4} tokens")
print(f"Short-key JSON (CSF):  {token_count(short_json_str):>4} tokens")
print(f"CSF Delimited String:  {token_count(csf):>4} tokens")
print(f"TOON Representation:   {token_count(toon):>4} tokens")
print("──────────────────────────────────────────────\n")



prompt = """
You are given data in Compact Serializer Format (CSF), a token-efficient schema-based encoding.

Schema (field order):
i|n|e|ia|a|s|c|st|z|pn|r|ca

Meaning:
id | name | email | is_active | age | street | city | state | zip_code | phone_numbers | roles | created_at

Encoding rules:
- "|" separates fields
- "," separates multiple items (arrays)
- "_" represents spaces
- "1" means True, "0" means False
- Roles are numeric: 0 = admin, 1 = editor

Please decode the data into a readable JSON structure before reasoning.
"""

print(prompt)


