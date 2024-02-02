import argparse
import asyncio
import sys
import openai
from openai.types import Completion
from decouple import config

helvia_rag_cache_token = config("RAG_BUDDY_KEY")
base_url = config("PROXY_URL")
openai_api_key = config("OPENAI_API_KEY")

async def test_completion_async_stream(prompt: str, cache_control: str):
    # Pass the cache control header, if provided
    cache_control_header = {}
    if cache_control:
        cache_control_header = {
            "Helvia-RAG-Buddy-Cache-Control": ", ".join(cache_control)
        }

    headers = {"Helvia-RAG-Buddy-Token": helvia_rag_cache_token, **cache_control_header}

    client = openai.AsyncOpenAI(
        api_key=openai_api_key,
        base_url=base_url,
        timeout=10,
        default_headers=headers,
    )

    raw_response = await client.completions.with_raw_response.create(
        prompt=prompt,
        model="gpt-3.5-turbo-instruct",
        stream=True,
    )

    stream = raw_response.parse()

    # Assert response body
    assert isinstance(stream, openai.AsyncStream)
    
    collected_chunks = []
    completion_text = ""
    # iterate through the stream, if it breaks, the test failed
    async for chunk in stream:
        collected_chunks.append(chunk)
        finish_reason = chunk.choices[0].finish_reason
        if finish_reason is not None:
            break
        chunk_text = chunk.choices[0].text
        print("\n")
        print(chunk_text)
        completion_text += chunk_text
    print(raw_response.headers)

async def test_completion_async(prompt: str, cache_control: str):
    # Pass the cache control header, if provided
    cache_control_header = {}
    if cache_control:
        cache_control_header = {
            "Helvia-RAG-Buddy-Cache-Control": ", ".join(cache_control)
        }

    headers = {
        "Helvia-RAG-Buddy-Token": helvia_rag_cache_token,
        **cache_control_header,
    }

    client = openai.AsyncOpenAI(
        api_key=openai_api_key,
        base_url=base_url,
        timeout=10,
        default_headers=headers,
    )

    raw_response = await client.completions.with_raw_response.create(
        prompt=prompt,
        model="gpt-3.5-turbo-instruct",
    )

    completion = raw_response.parse()

    # Assert response body
    assert isinstance(completion, Completion)
    assert len(completion.choices) > 0
    assert completion.choices[0].text
    print(completion.choices[0].text)
    print(completion.model_dump_json(indent=2))
    print(raw_response.headers)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a prompt for completion.")

    parser.add_argument(
        "--stream", action="store_true", help="Enable streaming completion"
    )
    parser.add_argument(
        "--cache-control",
        choices=["no-cache", "no-store"],
        nargs="*",
        default=[],
        help="Set SemCache cache-control header",
    )

    args = parser.parse_args()

    # After parsing arguments:
    print("Please enter the prompt you want to complete:")

    # Read prompt from standard input
    prompt = sys.stdin.readline().rstrip()

    if args.stream:
        asyncio.run(test_completion_async_stream(prompt, args.cache_control))
    else:
        asyncio.run(test_completion_async(prompt, args.cache_control))