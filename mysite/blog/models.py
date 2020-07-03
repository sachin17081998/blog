from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
'''
the two models post and comment are used to store information of post and comments on them
since it is a blogging site so a super user or the person who owns the blog can post content in it.
The post model is connected to auth.user(superuser) via a foreignkey so that a super user can only edit or create the post.

the comment model is connects to post model via a foreign key such that comments can be asociated to a particular
post.
'''

class post(models.Model):
    #author=models.ForeignKey('auth.user',on_delete=models.CASCADE)
   
    author = models.ForeignKey('auth.user',default=1,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    text=models.TextField()
    create_date=models.DateTimeField(default=timezone.now)
    published_date=models.DateTimeField(blank=True,null=True)
    
    #a method to set the published date
    def published(self):
        self.published_date=timezone.now()
        self.save()
    
    #a method to retrun only approved comments    
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)
    
    def __str__(self):
        return self.title
    #this method will take us to the post_deatil view whenever a new post is created
    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})    


class comments(models.Model):
    post=models.ForeignKey('blog.post',related_name='comments',on_delete=models.CASCADE)
    author=models.CharField(max_length=200)
    text=models.TextField() 
    create_date=models.DateTimeField(default=timezone.now())
    approved_comment=models.BooleanField(default=False)
    
    #a method to approved comments
    def approved(self):
        self.approved_comment=True
        self.save() 
    
    def __str__(self):
        return self.text          
    
    #a method to redirect us to the home page ,that is for our case is the  a page conatining list of posts
    #whenever someone comments on any post.
    def get_absolute_url(self):
        return reverse('post_list')