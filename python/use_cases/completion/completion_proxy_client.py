import argparse
import asyncio
import sys
import openai
from openai.types import Completion
from openai.types.chat import ChatCompletion
from decouple import config

openai_api_key = config("OPENAI_API_KEY")
helvia_rag_cache_token = config("RAG_BUDDY_TOKEN")
base_url = f"{config('PROXY_HOST', default='', cast=str)}/proxy/sem/{config('OPENAI_VERSION', default='', cast=str)}"


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


    raw_response: ChatCompletion = await client.chat.completions.with_raw_response.create(
        prompt=prompt,
        model="gpt-4o",
        stream=True,
    )

    stream = raw_response.parse()

    # Assert response body
    assert isinstance(stream, openai.AsyncStream)
    
    collected_chunks = []
    completion_text = ""
    # iterate through the stream, if it breaks, the test failed
    print("\n")
    async for chunk in stream:
        collected_chunks.append(chunk)
        finish_reason = chunk.choices[0].finish_reason
        if finish_reason is not None:
            break
        chunk_text = chunk.choices[0].text
        print(chunk_text)
        completion_text += chunk_text
    print("\n")
    print(raw_response.headers)

    if "Helvia-RAG-Buddy-Cache-Status" in raw_response.headers:
        cache_status = raw_response.headers["Helvia-RAG-Buddy-Cache-Status"]
        cache_hit = int(cache_status) if cache_status not in ["None", None] else None
        print(f"Cache hit: {cache_hit}")

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

    raw_response = await client.chat.completions.with_raw_response.create(
        messages=[            
            {"role": "user", "content": prompt
             },
        ],
        model="gpt-4o",
        stream=False
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
        print(f"Cache hit: {cache_hit}")

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