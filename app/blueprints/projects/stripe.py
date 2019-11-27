import stripe, os

stripe.api_key = os.environ.get('STRIPE_API_KEY')

# def convert_price(n):
#   return float(n/100)
convert_price = lambda n: float(n/100)

# def getUSD(x):
#   return round(x, 2)
getUSD = lambda x: round(x, 2)

products = [
  dict(
    id=p.id, 
    prod_id=p.product, 
    name=p.attributes.name, 
    image=p.image, 
    price=convert_price(p.price)
  ) for p in stripe.SKU.list().data
]