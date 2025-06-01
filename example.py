from openai import OpenAI
import json

import os
from dotenv import load_dotenv
from ai.schema_ai import AiResponse


load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def getGptResponse(card: str, situation: str) -> AiResponse:
    prompt = (
        f"The tarot card is {card}, and the situation is {situation}. "
        "Reply in JSON with fields 'emotion' (use only EARL label to determine user's emotion) and 'answer' (plain paragraph). "
        "Interpret the card in the context of situation. Solely on card visual symbolism and meaning, suggest improvements."
    )

    response = client.responses.create(
    model="gpt-4.1",
    input=prompt,
    )

    print(response.output_text)
    
getGptResponse("The Fool", "I am starting a new job and feeling anxious about it.")

# import os
# from dotenv import load_dotenv
# from openai import OpenAI
# from pydantic import BaseModel
# import json

# load_dotenv()

# client = OpenAI(
#     api_key=os.environ.get("OPENAI_API_KEY"),
# )

# class TarotResponse(BaseModel):
#     emotion: str
#     answer: str

# card="two of wands"
# situation="I think my bf cheat on me"
# prompt = f"The tarot card is {card}, and the situation is {situation}. Reply in JSON with fields 'emotion' (use only EARL label to determine user's emotion) and 'answer' (plain paragraph). Interpret the card in the context of situation. Based on card visual symbolism and meaning, suggest mental improvements."

# response = client.responses.create(
#     model="o4-mini",
#     reasoning={"effort": "medium"},
#     input=[
#         {
#             "role": "user",
#             "content": prompt
#         }
#     ]
# )

# raw_json_str = response.output[1].content[0].text
# data = json.loads(raw_json_str)

# print(data["emotion"])
# print(data["answer"])
# print(response.usage)


# import json
# from openai import OpenAI

# client = OpenAI(
#     api_key="sk-d17b9c864d5142078040a4469e296b46",
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