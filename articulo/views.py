from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Count
from django.contrib import messages
from django.views.generic import View, UpdateView, DeleteView
from .forms import ArticleForm, CategoryForm
from .models import Articles, Category
from django.urls import reverse_lazy


# Create your views here.
def home(request):
    articles = Articles.objects.order_by('-date_published')[:3]
    return render(request, 'home.html', {'articles': articles})


# para crear categorias
class CategoryCreateView(View):
    def get(self, request, *args, **kwargs):
        form = CategoryForm()
        categories = Category.objects.all()  
        context = {
            'form': form,
            'categories': categories,
        }
        return render(request, 'category/category_create.html', context)

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articulos:create_category')  
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
        }
        return render(request, 'category/category_create.html', context)


# Eliminar una categoria
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category/category_delete.html'
    success_url = reverse_lazy('articulos:create_category')
    




# mostrar todos los articulos desde nav articulos
class AllArticlesView(View):
    def get(self, request, *args, **kwargs):
        articles = Articles.objects.all()
        context = {
            'articles': articles  
        }
        return render(request, 'profile/articles/all_articles.html', context)





# para articulos CRUD
class ArtListView(View):
    def get(self, request, *args, **kwargs):
        articles = Articles.objects.order_by('-date_published')[:3]
        context = {
            'articles': articles
        }
        return render(request, 'home.html', context)


class ArtCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm(initial={'category':1})
        context = {
            'form': form
        }
        return render(request, 'profile/articles/Art_create.html', context)

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                content = form.cleaned_data.get('content')
                image = form.cleaned_data.get('image')
                date_published = form.cleaned_data.get('date_published')
                category = form.cleaned_data.get('category')

                p, created = Articles.objects.get_or_create(title=title, content=content, image=image, date_published=date_published, category=category)
                p.save()
                return redirect('articulos:home')

        context = {}
        return render(request, 'profile/articles/Art_create.html', context)
    


class ArtDetailView(View):
    def get(self, request, post_id, *args, **kwargs):
        article = get_object_or_404(Articles, pk=post_id)
        context = {
            'article': article
        }
        return render(request, 'profile/articles/Art_detail.html', context)


class ArtUpdateView(UpdateView):
    model = Articles
    form_class = ArticleForm
    template_name = 'profile/articles/Art_update.html'

    def form_valid(self, form):
        messages.success(self.request, 'Los cambios se han guardado exitosamente.')
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('articulos:detail_article', kwargs={'post_id': pk})



class ArtDeleteView(DeleteView):
    model = Articles
    template_name = 'profile/articles/Art_delete.html'
    success_url = reverse_lazy('articulos:home')



#Mostrar todas las categoria
class AllCategoriaView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.annotate(count=Count('articles'))
        context = {
            'categories': categories
        }
        return render(request, 'category/all_category.html', context)
    

# Mostrar todos los artículos dependientes de esa categoría
class AllCategoriaArticlesView(View):
    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id')
        try:
            category = Category.objects.get(pk=category_id)
            articles = category.articles_set.all()
        except Category.DoesNotExist:
            articles = []

        context = {
            'category': category,
            'articles': articles
        }
        return render(request, 'category/all_category_articles.html', context)
    


#Mostrar acerca-de
class AllAboutView(View):
    def get(self, request, *args, **kwargs):
        context = {
            
        }
        return render(request, 'about/about.html', context)


#Mostrar contact
class AllContactView(View):
    def get(self, request, *args, **kwargs):
        context = {
            
        }
        return render(request, 'contact/contact.html', context)
