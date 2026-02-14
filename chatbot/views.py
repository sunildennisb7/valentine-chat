import json
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def home(request):
    return render(request, "chat/home.html")

@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message")

        # Initialize conversation
        if "conversation" not in request.session:
            request.session["conversation"] = [
                {
                    "role":"system",
                    "content": """
You are CupidAI, a warm, playful AI created by Sunil.
- Keep responses short and sweet
- Make the user feel happy and special
- Guide gently toward expressing admiration and affection
- Do NOT reveal Sunil until cinematic flow
                    """
                }
            ]

        request.session["conversation"].append({"role":"user","content":user_message})

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=request.session["conversation"]
        )

        reply = completion.choices[0].message.content
        request.session["conversation"].append({"role":"assistant","content":reply})
        request.session.modified = True

        return JsonResponse({"reply":reply})
