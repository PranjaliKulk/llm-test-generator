import json

def load_spec(filepath: str)-> dict:
    with open(filepath, "r") as f:
        return json.load(f)

def extract_endpoints(spec: dict) -> list:
    endpoints = []
    paths = spec.get("paths", {})
    
    for path,method in paths.items():
        for method,details in method.items():
            endpoint = {
            "path": path,
            "method": method.upper(),
            "summary": details.get("summary", ""),
            "description": details.get("description", ""),
            "request_body": details.get("requestBody", None),
            "responses": details.get("responses", {})
            }
            endpoints.append(endpoint)
    return endpoints
