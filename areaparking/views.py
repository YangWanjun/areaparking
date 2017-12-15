from django.shortcuts import render


def handler_500(request):
    context = {
        'request_path': request.path,
    }
    return render(request, '500.html', context, status=500)
