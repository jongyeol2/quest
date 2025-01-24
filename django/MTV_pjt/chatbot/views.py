from django.shortcuts import render, redirect, get_object_or_404
import openai, os
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required
from .models import Chatbot
from .forms import ChatbotForm


@login_required
def chat(request):
    if request.method == "POST":
        form = ChatbotForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data["user_input"]
            
            # .env 파일에서 환경 변수 로드
            load_dotenv()
            
            # API Key 설정
            openai.api_key = os.getenv("OPENAI_API_KEY")
            
            # 프롬프트 명령
            prompt = "You are a very scary computer teacher."
            
            # 초기 대화 설정
            message = [{"role": "system", "content": prompt}]
            
            message.append({"role": "user", "content": user_input})
            
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=message
            )
            ai_response = response['choices'][0]['message']['content']
            
            chatbot_instance = form.save(commit=False)
            chatbot_instance.author = request.user
            chatbot_instance.ai_response = ai_response
            chatbot_instance.save()
            
            context = {
                "form": form,
                "ai_response": ai_response
            }
            return render(request, "chatbot/chat.html", context)
    else:
        form = ChatbotForm()
        context = {"form": form}
    return render(request, "chatbot/chat.html", context)