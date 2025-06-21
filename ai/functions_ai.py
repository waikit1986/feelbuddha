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
    f"I'm feeling {input_text}. Guide me with precise Buddhist wisdom from the {tradition} tradition to deeply understand and transform this emotion. "
    f"Carefully select teachings that directly address my specific situation—not general advice. "
    f"Respond in JSON format with these keys: "
    f"1. 'sutra_name' – [Search across all Buddhist scriptures to find the most relevant sutra that directly addresses this emotion or situation. Provide the exact name.] "
    f"2. 'sutra_excerpt' – [A powerful 1-3 sentence passage from this sutra that feels written for this moment. Include translation source.] "
    f"3. 'saint' – [A Buddhist saint, arhat or bodhisattva whose life story perfectly mirrors this struggle.] "
    f"4. 'advice' – [in a paragraph and in detail, without the numbering. 1. Explain the sutra meaning. 2. How the sutra applies to me. 3. Tell me the saint story in details. 4. How this story relates to me.] "
    f"5. 'practice' – [A concrete, beginner-friendly daily practice (mantra, meditation or reflection) designed specifically for working with '{input_text}'.] "
    f"Tone: Write as if the Buddha or my personal teacher is speaking just to me—warm, compassionate, and profoundly insightful. "
    )

    print(prompt)

    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        max_tokens=2048,
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

