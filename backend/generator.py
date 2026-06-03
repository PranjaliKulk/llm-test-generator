import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_tests(endpoint: dict) -> dict:
    prompt = f"""You are an expert software test engineer.
    
Given this API endpoint, generate a comprehensive set of test cases.

Endpoint:
- Method: {endpoint['method']}
- Path: {endpoint['path']}
- Summary: {endpoint['summary']}
- Description: {endpoint['description']}
- Request Body: {json.dumps(endpoint['request_body'], indent=2)}
- Responses: {json.dumps(endpoint['responses'], indent=2)}

Generate test cases covering:
1. Happy path (valid inputs, expected success)
2. Edge cases (empty input, boundary values)
3. Error scenarios (invalid input, missing fields)

Respond ONLY with a JSON array of test cases. Each test case should have:
- name: string
- description: string
- input: object (request body or null)
- expected_status: number
- expected_behavior: string

No preamble, no markdown, just the JSON array."""
    
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
        )
        
    response_text = message.content[0].text
    clean = response_text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    test_cases = json.loads(clean)
    
    return {
    "endpoint": f"{endpoint['method']} {endpoint['path']}",
    "test_cases": test_cases
}
