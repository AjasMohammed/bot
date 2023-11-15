from .models import *
import random


class Chatbot:
    def __init__(self, name):
        self.user, created = User.objects.get_or_create(name=name)
        self.cart = self.user.cart.all()

    def greet(self):
        return f'Hello {self.user.name}'

    def list_products(self):
        products = Product.objects.values_list('name', flat=True)
        context = " These are the Products We have <br> "
        for product in products:
            context += product + '<br>'

        context += 'If you need to know more about a product type [product name]'
        return context

    def products_info(self, product_names):
        products = Product.objects.filter(name__in=product_names)
        context = ""
        for product in products:
            context += f"""
                        Name: {product.name}<br>
                        Description: {product.description}<br>
                        Price: {product.price}<br><br>
                        
                """
        return context

    def prod_recommendation(self):
        products = Product.objects.all()
        product = random.choice(products)

        context = f''' 
                        Sure Here is a Great product for you, <br><br>
                        {product.name}<br>
                        {product.price}<br>
                        {product.description}<br>
                         '''
        return context

    def add_to_cart(self, product_name):
        product = Product.objects.get(name__icontains=product_name)
        if not product.is_available:
            context = f'Sorry for the Trouble, the {product.name} is currently Unavailabl!'
            return context
        cart = Cart.objects.create(user=self.user, product=product)
        cart.save()

        self.cart = Cart.objects.filter(user=self.user)
        context = 'Product succesfully added to the cart. Do you wish to view the cart?'
        return context

    def view_cart(self):
        context = ''
        total = 0
        print(self.cart)
        for product in self.cart:
            product = product.product
            total += float(product.price)
            context += f"""
                    {product.name} - {product.price}<br><br>
                    """
        context += f'Total: {total}Rs'
        return context
    
    def remove_from_cart(self, product_name):
        cart = Cart.objects.get(name=product_name)
        cart.delete()
        self.cart = Cart.objects.filter(user=self.user)
        context = "Product removed Sucessfully!"
        return context
    
    def place_order(self):
        Cart.objects.filter(user=self.user).delete()
        self.cart = []
        context = 'Order Placed Sucessfully!'
        return context
