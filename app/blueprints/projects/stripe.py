import stripe, os

stripe.api_key = os.environ.get('STRIPE_API_KEY')

convert_price = lambda n: float(n/100)

def initProducts():
  return [
    dict(
      id=p.id,
      prod_id=p.product,
      name=p.attributes.name,
      image=p.image,
      price=convert_price(p.price)
    )
    for p in stripe.SKU.list().data
  ]