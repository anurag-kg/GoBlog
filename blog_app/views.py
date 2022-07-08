from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from .models import Post,Comment
from django.utils import timezone
from .forms import PostForm,CommentForm
from django.urls import reverse_lazy 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

class HomePage(TemplateView):
    template_name='index.html'
    
def contact(request):
    context = {
        'contact_text':"For queries please contact us on 0551",
    }
    return render(request,'contact.html',context)

def about(request):
    context = {
        'about_text':"We are startup.",
    }
    return render(request,'about.html',context)

class PostListView(ListView):
    context_object_name = 'post_list'
    template_name = 'post_list.html'
    model = Post
    
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    
class CreatePostView(LoginRequiredMixin,CreateView):
    redirect_field_name = 'post_detail.html'
    template_name = 'post_form.html'
    form_class = PostForm
    model = Post
    
class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name='post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

class PostUpdateView(LoginRequiredMixin,UpdateView):
    redirect_field_name = 'post_detail.html'
    form_class = PostForm
    fields = ('title','text')
    template_name = 'post_form.html'
    model = Post

class DraftListView(LoginRequiredMixin,ListView):
    context_oject_name='post_draft_list'
    template_name = 'post_draft_list.html'
    login_url = '/login/'
    redirect_field_name = 'post_draft_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

    
    
@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)


def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method =="POST":
        form =CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
            form=CommentForm()
    return render(request,'comment_form.html',{'form':form})
    
@login_required    
def comment_approve(request, pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

