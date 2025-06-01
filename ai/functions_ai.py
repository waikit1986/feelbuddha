from openai import OpenAI
import json

import os
from dotenv import load_dotenv
from .schema_ai import AiResponse


load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def getGptResponse(card: str, situation: str) -> AiResponse:
    prompt = (
        f"The tarot card is {card}, and the situation is {situation}. "
        "Reply in JSON with fields 'emotion' (use only HUMAINE's EARL 48 emotions to determine user's emotion) and 'answer' (plain paragraph). "
        "Interpret the card in the context of situation. Solely on card visual symbolism and meaning, suggest improvements."
    )

    response = client.responses.create(
    model="gpt-4.1",
    input=prompt,
    )

    raw_output = response.output_text
    parsed_output = json.loads(raw_output)

    return AiResponse(
        emotion=parsed_output["emotion"],
        answer=parsed_output["answer"],
        tokens=response.usage.total_tokens
    )

# getGptResponse("The Fool", "I am starting a new job and feeling anxious about it.")

#     # response = client.responses.create(
#     #     model="o4-mini",
#     #     reasoning={"effort": "medium"},
#     #     input=[
#     #         {
#     #             "role": "user",
#     #             "content": prompt
#     #         }
#     #     ],
#     #     max_output_tokens=1000,
#     # )

#     # raw_json_str = response.output[1].content[0].text
#     # data = json.loads(raw_json_str)

#     # print(response.usage)
#     # print(data["emotion"])
#     # print(data["answer"])
#     # return AiResponse(emotion=data["emotion"], answer=data["answer"], tokens=response.usage.total_tokens)

