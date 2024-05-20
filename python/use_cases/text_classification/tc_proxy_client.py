import argparse
import asyncio
import logging
import sys
from typing import List
import openai
from openai.types.chat import ChatCompletion
from decouple import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


openai_api_key = config("OPENAI_API_KEY")


async def test_tc_completion_async_stream(
    prompt: str, cache_control: str
    ):

    # Pass the cache control header, if provided
    cache_control_header = {}
    if cache_control:
        cache_control_header = {
            "Helvia-RAG-Buddy-Cache-Control": ", ".join(cache_control)
        }

    helvia_rag_cache_token = config("RAG_BUDDY_TOKEN")
    base_url = f"{config('PROXY_HOST', default='', cast=str)}/proxy/tc/{config('OPENAI_VERSION', default='', cast=str)}"

    headers = {"Helvia-RAG-Buddy-Token": helvia_rag_cache_token, **cache_control_header}
    
    client = openai.AsyncOpenAI(
        api_key=openai_api_key,
        base_url=base_url,
        timeout=10,
        default_headers=headers,
    )

    raw_response = await client.chat.completions.with_raw_response.create(
        messages=[
            {
                "role": "system",
            },
            {"role": "user", "content": prompt},
        ],
        model="gpt-4",
        temperature=0.0,
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
        chunk_text = chunk.choices[0].delta.content
        print(chunk_text)
        completion_text += chunk_text
    print(completion_text)
    print(raw_response.headers)

    if "Helvia-RAG-Buddy-Cache-Status" in raw_response.headers:
        cache_status = raw_response.headers["Helvia-RAG-Buddy-Cache-Status"]
        cache_hit = int(cache_status) if cache_status not in ["None", None] else None
        print(f"\nCache hit: {cache_hit}\n")

async def test_tc_completion_async(prompt: str, cache_control: str):
    # Pass the cache control header, if provided
    cache_control_header = {}
    if cache_control:
        cache_control_header = {
            "Helvia-RAG-Buddy-Cache-Control": ", ".join(cache_control)
        }


    helvia_rag_cache_token = config("RAG_BUDDY_TOKEN")
    base_url = f"{config('PROXY_HOST', default='', cast=str)}/proxy/tc/{config('OPENAI_VERSION', default='', cast=str)}"
    
    headers = {"Helvia-RAG-Buddy-Token": helvia_rag_cache_token, **cache_control_header}

    client = openai.AsyncOpenAI(
        api_key=openai_api_key,
        base_url=base_url,
        timeout=20,
        default_headers=headers,
    )

    raw_response: ChatCompletion = await client.chat.completions.with_raw_response.create(
        messages=[
            {
                "role": "system",
            },
            {"role": "user", "content": prompt},
        ],
        model="gpt-4",
        temperature=0.0,
        stream=False,
    )

    completion = raw_response.parse()

    # Assert response body
    assert isinstance(completion, ChatCompletion)
    assert len(completion.choices) > 0
    assert completion.choices[0].message
    print(completion.choices[0].message)
    print(completion.model_dump_json(indent=2))
    print(raw_response.headers)

    if "Helvia-RAG-Buddy-Cache-Status" in raw_response.headers:
        cache_status = raw_response.headers["Helvia-RAG-Buddy-Cache-Status"]
        cache_hit = int(cache_status) if cache_status not in ["None", None] else None
        print(f"\nCache hit: {cache_hit}\n")

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
            test_tc_completion_async_stream(
                prompt, args.cache_control
            )
        )
    else:
        asyncio.run(
            test_tc_completion_async(
                prompt, args.cache_control
            )
        )
