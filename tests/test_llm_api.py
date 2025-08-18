import os
from unittest.mock import MagicMock, patch

import dotenv
import pytest

from genestack_tools.custom_types import AskModelRequest, AskModelResponse
from genestack_tools.llm_api import ask_model

dotenv.load_dotenv()


@pytest.fixture
def sample_request():
    return AskModelRequest(
        prompt="Explain how sequencing data compression can benefit from Genestack",
        model="anthropic/claude-sonnet-4",
        max_tokens=100,
        temperature=0.2,
    )


def test_ask_model_success(sample_request):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "Genestack can make sequencing data smaller and faster"
                }
            }
        ]
    }
    mock_response.raise_for_status.return_value = None

    with patch(
        "genestack_tools.llm_api.requests.post", return_value=mock_response
    ) as mock_post:
        response = ask_model(
            sample_request,
            base_url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer fake_key",
                "Content-Type": "application/json",
            },
        )

        assert isinstance(response, AskModelResponse)
        assert (
            response.content == "Genestack can make sequencing data smaller and faster"
        )
        mock_post.assert_called_once()


def test_ask_model_exception(sample_request):
    with patch(
        "genestack_tools.llm_api.requests.post", side_effect=Exception("Network error")
    ):
        response = ask_model(
            sample_request,
            base_url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer fake_key",
                "Content-Type": "application/json",
            },
        )

        assert isinstance(response, AskModelResponse)
        assert "Error" in response.content


@pytest.mark.skipif(
    os.getenv("OPENROUTER_API_KEY") is None,
    reason="OPENROUTER_API_KEY not set, skipping real API call",
)
def test_ask_model_real_request():
    api_key = os.getenv("OPENROUTER_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    request = AskModelRequest(
        prompt="How can sequencing data compression benefit from Genestack?",
        model="anthropic/claude-sonnet-4",
    )

    response = ask_model(
        request,
        base_url="https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
    )
    assert isinstance(response, AskModelResponse)
    assert isinstance(response.content, str)
    assert len(response.content) > 0
