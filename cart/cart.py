from account.models import User
from cart.functions import getPass
from cart.models import CartItem
from ticket.functions import generate_ticket
from ticket.models import Ticket, Events
from ticket.send_ticket import send_email_thread
from PIL import Image
import io
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
			CartItem.objects.get(event=Events.objects.get(id=event_id),user=self.user).delete()
		self.cart.remove(event_id)
  
	def emptycart(self):
		"""Remove all items from the user's shopping cart."""
		for eventid in self.cart:
			CartItem.objects.get(event=Events.objects.get(id=eventid),user=self.user).delete()
		self.cart.clear()
  
	def generate_ticket(self):
		user=self.user
		_pass = getPass(user)
		added_events=list(self.get())
		if _pass != None:
			if _pass.technical == None:
				for event in added_events:
					if event.type == 'tech' and event.includedInPass:
						_pass.technical=event
						_pass.save()
						added_events.remove(event)
						break;
			if _pass.splash == None:
				for event in added_events:
					if event.type == 'splash' and event.includedInPass:
						_pass.splash=event
						_pass.save()
						added_events.remove(event)
						break;
		for eventid in self.cart:
			event=Events.objects.get(id=eventid)
			obj = Ticket.objects.create(user=user,event=event)
			user_obj=User.objects.get(id=user.id)
			email=user_obj.email
			print(event,obj)
			img = generate_ticket(obj.id)
			# image_buffer = io.BytesIO(img)
			# image=Image.open(image_buffer)
			# img_rgb=image.convert('RGB')
			# pdf_buffer = io.BytesIO()
			# img_rgb.save(pdf_buffer, 'PDF', resolution=100.0)
			# send_email_thread(email,event,pdf_buffer)
		self.emptycart()