from django.shortcuts import render, redirect
from django.views.generic import ListView

from .forms import SearchForm
from .parser import main
from .models import Parser


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            main(form.cleaned_data['keyword'])
            return redirect('index_list')

    else:
        form = SearchForm()
    return render(request, 'parser/form.html', {'form': form, 'title': 'поиск вакансий'})


# def index_view(request):
#     parser = Parser.objects.all()
#     return render(request, 'list_view.html', {"parser": parser, 'title': 'Все вакансии'})
class IndexListView(ListView):
    model = Parser
    template_name = 'list_view.html'