# import json
# from openai import OpenAI

# client = OpenAI(
#     api_key=os.environ.get("DEEPSEEK_API_KEY"),
#     base_url="https://api.deepseek.com"
# )

# def getDeepSeekResponse(card: str, situation: str):
    
#     prompt = f"The tarot card is {card}, and the situation is {situation}. Reply in JSON with fields 'emotion' (use only EARL label to determine user's emotion) and 'answer' (plain paragraph). Interpret the card in the context of situation. Based on card visual symbolism and meaning, suggest mental improvements."
    
#     print(prompt)

#     messages = [{
#         "role": "user",
#         "content": prompt
#     }]
    
#     response = client.chat.completions.create(
#         model="deepseek-reasoner",
#         messages=messages,
#         # stream=True,
#         max_tokens=1000,
#         temperature=1.5,
#     )
    
#     content = response.choices[0].message.content
#     data = json.loads(content)

#     emotion = data["emotion"]
#     answer = data["answer"]
#     tokens = response.usage.total_tokens
    
#     print(f"Emotion: {emotion}")
#     print(f"Answer: {answer}")
#     print(f"Tokens used: {tokens}")

#     return {
#         "emotion": emotion,
#         "answer": answer,
#         "tokens": tokens
#     }

# getDeepSeekResponse("two of wands", "I think my bf cheat on me")

from openai import OpenAI
import json

import os
from dotenv import load_dotenv
from .schema_ai import AiResponse


load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

EARL_48 = [
    "admiration",
    "adoration",
    "aesthetic appreciation",
    "amusement",
    "anger",
    "anxiety",
    "awe",
    "awkwardness",
    "boredom",
    "calmness",
    "confusion",
    "craving",
    "disgust",
    "empathetic pain",
    "entrancement",
    "envy",
    "excitement",
    "fear",
    "gratitude",
    "guilt",
    "horror",
    "interest",
    "joy",
    "love",
    "nostalgia",
    "pride",
    "realization",
    "relief",
    "remorse",
    "romantic love",
    "sadness",
    "satisfaction",
    "sexual desire",
    "surprise (positive)",
    "surprise (negative)",
    "sympathy",
    "tiredness",
    "triumph",
    "awkward amusement",
    "confident amusement",
    "compassionate sympathy",
    "disappointed relief",
    "fearful horror",
    "loving admiration",
    "proud joy",
    "relieved surprise",
    "sad nostalgia",
    "suspicious anxiety"
]

def getGptResponse(card: str, situation: str) -> AiResponse:
    emotions_str = ", ".join(f'"{e}"' for e in EARL_48)
    prompt = (
        f"The tarot card is {card} and the situation is {situation}. "
        f"Reply in JSON with 'emotion' (choose exactly one from this list only: {emotions_str}) and 'answer' (a plain paragraph). "
        "Interpret the card's symbolism in this context and suggest improvements."
    )

    response = client.responses.create(
    model="gpt-4.1",
    input=prompt,
    )
    
    # response = client.responses.create(
    # model="o4-mini",
    # reasoning={"effort": "medium"},
    # input=[
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #     ],
    #     max_output_tokens=1000,
    # )

    raw_output = response.output_text
    parsed_output = json.loads(raw_output)

    return AiResponse(
        emotion=parsed_output["emotion"],
        answer=parsed_output["answer"],
        tokens=response.usage.total_tokens
    )
