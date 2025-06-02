import json
from openai import OpenAI

import os
from dotenv import load_dotenv
from .schema_ai import AiResponse


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

def getDeepSeekResponse(card: str, situation: str):
    all_emotions = [emotion for sublist in EMOTIONS.values() for emotion in sublist]
    emotion_str = ", ".join(all_emotions)
        
    prompt = (
        f"The tarot card is {card} and the situation is {situation}. "
        f"Reply in JSON with 'emotion' (choose one from {emotion_str} only) and 'answer' (a plain paragraph)."
        "Interpret the card's symbolism in this context and suggest improvements."
    )
    
    print(prompt)

    response = client.chat.completions.create(
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
    
    # print(parsed_output)
    # print(response.usage.prompt_tokens)
    # print(response.usage.completion_tokens)
    # print(response.usage.total_tokens)

    return AiResponse(
        emotion=parsed_output["emotion"],
        answer=parsed_output["answer"],
        tokens=response.usage.total_tokens
    )