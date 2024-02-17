from ticket.models import Ticket, Events

class Cart():
	def __init__(self, request):
		self.session = request.session
		# Get request
		self.request = request
		# Get the current session key if it exists
		cart = self.session.get('cart_key')

		# If the user is new, no session key!  Create one!
		if 'cart_key' not in request.session:
			cart = self.session['cart_key'] = {}


		# Make sure cart is available on all pages of site
		self.cart = cart

	def add(self, event_id:int):
		# Logic
		if event_id in self.cart:
			pass
		else:
			self.cart[event_id] = 1
			# self.cart.add(event_id)

		self.session.modified = True

		# Deal with logged in user
		# if self.request.user.is_authenticated:
		# 	# Get the current user profile
		# 	current_user = Profile.objects.filter(user__id=self.request.user.id)
		# 	# Convert {'3':1, '2':4} to {"3":1, "2":4}
		# 	carty = str(self.cart)
		# 	carty = carty.replace("\'", "\"")
		# 	# Save carty to the Profile Model
		# 	current_user.update(old_cart=str(carty))

	# def cart_total(self):
	# 	# Get product IDS
	# 	product_ids = self.cart.keys()
	# 	# lookup those keys in our products database model
	# 	products = Product.objects.filter(id__in=product_ids)
	# 	# Get quantities
	# 	quantities = self.cart
	# 	# Start counting at 0
	# 	total = 0
		
	# 	for key, value in quantities.items():
	# 		# Convert key string into into so we can do math
	# 		key = int(key)
	# 		for product in products:
	# 			if product.id == key:
	# 				if product.is_sale:
	# 					total = total + (product.sale_price * value)
	# 				else:
	# 					total = total + (product.price * value)



	# 	return total



	def __len__(self):
		return len(self.cart)

	def get(self) -> list[Events]:
		# Get ids from cart
		event_ids = self.cart.keys()
		# Use ids to lookup products in database model
		added_events = Events.objects.filter(id__in=event_ids)

		# Return those looked up products
		return added_events

	# def update(self, product, quantity):
	# 	product_id = str(product)
	# 	product_qty = int(quantity)

	# 	# Get cart
	# 	ourcart = self.cart
	# 	# Update Dictionary/cart
	# 	ourcart[product_id] = product_qty

	# 	self.session.modified = True

	# 	thing = self.cart
	# 	return thing

	def delete(self, event_id:int):
		# Delete from dictionary/cart
		del	self.cart[event_id]

		self.session.modified = True