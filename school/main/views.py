from django.shortcuts import render, redirect


def index_view(request):
    context_header = {'title': ''}
    context = {'context_header': context_header}
    return render(request, 'main/index.html')