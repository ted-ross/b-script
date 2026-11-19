#!/usr/bin/env python3

import json
import yaml
from jsonschema import validate, ValidationError
import sys

def main():
    # 1. Load the JSON Schema
    if len(sys.argv) == 3:
        with open(sys.argv[2], "r") as schema_file:
            if sys.argv[2].lower().endswith(".yaml"):
                schema = yaml.safe_load(schema_file)
            else:
                schema = json.load(schema_file)
    else:
        schema = meta_schema()

    # 2. Load and parse the YAML file
    with open(sys.argv[1], "r") as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)

    # 3. Validate
    try:
        validate(instance=yaml_data, schema=schema)
        print("Valid")
    except ValidationError as e:
        print(f"Validation failed: {e.message}")

def meta_schema():
    text = """
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://json-schema.org/draft/2020-12/schema",
    "$vocabulary": {
        "https://json-schema.org/draft/2020-12/vocab/core": true,
        "https://json-schema.org/draft/2020-12/vocab/applicator": true,
        "https://json-schema.org/draft/2020-12/vocab/unevaluated": true,
        "https://json-schema.org/draft/2020-12/vocab/validation": true,
        "https://json-schema.org/draft/2020-12/vocab/meta-data": true,
        "https://json-schema.org/draft/2020-12/vocab/format-annotation": true,
        "https://json-schema.org/draft/2020-12/vocab/content": true
    },
    "$dynamicAnchor": "meta",

    "title": "Core and Validation specifications meta-schema",
    "allOf": [
        {"$ref": "meta/core"},
        {"$ref": "meta/applicator"},
        {"$ref": "meta/unevaluated"},
        {"$ref": "meta/validation"},
        {"$ref": "meta/meta-data"},
        {"$ref": "meta/format-annotation"},
        {"$ref": "meta/content"}
    ],
    "type": ["object", "boolean"],
    "$comment": "This meta-schema also defines keywords that have appeared in previous drafts in order to prevent incompatible extensions as they remain in common use.",
    "properties": {
        "definitions": {
            "$comment": "'definitions' has been replaced by '$defs'.",
            "type": "object",
            "additionalProperties": { "$dynamicRef": "#meta" },
            "deprecated": true,
            "default": {}
        },
        "dependencies": {
            "$comment": "'dependencies' has been split and replaced by 'dependentSchemas' and 'dependentRequired' in order to serve their differing semantics.",
            "type": "object",
            "additionalProperties": {
                "anyOf": [
                    { "$dynamicRef": "#meta" },
                    { "$ref": "meta/validation#/$defs/stringArray" }
                ]
            },
            "deprecated": true,
            "default": {}
        },
        "$recursiveAnchor": {
            "$comment": "'$recursiveAnchor' has been replaced by '$dynamicAnchor'.",
            "$ref": "meta/core#/$defs/anchorString",
            "deprecated": true
        },
        "$recursiveRef": {
            "$comment": "'$recursiveRef' has been replaced by '$dynamicRef'.",
            "$ref": "meta/core#/$defs/uriReferenceString",
            "deprecated": true
        }
    }
}
    """
    return json.loads(text)

main()
