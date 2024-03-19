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
    system_instructions: str,
    classes: List[str],
    user_message: str,
    **kwargs: Any,
) -> Tuple[Any, Dict[str, str]]:
    # Base payload
    payload = {
        "remote_llm_url": remote_llm_url,
        "system_instructions": system_instructions,
        "classes": classes,
        "user_message": user_message,
    }

    # Add extra keyword arguments to the payload
    payload.update(kwargs)

    api_url = "https://api.ragbuddy.ai/tc/v1"

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
    system_instructions, classes, user_message, cache_control, stream
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
        system_instructions,
        classes,
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
    prompt: str, system_instructions: str, classes: List, cache_control: str
):
    user_message = prompt

    completion, cache_hit = await call_RB(
        system_instructions, classes, user_message, cache_control, True
    )

    if cache_hit is not None:
        print(f"Cache hit: {cache_hit}")

    print(completion)


async def test_tc_async(
    prompt: str,
    system_instructions: str,
    classes: List,
    cache_control: str,
):
    user_message = prompt

    completion, cache_hit = await call_RB(
        system_instructions, classes, user_message, cache_control, False
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

    system_instructions = """You are an expert assistant in the field of customer service. Your task is to help workers in the customer service department of a company.\nYour task is to classify the customer's question in order to help the customer service worker to answer the question. In order to help the worker, you MUST respond with the name of one of the following classes you know.\nIn case you reply with something else, you will be penalized.\nThe classes are the following:"""
    classes = [
        "activate_my_card",
        "age_limit",
        "apple_pay_or_google_pay",
        "atm_support",
        "automatic_top_up",
        "balance_not_updated_after_bank_transfer",
        "balance_not_updated_after_cheque_or_cash_deposit",
        "beneficiary_not_allowed",
        "cancel_transfer",
        "card_about_to_expire",
        "card_acceptance",
        "card_arrival",
        "card_delivery_estimate",
        "card_linking",
        "card_not_working",
        "card_payment_fee_charged",
        "card_payment_not_recognised",
        "card_payment_wrong_exchange_rate",
        "card_swallowed",
        "cash_withdrawal_charge",
        "cash_withdrawal_not_recognised",
        "change_pin",
        "compromised_card",
        "contactless_not_working",
        "country_support",
        "declined_card_payment",
        "declined_cash_withdrawal",
        "declined_transfer",
        "direct_debit_payment_not_recognised",
        "disposable_card_limits",
        "edit_personal_details",
        "exchange_charge",
        "exchange_rate",
        "exchange_via_app",
        "extra_charge_on_statement",
        "failed_transfer",
        "fiat_currency_support",
        "get_disposable_virtual_card",
        "get_physical_card",
        "getting_spare_card",
        "getting_virtual_card",
        "lost_or_stolen_card",
        "lost_or_stolen_phone",
        "order_physical_card",
        "passcode_forgotten",
        "pending_card_payment",
        "pending_cash_withdrawal",
        "pending_top_up",
        "pending_transfer",
        "pin_blocked",
        "receiving_money",
        "Refund_not_showing_up",
        "request_refund",
        "reverted_card_payment?",
        "supported_cards_and_currencies",
        "terminate_account",
        "top_up_by_bank_transfer_charge",
        "top_up_by_card_charge",
        "top_up_by_cash_or_cheque",
        "top_up_failed",
        "top_up_limits",
        "top_up_reverted",
        "topping_up_by_card",
        "transaction_charged_twice",
        "transfer_fee_charged",
        "transfer_into_account",
        "transfer_not_received_by_recipient",
        "transfer_timing",
        "unable_to_verify_identity",
        "verify_my_identity",
        "verify_source_of_funds",
        "verify_top_up",
        "virtual_card_not_working",
        "visa_or_mastercard",
        "why_verify_identity",
        "wrong_amount_of_cash_received",
        "wrong_exchange_rate_for_cash_withdrawal",
    ]

    if args.stream:
        asyncio.run(
            test_tc_async_stream(
                prompt,
                system_instructions,
                classes,
                args.cache_control,
            )
        )
    else:
        asyncio.run(
            test_tc_async(
                prompt,
                system_instructions,
                classes,
                args.cache_control,
            )
        )