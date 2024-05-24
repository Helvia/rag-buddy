default_ragc_instructions = """Select the best article to reply to the question of the user below.
If you can find the answer in the articles listed below, then:
You MUST select exactly one article from the listed articles.
You MUST add the ID of the selected article at the start of your answer in the format "(ID:number) your answer", For example: (ID:1) your answer.
You MUST provide a short summarized answer.
If you cannot find the answer in the list of articles below, then:
You MUST say "(ID:None) I cannot answer this" and MUST say nothing more.
"""

default_ragc_template = """{system_intro}
 
INSTRUCTIONS:
{system_instructions}

ARTICLES:
{articles}
"""
# The articles for the default template follow the format of articles2 below


""" Three scenarios:
1. The template instructions are correct, they include instructions to pick a winner and return the ID in the response. The articles have ID's of the form 1, 2, 3...
2. The template instructions are correct, they include instructions to pick a winner and return the ID in the response. The articles have ID's of the form longer strings or numbers.
3. The template instruction doesn't include instructions to pick a winner and return the ID in the response. The articles have no ID's, just separators.
"""

template1 = """
You are a customer support agent of the e-banking application called Piggy Bank Extraordinaire.

INSTRUCTIONS:
Select the best article to reply to the question of the user below.
If you can find the answer in the articles listed below, then:
You MUST select exactly one article from the listed articles.
You MUST add the ID of the selected article at the start of your answer in the format "(ID:number) your answer", For example: (ID:1) your answer.
You MUST provide a short summarized answer.
If you cannot find the answer in the list of articles below, then:
You MUST say "(ID:None) I cannot answer this" and MUST say nothing more.

ARTICLES:
{articles1}
"""

articles1 = """
## ID:1    I've lost my card. What should I do?
You can always freeze your card directly from the app!
Just follow the next steps:
1️⃣ Choose the card you lost from the available cards
2️⃣ Tap on the ""Freeze"" button.
3️⃣ Once you are sure that your card is lost, tap on the ""Lost"" button and deactivate your card.

## ID:2    Card menu
card

## ID:3    How can I change my card's PIN?
You can reset your card's PIN by following the next steps:

1️⃣ Choose the card you need
2️⃣ Tap on “Settings” button 
3️⃣ Choose "Manage your PIN"
4️⃣ Choose "Reset your PIN"

## ID:4    My card has expired, what should I do?
In this case, the card will have to be reissued. Would you like me to connect you with a member of our team to complete the process? 👨‍🚀

## ID:5    I want a physical card, how can I receive it?
💳 You can request a physical card at any time, through the app. 
1. Log in to your account → Cards → New Card.
2. Tap Request for Card.
3. Follow the process that will appear on your screen.

That's it! Your physical card will be in your hands within 15 working days.
"""


template2 = """
You are a customer support agent of the e-banking application called Piggy Bank Extraordinaire.

INSTRUCTIONS:
Select the best article to reply to the question of the user below.
If you can find the answer in the articles listed below, then:
You MUST select exactly one article from the listed articles.
You MUST add the ID of the selected article at the start of your answer in the format "(ID:number) your answer", For example: (ID:1) your answer.
You MUST provide a short summarized answer.
If you cannot find the answer in the list of articles below, then:
You MUST say "(ID:None) I cannot answer this" and MUST say nothing more.

ARTICLES:
{articles2}
"""

articles2 = """
## ID:UUID1    I've lost my card. What should I do?
You can always freeze your card directly from the app!
Just follow the next steps:
1️⃣ Choose the card you lost from the available cards
2️⃣ Tap on the ""Freeze"" button.
3️⃣ Once you are sure that your card is lost, tap on the ""Lost"" button and deactivate your card.

## ID:UUID2    Card menu
card

## ID:UUID3    How can I change my card's PIN?
You can reset your card's PIN by following the next steps:

1️⃣ Choose the card you need
2️⃣ Tap on “Settings” button 
3️⃣ Choose "Manage your PIN"
4️⃣ Choose "Reset your PIN"

## ID:UUID4    My card has expired, what should I do?
In this case, the card will have to be reissued. Would you like me to connect you with a member of our team to complete the process? 👨‍🚀

## ID:UUID5    I want a physical card, how can I receive it?
💳 You can request a physical card at any time, through the app. 
1. Log in to your account → Cards → New Card.
2. Tap Request for Card.
3. Follow the process that will appear on your screen.

That's it! Your physical card will be in your hands within 15 working days.
"""


template3 = """
You are a customer support agent of the e-banking application called Piggy Bank Extraordinaire.

INSTRUCTIONS:
Select the best article to reply to the question of the user below.
If you can find the answer in the articles listed below, then:
You MUST select exactly one article from the listed articles.
You MUST add the ID of the selected article at the start of your answer in the format "(ID:number) your answer", For example: (ID:1) your answer.
You MUST provide a short summarized answer.
If you cannot find the answer in the list of articles below, then:
You MUST say "(ID:None) I cannot answer this" and MUST say nothing more.

ARTICLES:
{articles3}
"""

articles3 = """
I've lost my card. What should I do?
You can always freeze your card directly from the app!
Just follow the next steps:
1️⃣ Choose the card you lost from the available cards
2️⃣ Tap on the ""Freeze"" button.
3️⃣ Once you are sure that your card is lost, tap on the ""Lost"" button and deactivate your card.

Card Menu
####
card
####
How can I change my card's PIN?
You can reset your card's PIN by following the next steps:

1️⃣ Choose the card you need
2️⃣ Tap on “Settings” button 
3️⃣ Choose "Manage your PIN"
4️⃣ Choose "Reset your PIN"

We will make a quick check to confirm your identity, and once it is completed you have a new PIN!✌️
####
My card has expired, what should I do? 
In this case, the card will have to be reissued. Would you like me to connect you with a member of our team to complete the process? 👨‍🚀
####
I want a physical card, how can I receive it?
💳 You can request a physical card at any time, through the app. 
1. Log in to your account → Cards → New Card.
2. Tap Request for Card.
3. Follow the process that will appear on your screen.

That's it! Your physical card will be in your hands within 15 working days.
"""
