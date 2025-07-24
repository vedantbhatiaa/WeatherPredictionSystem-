from django.shortcuts import render
from django.http import JsonResponse
from .farm_assistant import FarmAssistant

# Initialize the assistant
farm_bot = FarmAssistant()

def chat_view(request):
    return render(request, 'chatbot/chat.html')

def process_message(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        response = farm_bot.process_query(user_message)
        return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request'}, status=400)