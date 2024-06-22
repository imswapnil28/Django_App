from django.shortcuts import render

# Create your views here.
import openai
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

openai.api_key = 'sk-proj-a19lE1yniLUAt3Mn9TqRT3BlbkFJ5IUFGKaTjLKROuwYP12O'  # Replace with your OpenAI API key


def parse_text_with_chatgpt(text, fields):
    
    prompt = f"Extract the following fields from the text: {', '.join(fields)}.\n\n{text}"
    
    # Send the request to API
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that extracts specific information from text."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Collect the response
    return response.choices[0].message.content

def index(request):
    # Generate a token for the form
    csrf_token = get_token(request)
    return render(request, 'parserapp/index.html', {'csrf_token': csrf_token})

@csrf_exempt
def parse_text(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text')
        fields = data.get('fields', [])
        
        if not fields or not text:
            return JsonResponse({'error': 'Invalid request, fields and text are required'}, status=400)
        
        parsed_response = parse_text_with_chatgpt(text, fields).strip()
        parsed_data = {}

        # Convert the response to a dictionary
        for item in parsed_response.split('\n'):
            if ':' in item:
                key, value = item.split(':', 1)
                parsed_data[key.strip()] = value.strip()
        
        return JsonResponse(parsed_data)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

    


