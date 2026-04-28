from django.shortcuts import render, get_object_or_404

def home(request):
    return render(request, 'public/home.html')

def about(request):
    return render(request, 'public/about.html')

def articles(request):
    return render(request, 'public/articles/list.html')

def articles_list(request):
    return render(request, 'public/articles/list.html')

def article_detail(request, slug):
    # Para contenido estático, se tiene q mapear slugs a templates específicos
    template_name = f'public/articles/{slug}.html'
    try:
        return render(request, template_name)
    except:
        return render(request, 'public/articles/not_found.html', status=404)

def faq(request):
    return render(request, 'public/faq.html')
