from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView, FormView
from django.urls import reverse_lazy
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Article, Comment
from django.shortcuts import get_object_or_404, render, redirect


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    login_url = 'login'

    def get_queryset(self):
        articles = Article.objects.all().order_by('-date')
        paginator = Paginator(articles, 4)
        page = self.request.GET.get('page', 1)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(0)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
            print(page.paginator.num_pages)
        return articles


def add_like(request, pk):
    # pk = Article.objects.get(pk=kwargs.get('pk'))

    articles = Article.objects.get(pk=pk)
    articles.likes += 1
    articles.save()
    return redirect("article_list")
    


def add_dislike(request, pk):
   
    articles = Article.objects.get(pk=pk)
    articles.dislike += 1
    articles.save()
    return redirect('article_list')


class ArticleDetailView(LoginRequiredMixin, FormView, DetailView):
    model = Article
    form_class = CommentForm
    template_name = 'article_detail.html'
    login_url = 'login'
    hello = 0
  

    def get_success_url(self):
        self.form_class
        return reverse_lazy('article_list')
    
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs) 
        res = Article.objects.get(pk=self.object.pk)
        ArticleDetailView.hello = self.object.pk
        context['comments'] = res.comments.all()
        return context

    def form_valid(self, form):
        comment = form.cleaned_data.get('comment')
        author = self.request.user
        article = Article.objects.get(pk=self.hello)
        if form:
            Comment.objects.create(author=author, comment=comment, article=article)
        form.instance.author = self.request.user
        form.save()
        return super(ArticleDetailView, self).form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'body',)
    template_name = 'article_edit.html'
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user




class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user



class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'body')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class SearchResultsView(ListView):
    model = Article
    template_name = 'search_results.html'
    
    def get_queryset(self):
        queryset = self.request.GET.get('q')
        objects_list = Article.objects.filter(
            Q(title__icontains=queryset) | Q(body__icontains=queryset)
        )
        return objects_list


# class CommentView(LoginRequiredMixin, DetailView):
#     model = Article
#     fields = ('title', 'body',)
#     template_name = 'add_comment.html'
#     success_url = reverse_lazy('add_comment')
#     login_url = 'login'

#     def test_func(self):
#         obj = self.get_object()
#         return obj.author == self.request.user