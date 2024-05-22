import openai
from decouple import config


# Your OpenAI API key
openai_api_key = config('OPENAI_API_KEY', default='', cast=str) # Replace with your actual API key

# Your RAG Buddy key
rag_buddy_key = config('RAG_BUDDY_TOKEN', default='', cast=str) # Replace with your actual RAG Buddy key
# Needed for RAG Cache integration
base_url = f"{config('PROXY_HOST', default='', cast=str)}/proxy/ragc/{config('OPENAI_VERSION', default='', cast=str)}"
headers = {"Helvia-RAG-Buddy-Token": rag_buddy_key}

# System messages
system_intro = "You are a customer support agent of the e-banking application called Piggy Bank Extraordinaire."
system_instructions = """Select the best article to reply to the question of the user below.
If you can find the answer in the articles listed below, then:
You MUST select exactly one article from the listed articles.
You MUST add the ID of the selected article at the start of your answer in the format "(ID:number) your answer", For example: (ID:1) your answer.
You MUST provide a short summarized answer.
If you cannot find the answer in the list of articles below, then:
You MUST say "(ID:None) I cannot answer this" and MUST say nothing more.
"""

# Articles
chosen_articles = """
## ID:123e4567-e89b-12d3-a456-426655440000    Interest Rates on Piggy Bank Extraordinaire's Savings Accounts
At Piggy Bank Extraordinaire, we understand the importance of saving for your future. That's why our Gold Plus Savings Account offers a competitive interest rate of 2.6% per annum, ensuring your savings grow steadily over time. For those seeking more flexibility, our Silver Flexi Savings Account provides an interest rate of 1.8% per annum, with the added benefit of no minimum balance requirement. Our Bronze Everyday Savings Account is perfect for daily transactions, offering a 1.2% interest rate per annum. With Piggy Bank Extraordinaire, you can choose the savings account that best suits your financial goals and lifestyle.

## ID:123e4567-e89b-12d3-a456-426655440001    Comparing Interest Rates: Piggy Bank Extraordinaire vs. Other Banks
When it comes to choosing a bank for your savings, interest rates play a crucial role. Piggy Bank Extraordinaire stands out with its competitive rates. Our Gold Plus Savings Account offers an interest rate of 2.6% per annum, significantly higher than the industry average of 2.0%. In comparison, Big Bank offers 2.2% on its equivalent account, and Global Trust offers 2.1%. Furthermore, Piggy Bank Extraordinaire's Silver Flexi and Bronze Everyday accounts also outperform their counterparts at other banks, offering higher returns on your deposits. With Piggy Bank Extraordinaire, you can be assured of getting one of the best rates in the market for your savings.

## ID:123e4567-e89b-12d3-a456-426655440002    Understanding Fixed Deposit Interest Rates at Piggy Bank Extraordinaire
Fixed Deposits at Piggy Bank Extraordinaire are an excellent way to earn higher interest on your savings. Our Fixed Deposit accounts offer various tenures ranging from 6 months to 5 years, with interest rates varying accordingly. For a 6-month deposit, enjoy an interest rate of 2.0% per annum. The rate increases to 2.5% for a 1-year term and peaks at 3.5% for a 5-year term. These rates are designed to reward longer commitments with higher returns. Our Fixed Deposits are perfect for customers who wish to lock in their savings for a fixed period to earn a guaranteed return without the risks associated with market fluctuations.
"""

# User query (can be replaced with any relevant question)
user_query = "What are the interest rates for the Gold Plus Savings Account?"

# Format the template
template = f"{system_intro}\n\nINSTRUCTIONS:\n{system_instructions}\n\nARTICLES:\n{chosen_articles}\n\n"

# Initialize OpenAI client
client = openai.OpenAI(
    api_key=openai_api_key,
    timeout=10,
    default_headers=headers,
    base_url=base_url
)

# Prepare the messages
messages = [
    {
        "role": "system",
        "content": template,
    },
    {"role": "user", "content": user_query},
]

# Call OpenAI API
raw_response = client.chat.completions.with_raw_response.create(
    model="gpt-3.5-turbo",  # Replace with the specific model name
    messages=messages,
)
completion = raw_response.parse()


# Read the response
print(completion.choices[0].message)
print(completion.model_dump_json(indent=2))
print(raw_response.headers)
if "Helvia-RAG-Buddy-Cache-Status" in raw_response.headers:
        cache_status = raw_response.headers["Helvia-RAG-Buddy-Cache-Status"]
        cache_hit = int(cache_status) if cache_status not in ["None", None] else None
        print(f"Cache hit: {cache_hit}")
