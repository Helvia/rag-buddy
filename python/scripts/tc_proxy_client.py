import argparse
import asyncio
import sys
from typing import List
import openai
from openai.types.chat import ChatCompletion
from decouple import config
from ..utils.tc_templates import default_tc_template



openai_api_key = config("OPENAI_API_KEY")


async def test_tc_completion_async_stream(
    prompt: str, system_instructions: str, classes: List, cache_control: str, api: str
    ):

    # Pass the cache control header, if provided
    cache_control_header = {}
    if cache_control:
        cache_control_header = {
            "Helvia-RAG-Buddy-Cache-Control": ", ".join(cache_control)
        }

    helvia_rag_cache_token = config("RAG_BUDDY_KEY")
    base_url = "https://api.ragbuddy.ai/proxy/tc/v1"

    headers = {"Helvia-RAG-Buddy-Token": helvia_rag_cache_token, **cache_control_header}

    classes_string = "\n".join(classes)
    system_content = default_tc_template.format(
        system_instructions=system_instructions,
        classes=f"####\n{classes_string}\n####",
    )
    
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
                "content": system_content,
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
        print(f"Cache hit: {cache_hit}")

async def test_tc_completion_async(prompt: str, system_instructions: str, classes: List,  cache_control: str, api: str):
    # Pass the cache control header, if provided
    cache_control_header = {}
    if cache_control:
        cache_control_header = {
            "Helvia-RAG-Buddy-Cache-Control": ", ".join(cache_control)
        }


    helvia_rag_cache_token = config("RAG_BUDDY_KEY")
    base_url = "https://api.ragbuddy.ai/proxy/tc/v1"
    
    headers = {"Helvia-RAG-Buddy-Token": helvia_rag_cache_token, **cache_control_header}

    classes_string = "\n".join(classes)
    system_content = default_tc_template.format(
        system_instructions=system_instructions,
        classes=f"####\n{classes_string}\n####",
    )

    client = openai.AsyncOpenAI(
        api_key=openai_api_key,
        base_url=base_url,
        timeout=20,
        default_headers=headers,
    )

    raw_response = await client.chat.completions.with_raw_response.create(
        messages=[
            {
                "role": "system",
                "content": system_content,
            },
            {"role": "user", "content": prompt},
        ],
        model="gpt-4",
        temperature=0.0,
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
    parser.add_argument("--stream", action="store_true", help="Enable streaming")
    parser.add_argument(
        "--cache-control",
        choices=["no-cache", "no-store"],
        nargs="*",
        default=[],
        help="Set SemCache cache-control header",
    )
    parser.add_argument(
        "--api",
        choices=["local", "dev", "prod"],
        default="local",
        help="Select the API host environment (local, dev, prod)",
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
            test_tc_completion_async_stream(
               prompt, system_instructions, classes, args.cache_control, args.api
            )
        )
    else:
        asyncio.run(
            test_tc_completion_async(
                prompt, system_instructions, classes, args.cache_control, args.api
            )
        )