from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import *
import random
from .bot import Chatbot


def home(request):
    return render(request, 'home.html')


def chat(request):
    if request.method == 'POST':
        data = request.POST.get('data')

        user_name = request.GET.get('username')

        message = json.loads(data).get('message')
        context = {
            'response': ''
        }

        bot = Chatbot(user_name)

        content = message.lower()

        if 'hi' in content or 'hello' in content or 'hai' in content:
            context['response'] = bot.greet()


        elif '[' and ']' in message:
            start_index = message.find('[')
            end_index = message.find(']')

            value = message[start_index+1 : end_index]
            product_names = list(map(lambda val: val.title().strip(), value.split(',')))
            
            context['response'] = bot.products_info(product_names)


        elif 'recommend' in content:
            context['response'] = bot.prod_recommendation()


        elif 'products' in content:
            context['response'] = bot.list_products()
        

        elif 'cart' in content:
            if 'add' in content:
                products = Product.objects.values_list('name', flat=True)
                for product in products:
                    if product.lower() in content:
                        context['response'] = bot.add_to_cart(product)
        
            elif 'view' in content:
                context['response'] = bot.view_cart()

            elif 'remove' in content or 'delete' in content:
                products = Product.objects.values_list('name', flat=True)
                for product in products:
                    if product.lower() in content:
                        context['response'] = bot.remove_from_cart() 
            else:
                context['response'] = 'Sorry the Product Not Found!'

        else:
            context['response'] = "Sorry I couldn't understand what you said! Can you repeat?"    

        return JsonResponse(context)
    
    return render(request, 'chat.html')