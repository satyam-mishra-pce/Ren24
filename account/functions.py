from ticket.models import Ticket
from account.models import Passes

def getPass(user):
    if user._pass :
        return user._pass
    _pass = Passes.objects.filter(email=user.email)
    if _pass.exists():
        user._pass = _pass.first()
        user.save()
        return _pass.first()
    else:
        return None