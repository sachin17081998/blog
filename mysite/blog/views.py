from django.shortcuts import render
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import post,comments
from django.utils import timezone
from blog.forms import postform,commentform
from django.urls import reverse,reverse_lazy
# Create your views here.

class aboutview(TemplateView):
    template_name='about.html'
    
class post_list_view(ListView):   
    model=post
    
    # a method get_queryset() to make sql queries
    def get_queryset(self):
        return post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date') 
    #sql query: select * from post where published_date<=timezone.now() orderby='desc'
    #filter():it take out only those post where published date is todays date
    #__lte()[double underscore lte]:it is django ORM for less than
    #-published_date:means oredr in descending oredre,for ascending order just use published_date 

class post_detail_view(DetailView):
    model=post
    
    
#CRUD views    

#here we use a mixin to allow to create post for only those user who has login in
class create_post_view(LoginRequiredMixin,CreateView):
    #login_url specify the url incase the peron is not logged in
    login_url='/login/'
    #redirect_field_name to redirect user to the deatl view fter creating the post.

    redirect_field_name = 'blog/post_detail.html'
    form_class=postform
    model=post
    

#similar to create view    
class post_update_view(LoginRequiredMixin,UpdateView):
    login_url='/login/'
    redirect_field_name='blog/post_detail.html'
    form_class=postform
    model=post
    
class post_delete_view(LoginRequiredMixin,DeleteView):                
    model=post
    success_url=reverse_lazy('post_list')

class draft_list_view(LoginRequiredMixin,ListView):
    login_url='/login/'
    redirect_field_name='blog/post_list.html'
    model=post
    
    def get_query_set(self):
        return post.objects.filter(published_date__isnull=True).order_by('create_date')    
    
    
#######################################################################################
#######################################################################################
#######################################################################################

#functional views for comments 
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required

@login_required
def add_comment_to_post(request,pk):
    Post=get_object_or_404(post,pk=pk)
    if request.method=='POST':
        form=commentform(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=Post
            comment.save()
            return redirect('post_detail',pk=Post.pk)#post remainder for error
    else:
        form=commentform()
    return render(request,'blog/comment_form.html',{'form':form})    
    
@login_required
def comments_approved(request,pk):
    comment=get_object_or_404(comments,pk=pk)
    comment.approved()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(comments,pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk) 

@login_required
def post_publish(request,pk):
    Post=get_object_or_404(post,pk=pk)
    Post.published()
    return redirect('post_detail',pk=pk)
          