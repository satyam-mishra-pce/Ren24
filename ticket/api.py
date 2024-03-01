from datetime import datetime
import json
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from account.models import Passes
from ticket.models import CustomTicket, Ticket


#TODO : Update this Date
day1 = datetime.strptime('2024-3-1','%Y-%m-%d').date()
day2 = datetime.strptime('2024-3-20','%Y-%m-%d').date()
day3 = datetime.strptime('2024-3-21','%Y-%m-%d').date()

@csrf_exempt
def verify(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # event_id = request.POST.get('event_id')
            ticket_id = data.get('ticketId')
            if ticket_id is not None:
                ticket = Passes.objects.get(psid=ticket_id)
                print(datetime.today())
                # today = datetime.strptime('2024-3-2','%Y-%m-%d').date()
                today = datetime.today().date()
                if ticket.day1 == True and today == day1:
                    return HttpResponse('Ticket used or not for today',status=404)
                elif ticket.day2 == True and today == day2:
                    return HttpResponse('Ticket used or not for today',status=404)
                elif ticket.day3 == True and today == day3:
                    return HttpResponse('Ticket used or not for today',status=404)
                else:
                    context = {
                        'first_name':str(ticket.user.first_name),
                        'last_name':str(ticket.user.last_name),
                        'email':str(ticket.user.email),
                        'date':str(today),
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

@csrf_exempt
def permit(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # event_id = request.POST.get('event_id')
            ticket_id = data.get('ticketId')
            if ticket_id is not None:
                today = datetime.today().date()
                ticket = Passes.objects.get(psid=ticket_id)
                if ticket.day1 == True and today == day1:
                    return HttpResponse('Ticket used or not for today',status=404)
                elif ticket.day2 == True and today == day2:
                    return HttpResponse('Ticket used or not for today',status=404)
                elif ticket.day3 == True and today == day3:
                    return HttpResponse('Ticket used or not for today',status=404)
                # if ticket.used == True :#or ticket.date != datetime.today():
                #     return HttpResponse('Ticket used or not for today',status=404)
                else:
                    if today == day1:
                        ticket.day1 = True
                    elif today == day2:
                        ticket.day2 = True
                    elif today == day3:
                        ticket.day3 = True 
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

@csrf_exempt
def verify_custom(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # event_id = request.POST.get('event_id')
            ticket_id = data.get('ticketId')
            if ticket_id is not None:
                ticket = CustomTicket.objects.get(id=ticket_id)
                # today = datetime.today().date()
                today = datetime.strptime('2024-3-1','%Y-%m-%d').date()
                # if ticket.day1 == True and today == day1:
                #     return HttpResponse('Ticket used or not for today',status=404)
                # if ticket.day2 == True and today == day2:
                #     return HttpResponse('Ticket used or not for today',status=404)
                # if ticket.day3 == True and today == day3:
                #     return HttpResponse('Ticket used or not for today',status=404)
                if ticket.used == True and ticket.event.date != today:
                    return HttpResponse('Ticket used or not for today',status=404)
                context = {
                    'first_name':str(ticket.name.split(' ')[0]),
                    'last_name':str(ticket.name.split(' ')[-1]),
                    'email':str(ticket.email),
                    'date':str(ticket.event.date),
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

@csrf_exempt
def permit_custom(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # event_id = request.POST.get('event_id')
            ticket_id = data.get('ticketId')
            if ticket_id is not None:
                ticket = CustomTicket.objects.get(id=ticket_id)
                # today = datetime.today().date()
                today = datetime.strptime('2024-3-1','%Y-%m-%d').date()
                if ticket.used == True and ticket.event.date.date() != today:
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