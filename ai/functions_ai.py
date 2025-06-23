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
        figure_name=response.figure_name,
        figure_story=response.figure_story,
        sutra_name=response.sutra_name,
        sutra_excerpt=response.sutra_excerpt,
        explanation=response.explanation,
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
    f"I am currently experiencing or exploring: {input_text} "
    f"within the {tradition} Buddhist tradition that relates to, reflects, or speaks to my situation. This could be about an "
    "arahant, bodhisattva, guru, yogi, or renowned monk—someone whose life, struggle, or insight might "
    "mirror or transform this experience. You may go beyond the most famous figures and include "
    "lesser-known but meaningful examples.\n\n"
    "If possible, identify the associated sutra, agama, scripture, koan, or oral tradition that features "
    "this figure or moment, and include a direct excerpt. If no exact match exists, search across the "
    "broader Buddhist canon to find the most resonant teaching.\n\n"
    "Reply in valid JSON format with the following keys only:\n\n"
    "1. \"figure_name\": [Name of the Buddhist figure whose story relates to this issue]\n"
    "2. \"figure_story\": [A personal retelling of their relevant story, emphasizing emotional resonance to me]\n"
    "3. \"sutra_name\": [Name of the text where this appears (or 'Oral Tradition' if not canonical)]\n"
    "4. \"sutra_excerpt\": [Direct quote or summary of key teaching from the text, provide the source if available]\n"
    "5. \"explanation\": [How this story specifically relates to my current situation]\n"
    "6. \"advice\": [Personalized guidance drawn from this story, in a warm, teacher-like tone]\n"
    "7. \"practice\": [A simple, actionable practice derived from this story]\n\n"
    "Requirements:\n"
    "- The story should feel personally relevant to my experience\n"
    "- Include source text when possible, but oral traditions are acceptable\n"
    "- The practice should be genuinely derived from the tradition\n"
    "- Use first-person tone in advice, as if speaking directly to me\n\n"
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
        figure_name=parsed_output["figure_name"],
        figure_story=parsed_output["figure_story"],
        sutra_name=parsed_output["sutra_name"],
        sutra_excerpt=parsed_output["sutra_excerpt"],
        explanation=parsed_output["explanation"],
        advice=parsed_output["advice"],
        practice=parsed_output["practice"],
    )

