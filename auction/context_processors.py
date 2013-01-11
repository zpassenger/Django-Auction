from auction.utils import get_or_create_bidbasket

def bidbasket(request):
    user = request.user
    bidbasket = get_or_create_bidbasket(request)
    result = {'bidbasket':bidbasket}
    return result