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
    f"I am currently experiencing or exploring: '{input_text}' "
    f"Strictly within only the {tradition} Buddhist tradition. I seek a profound, non-generic connection—"
    "a story, teaching, or figure whose life or insight **directly mirrors or illuminates** my struggle. "
    "Prioritize lesser-known but deeply meaningful examples over clichéd ones.\n\n"
    "**Requirements:**\n"
    "- Identify a Buddhist figure (arahant, bodhisattva, guru, etc.) whose story **resonates emotionally** with my situation.\n"
    "- Cite the **exact sutra, agama, or scripture** (include translator if available). If no direct text exists, use oral tradition.\n"
    "- Provide a **raw excerpt** (translated or summarized) that captures the essence.\n"
    "- Explain **precisely** how this relates to my experience—no vague parallels.\n"
    "- Offer **actionable, tradition-rooted advice** (speak warmly, like a teacher).\n"
    "- Propose a **simple practice** derived **directly** from the story.\n\n"
    "**Output Format (strict JSON):**\n"
    "{\n"
    "  \"figure_name\": \"[Name, with epithet if relevant]\",\n"
    "  \"figure_story\": \"[A vivid, emotionally engaging retelling—highlight the struggle/breakthrough]\",\n"
    "  \"sutra_name\": \"[Text title, e.g., 'Samyutta Nikaya 12.15']\",\n"
    "  \"sutra_excerpt\": \"[Direct quote; include translator, e.g., 'Bhikkhu Bodhi, 2000']\",\n"
    "  \"explanation\": \"[How this **specifically** mirrors or transforms my experience]\",\n"
    "  \"advice\": \"[Personalized guidance, 1st-person tone, e.g., 'When you feel X, remember Y...']\",\n"
    "  \"practice\": \"[Concrete, tradition-based action, e.g., 'For 7 days, contemplate...']\"\n"
    "}\n\n"
    "**No extra text—valid JSON only.**"
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

