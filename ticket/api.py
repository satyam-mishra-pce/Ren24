from datetime import datetime
import json
from django.http import JsonResponse,HttpResponse

from ticket.models import Ticket

def verify(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # event_id = request.POST.get('event_id')
            ticket_id = data.get('ticketId')
            if ticket_id is not None:
                ticket = Ticket.objects.get(id=ticket_id)
                if ticket.used == True or ticket.date != datetime.today():
                    return HttpResponse('Ticket used or not for today',status=404)
                else:
                    context = {
                        'avatar':ticket.user.profile.avatar.url,
                        'first_name':ticket.user.first_name,
                        'last_name':ticket.user.last_name,
                        'event':ticket.event,
                        'time':ticket.time,
                        'date':ticket.date,
                    }
                    return JsonResponse(context)
            else:
                return HttpResponse('Ticket Id missing',status=400)
        except Ticket.DoesNotExist:
            return HttpResponse('Invalid ticket',status=402)
        except Exception as e:
            print(e)
            return HttpResponse("Unexpected error occured !",status=500)
    else:
        return HttpResponse('Method not allowed',status=400)

def permit(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # event_id = request.POST.get('event_id')
            ticket_id = data.get('ticketId')
            if ticket_id is not None:
                ticket = Ticket.objects.get(id=ticket_id)
                if ticket.used == True or ticket.date != datetime.today():
                    return HttpResponse('Ticket used or not for today',status=404)
                else:
                    ticket.used = True
                    ticket.save()
                    return HttpResponse('Entry permitted',status=200)
            else:
                return HttpResponse('Ticket Id missing',status=400)
        except Ticket.DoesNotExist:
            return HttpResponse('Invalid ticket',status=402)
        except Exception as e:
            print(e)
            return HttpResponse("Unexpected error occured !",status=500)
    else:
        return HttpResponse('Method not allowed',status=400)