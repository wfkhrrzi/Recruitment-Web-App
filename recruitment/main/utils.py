
def return_json(request):
    if request.META.get('HTTP_ACCEPT') == 'application/json':
        return True
    else:
        return False