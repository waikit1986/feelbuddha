import json
from fastapi import Depends
from sqlalchemy.orm.session import Session
from openai import AsyncOpenAI
# from openai import OpenAI

import os
from dotenv import load_dotenv
from .schema_ai import AiResponse
from reading.models_reading import Reading
from user.models_user import User
from user.functions_user import get_user_by_username


load_dotenv()

client = AsyncOpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def saveReading(tradition: str, input_text: str, response: AiResponse, total_tokens: int, user: User, db: Session):
    reading = Reading(
        tradition=tradition,
        input_text=input_text,
        sutra_name=response.sutra_name,
        sutra_excerpt=response.sutra_excerpt,
        saint=response.saint,
        advice=response.advice,
        practice=response.practice,
        total_tokens=total_tokens,
        user_id=user.id,
        username=user.username,
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading

async def getDeepSeekResponse(tradition: str, input_text: str, current_user: User, db: Session):

    prompt = (
    f"I am currently experiencing or exploring: {input_text}. Please guide me with clear, direct wisdom from the {tradition} Buddhist tradition to help me understand and transform this situation. "
    f"Do not give general spiritual advice—only draw from canonical {tradition} texts that speak specifically to this issue. "
    "Reply in valid JSON format with the following keys only:\n\n"
    "1. \"saint\": [A named Buddhist saint, arhat, or bodhisattva from a canonical {tradition} text, whose story relates to this issue.]\n"
    "2. \"sutra_name\": [Exact name of the sutra, tantra, or text where this figure appears and which addresses the situation. Must be canonical.]\n"
    "3. \"sutra_excerpt\": [Direct quote from the text related to the issue. Include English translation source if available.]\n"
    "4. \"advice\": [Explain the quote clearly. Show how it applies to my situation. Then, tell the saint’s story from the text: what happened, what they realized, and how it relates to my struggle. Tone should be warm and wise, like a teacher.]\n"
    "5. \"practice\": [A beginner-friendly daily {tradition} practice from this saint or sutra—such as a mantra, visualization, or reflection—directly aimed at this issue.]\n\n"
    "Requirements:\n"
    "- The saint must be explicitly present in the cited sutra.\n"
    "- The excerpt must clearly mention the emotion or issue.\n"
    "- The practice must come from the sutra or saint, not improvised.\n"
    "- Use first-person tone, as if a teacher or Buddha were speaking to me.\n\n"
    "Output valid JSON only, with double quotes and no extra text."
)

    print(prompt)

    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        # max_tokens=2048,
        temperature=1.7,
        stream=False
    )
    
    raw_output = response.choices[0].message.content
    parsed_output = json.loads(raw_output)
    print(parsed_output)

    user = get_user_by_username(db, current_user.username)
    saveReading(
        tradition=tradition,
        input_text=input_text,
        response=AiResponse(**parsed_output),
        total_tokens=response.usage.total_tokens,
        user=user,
        db=db
    )

    return AiResponse(
        sutra_name=parsed_output["sutra_name"],
        sutra_excerpt=parsed_output["sutra_excerpt"],
        saint=parsed_output["saint"],
        advice=parsed_output["advice"],
        practice=parsed_output["practice"],
    )

