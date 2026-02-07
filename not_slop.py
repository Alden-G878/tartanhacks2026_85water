import asyncio
from typing import Literal
from dedalus_labs import AsyncDedalus
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Command(BaseModel):
    Source: Literal["red box", "blue box", "green box"]
    Destination: Literal["lower left corner", "lower right corner", "upper left corner", "upper right corner"]

async def ai_cmd(usr_txt):
    client = AsyncDedalus()
    completion = await client.chat.completions.parse(
        model="openai/gpt-5.2",
        messages=[{
            "role": "user",
            "content": (
                "You are a controller for a robotic arm"
                "There are three objects that can be moved"
                "One of the objects that can be moved is a red box"
                "One of the objects that can be moved is a blue box"
                "One of the objects that can be moved is a green box"
                "There are four locations that each object can be moved to"
                "One of the locations is the lower left corner"
                "One of the locations is the lower right corner"
                "One of the locations is the upper left corner"
                "One of the locations is the upper right corner"
                "There is a user of this robotic arm"
                "Your role is to assist the user"
                "The user may not use the exact language for each box or location"
                "The user will request to move one object to one destination"
                "Only one object will be moved a time"
                "An object will only move to one destination at a time"
                "Each event must include a Source (red box/blue box/green box) and a Destination (lower left corner/lower right corner/upper left corner/upper right corner)"
                f"The user's command is: {usr_txt}"
            )
        }],
        response_format=Command
    )

    parsed = completion.choices[0].message.parsed
    return f"{parsed.Source}:{parsed.Destination}"
