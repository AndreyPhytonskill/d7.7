from django.urls import reverse_lazy
from datetime import datetime
from django.views.generic import (
    ListView, DetailView,CreateView,UpdateView,
    DeleteView
)
from .filters import PostFilter
from .forms import PostForm
from .models import Post


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'time'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()

        self.filterset = PostFilter(self.request.GET, queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()

        return context

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

class SearchPosts(ListView):
     paginate_by = 10
     model = Post
     ordering = 'time'
     template_name = 'post_seach.html'
     context_object_name = 'news'

     def get_queryset(self):
         queryset = super().get_queryset()
         self.filterset = PostFilter(self.request.GET, queryset)
         return self.filterset.qs

     def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         # Добавляем в контекст объект фильтрации.
         context['search_filter'] = self.filterset
         return context

class NewsCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'
    premission_required = ('news.add_post')

    def form_valid(self, form):
        post = form.save(commit=False)

        if 'news' in self.request.path.split('/'):
            post.post_type = 'NS'
            self.success_url = reverse_lazy('news_list')
        else:
            post.post_type = 'AR'
            self.success_url = reverse_lazy('arts_list')

        return  super().form_valid(form)

class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Добавить статью"
        return context


class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Редактировать статью"
        return context


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Удалить статью"
        context['previous_page_url'] = reverse_lazy('posts_list')
        return context