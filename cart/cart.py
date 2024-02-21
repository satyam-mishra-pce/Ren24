from cart.models import CartItem
from ticket.models import Ticket, Events

class Cart():
	def __init__(self, request):
		# self.session = request.session
		# Get request
		self.user = request.user
		self.request = request
		# Get the current session key if it exists
		cart = []
		if request.user.is_anonymous ==  False:
			items = CartItem.objects.filter(user=request.user)
			for item in items:
				cart.append(item.event.id)

		# Make sure cart is available on all pages of site
		self.cart = cart

	def add(self, event_id:int):
		# Logic
		if event_id in self.cart:
			pass
		else:
			if self.request.user.is_anonymous ==  False:
				CartItem.objects.create(
					user=self.request.user,
					event=Events.objects.get(id=event_id)
				)
			self.cart.append(event_id)
			# self.cart.add(event_id)


	def cart_total(self):
		# Get product IDS
		event_ids = self.cart
		# lookup those keys in our events database model
		events = Events.objects.filter(id__in=event_ids)
		# Get quantities
		quantities = self.cart
		# Start counting at 0
		total = 0
		
		for key in events:
			total += key.amount

		return total



	def __len__(self):
		return len(self.cart)

	def get(self) -> list[Events]:
		# Get ids from cart
		event_ids = self.cart
		# Use ids to lookup products in database model
		added_events = Events.objects.filter(id__in=event_ids)

		# Return those looked up products
		return added_events

	def delete(self, event_id:int):
		# Delete from dictionary/cart
		if self.request.user.is_anonymous ==  False:
			CartItem.objects.get(event=Events.objects.get(id=event_id)).delete()
		self.cart.remove(event_id)
  
	def emptycart(self):
		"""Remove all items from the user's shopping cart."""
		for eventid in self.cart:
			Events.objects.get(id=eventid).delete()
		self.cart.clear()
  
	def generate_ticket(self):
		user=self.user
		for eventid in self.cart:
			event=Events.objects.get(id=eventid)
			Ticket.objects.create(user=user,event=event)
		self.emptycart()