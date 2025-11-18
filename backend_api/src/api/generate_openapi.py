import json
import os

from src.api.main import app

"""
Generate OpenAPI schema with full app metadata and tags.

This script writes the schema to backend_api/interfaces/openapi.json
"""

# Get the OpenAPI schema
openapi_schema = app.openapi()

# Write to file
output_dir = "interfaces"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "openapi.json")

with open(output_path, "w") as f:
    json.dump(openapi_schema, f, indent=2)
