import requests
from typing import Dict, TypeVar
from .custom_types import AskModelRequest, AskModelResponse

T = TypeVar("T", bound=AskModelResponse)

def ask_model(
    request: AskModelRequest,
    base_url: str,
    headers: Dict[str, str],
    response_format: type[T] = AskModelResponse,
) -> T:
    payload = {
        "model": request.model,
        "messages": [{"role": "user", "content": request.prompt}],
        "max_tokens": request.max_tokens,
        "temperature": request.temperature,
    }
    try:
        response = requests.post(base_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        message = data["choices"][0]["message"]["content"].strip()
        return response_format(content=message)
    except Exception as e:
        return response_format(content=f"Error: {str(e)}")
