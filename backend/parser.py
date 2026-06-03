import json
import os


def load_spec(path: str) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Spec file not found: {path}")
    try:
        with open(path, "r") as f:
            spec = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in spec file: {e}")
    if not isinstance(spec, dict):
        raise ValueError("Spec file must contain a JSON object at the top level")
    return spec


def extract_endpoints(spec: dict) -> list[dict]:
    paths = spec.get("paths", {})
    if not paths:
        return []

    endpoints = []
    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if method.lower() not in {"get", "post", "put", "patch", "delete", "head", "options"}:
                continue
            if not isinstance(operation, dict):
                continue
            endpoints.append({
                "method": method.upper(),
                "path": path,
                "summary": operation.get("summary", ""),
                "parameters": operation.get("parameters", []),
                "request_body": operation.get("requestBody"),
                "responses": operation.get("responses", {}),
            })

    return endpoints
