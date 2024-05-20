import argparse
import asyncio
import json
import sys
import httpx
from typing import List, Tuple, Any, Dict
from decouple import config


async def chat_completion(
    headers: Dict[str, str],
    remote_llm_url: str,
    user_message: str,
    **kwargs: Any,
) -> Tuple[Any, Dict[str, str]]:
    # Base payload
    payload = {
        "remote_llm_url": remote_llm_url,
        "user_message": user_message,
    }

    # Add extra keyword arguments to the payload
    payload.update(kwargs)

    api_url = f"{config('PROXY_HOST', default='', cast=str)}/tc/{config('OPENAI_VERSION', default='', cast=str)}"

    if payload.get("stream"):
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST", api_url, headers=headers, json=payload, timeout=120.0
            ) as response:
                if response.status_code == 200:
                    response_headers = response.headers

                    response_text = ""
                    buffered_data = ""
                    # iterate through the stream, if it breaks, the test failed
                    async for chunk_bytes in response.aiter_bytes():
                        chunk = chunk_bytes.decode("utf-8")  # Decode bytes to string

                        data_elements = chunk.split("data:")

                        for str_data in data_elements:
                            str_data = str_data.strip()
                            if not str_data or str_data == "[DONE]":
                                continue

                            buffered_data += str_data

                            try:
                                data_dict = json.loads(buffered_data)
                                buffered_data = ""
                            except json.decoder.JSONDecodeError:
                                print("JSONDecodeError")
                                continue

                            for i, choice in enumerate(data_dict["choices"]):
                                delta = choice.get("delta", {})
                                content = delta.get("content", "")

                                print(content)
                                response_text += content

                                # Update the finish reason
                                choice["finish_reason"] = choice.get("finish_reason")

                            # Check if the response is complete
                            if all(
                                choice["finish_reason"] is not None
                                for choice in data_dict["choices"]
                            ):
                                response = data_dict
                                break

                    return response_text, response_headers
                else:
                    text = await response.aread()
                    print(text)
                    raise Exception(
                        f"API call failed with status code {response.status_code}"
                    )
    else:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                api_url, headers=headers, json=payload, timeout=120.0
            )

        if response.status_code == 200:
            response_headers = response.headers
            content = response.json()
            return content, response_headers
        else:
            print(response.text)
            raise Exception(f"API call failed with status code {response.status_code}")


async def call_RB(
    user_message, cache_control, stream
):
    helvia_rag_cache_token = config("RAG_BUDDY_TOKEN")

    # Pass the cache control header, if provided
    cache_control_header = {}
    if cache_control:
        cache_control_header = {
            "Helvia-RAG-Buddy-Cache-Control": ", ".join(cache_control)
        }

    headers = {"Helvia-RAG-Buddy-Token": helvia_rag_cache_token, **cache_control_header}
    headers2 = {
        "Authorization": "Bearer " + config("OPENAI_API_KEY"),
        "Content-Type": "application/json",
    }
    # Merge the headers
    headers = {**headers, **headers2}

    remote_llm_url = "https://api.openai.com/v1/chat/completions"
    model = "gpt-4"
    temperature = 0

    content, response_headers = await chat_completion(
        headers,
        remote_llm_url,
        user_message,
        model=model,
        temperature=temperature,
        stream=stream,
    )

    print(f"Response Headers: {response_headers}")

    cache_status = response_headers.get("Helvia-RAG-Buddy-Cache-Status")
    cache_hit = int(cache_status) if cache_status not in ["None", None] else None

    return content, cache_hit


async def test_tc_async_stream(
    prompt: str, cache_control: str
):
    user_message = prompt

    completion, cache_hit = await call_RB(
        user_message, cache_control, True
    )

    if cache_hit is not None:
        print(f"Cache hit: {cache_hit}")

    print(completion)


async def test_tc_async(
    prompt: str,
    cache_control: str,
):
    user_message = prompt

    completion, cache_hit = await call_RB(
        user_message, cache_control, False
    )

    if cache_hit is not None:
        print(f"Cache hit: {cache_hit}")

    print(completion)

    # Assert response body
    assert isinstance(completion, dict)
    assert "choices" in completion
    assert len(completion["choices"]) > 0
    assert completion["choices"][0]["message"]

    print(completion["choices"][0]["message"]["content"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a prompt for completion.")
    parser.add_argument("--stream", action="store_true", help="Enable streaming")
    parser.add_argument(
        "--cache-control",
        choices=["no-cache", "no-store"],
        nargs="*",
        default=[],
        help="Set SemCache cache-control header",
    )
    
    args = parser.parse_args()

    # After parsing arguments:
    print("Please enter the prompt :")

    # Read prompt from standard input
    prompt = sys.stdin.readline().rstrip()

    if args.stream:
        asyncio.run(
            test_tc_async_stream(
                prompt,
                args.cache_control,
            )
        )
    else:
        asyncio.run(
            test_tc_async(
                prompt,
                args.cache_control,
            )
        )