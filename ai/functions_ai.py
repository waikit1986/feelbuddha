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

async def getDeepSeekResponse(tradition: str, input_text: str, current_user: User, db: Session):

    prompt = (
        f"I'm feeling {input_text}. Guide me with wisdom from the {tradition} Buddhist tradition—help me understand this emotion and transform it with compassion and insight. "  
        f"Select a sutra or teaching that *directly* speaks to my current state, not just generally. "  
        f"Find a passage that feels like it was written for this moment, and tell me: "  
        f"1. The **exact sutra name** and a **powerful, resonant excerpt** (cite a reliable source). "  
        f"2. A **Buddhist saint, arhat, or bodhisattva** whose life story or vows mirror my struggle or offer inspiration. "  
        f"3. A **deep, personal explanation** of how this teaching applies—not just a generic interpretation, but how it speaks to *this specific emotion*. "  
        f"4. **Practical advice**—a small but meaningful daily practice (e.g., a mantra, reflection, or meditation) to work with this feeling. "  
        f"Respond in **JSON format** with these keys: "  
        f"'sutra_name' (be precise), "  
        f"'sutra_excerpt' (include the exact words and source), "  
        f"'saint' (name and why they’re relevant), "  
        f"'explanation' (detailed, empathetic, and tailored to my emotion), "  
        f"'advice' (something actionable, even for beginners). "  
        f"Structure it like this: "  
        f"{{'sutra_name': '', 'sutra_excerpt': '', 'saint': '', 'explanation': '', 'advice': ''}}. "  
        f"**Important**: Make it feel personal—like the Buddha or a great teacher is speaking directly to me."  
    )

    print(prompt)

    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        max_tokens=1024,
        temperature=1.7,
        stream=False
    )
    
    raw_output = response.choices[0].message.content
    parsed_output = json.loads(raw_output)
    print(parsed_output)

    user = get_user_by_username(db, current_user.username)

    return AiResponse(
        sutra_name=parsed_output["sutra_name"],
        sutra_excerpt=parsed_output["sutra_excerpt"],
        explanation=parsed_output["explanation"],
        saint=parsed_output["saint"],
        advice=parsed_output["advice"],
    )

