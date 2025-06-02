import json
from fastapi import Depends
from sqlalchemy.orm.session import Session
from openai import OpenAI

import os
from dotenv import load_dotenv
from .schema_ai import AiResponse
from .models_ai import Reading
from user.models_user import User
from user.functions_user import get_user_by_username


load_dotenv()

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

EMOTIONS = {
    "Negative and forceful": ["Anger", "Annoyance", "Contempt", "Disgust", "Irritation"],
    "Negative and not in control": ["Anxiety", "Embarrassment", "Fear", "Helplessness", "Powerlessness", "Worry"],
    "Negative thoughts": ["Doubt", "Envy", "Frustration", "Guilt", "Shame"],
    "Negative and passive": ["Boredom", "Despair", "Disappointment", "Hurt", "Sadness", "Agitation", "Stress", "Shock", "Tension"],
    "Positive and lively": ["Amusement", "Delight", "Elation", "Excitement", "Happiness", "Joy", "Pleasure"],
    "Caring": ["Affection", "Empathy", "Friendliness", "Love"],
    "Positive thoughts": ["Pride", "Courage", "Hope", "Humility", "Satisfaction", "Trust"],
    "Quiet positive": ["Calmness", "Contentment", "Relaxation", "Relief", "Serenity"],
    "Reactive": ["Interest", "Politeness", "Surprise"]
}

def saveReading(card: str, situation: str, response: AiResponse, total_tokens: int,user: User, db: Session):
    reading = Reading(
        card=card,
        situation=situation,
        emotion=response.emotion,
        answer=response.answer,
        total_tokens=total_tokens,
        user_id=user.id,
        username=user.username,
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)

async def getDeepSeekResponse(card: str, situation: str, current_user: User, db: Session):
    all_emotions = [emotion for sublist in EMOTIONS.values() for emotion in sublist]
    emotion_str = ", ".join(all_emotions)
        
    prompt = (
        f"The tarot card is {card} and the situation is {situation}. "
        f"Reply in JSON with 'emotion' (choose one from {emotion_str} only) and 'answer' (a plain paragraph)."
        "Interpret the card's symbolism in this context and suggest improvements."
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

    user = get_user_by_username(db, current_user.username)
    saveReading(card, situation, AiResponse(**parsed_output), response.usage.total_tokens, user, db)

    # print(parsed_output)
    # print(response.usage.prompt_tokens)
    # print(response.usage.completion_tokens)
    # print(response.usage.total_tokens)

    return AiResponse(
        emotion=parsed_output["emotion"],
        answer=parsed_output["answer"],
    )
    
