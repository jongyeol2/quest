from django.shortcuts import render, redirect, get_object_or_404
import openai, os
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required
from .models import Chatbot
from .forms import ChatbotForm

# .env 파일에서 환경 변수 로드
load_dotenv()

# API Key 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 프롬프트 명령
prompt = "You are a tour guide in Korea."

@login_required
def chat(request):
    if request.method == "POST":
        form = ChatbotForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data["user_input"]
            
            chat_history = Chatbot.objects.filter(author=request.user).order_by("-created_at")
            
            # 초기 대화 설정
            message = [{"role": "system", "content": prompt}]
            
            # 이전 대화내역 가져오기
            for chat in chat_history:
                message.append({"role": "user", "content": chat.user_input})
                message.append({"role": "assistant", "content": chat.ai_response})
            
            # 사용자 입력 추가
            message.append({"role": "user", "content": user_input})
            
            # OpenAI API 호출
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=message
            )
            ai_response = response['choices'][0]['message']['content']
            
            # 대화내용 저장
            chatbot_instance = form.save(commit=False)
            chatbot_instance.author = request.user
            chatbot_instance.ai_response = ai_response
            chat_history = Chatbot.objects.filter(author=request.user).order_by("-created_at")
            chatbot_instance.save()
            
            character = prompt.replace("You are ", "I am ")
            
            context = {
                "form": form,
                "ai_response": ai_response,
                "chat_history": chat_history,
                "character": character
            }
            return render(request, "chatbot/chat.html", context)
    else:
        form = ChatbotForm()
        chat_history = Chatbot.objects.filter(author=request.user).order_by("-created_at")
        character = prompt.replace("You are ", "I am ")
        context = {
            "form": form,
            "chat_history": chat_history,
            "character": character
        }
    return render(request, "chatbot/chat.html", context)