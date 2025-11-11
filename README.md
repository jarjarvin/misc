
# MISC Stuff

## CSF (Compact Serializer Format)

### Token Counts (using `gpt-4o-mini`)

- Original JSON: 98 tokens 
- Short-key JSON (CSF): 93 tokens
- CSF Delimited String: 65 tokens
- TOON Representation: 106 tokens


### Overview
**CSF (Compact Serializer Format)** is a token-efficient, schema-based encoding designed to reduce prompt and data size for LLM interactions.

### Prompt example

You are given data in Compact Serializer Format (CSF), a token-efficient schema-based encoding. 
Schema (field order): i|n|e|ia|a|s|c|st|z|pn|r|ca 
Meaning: id | name | email | is_active | age | street | city | state | zip_code | phone_numbers | roles | created_at 

Encoding rules: 
- "|" separates fields
- "," separates multiple items (arrays)
- "_" represents spaces
- "1" means True, "0" means False
- Roles are numeric: 0 = admin, 1 = editor 

Please decode the data into a readable JSON structure before reasoning.


