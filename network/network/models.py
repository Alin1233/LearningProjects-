from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(max_length=256)
    date_time = models.DateTimeField(auto_now_add = True)

    #order by most recent post
    class Meta:
       ordering = ['-date_time']

    def __str__(self):
        return f"{self.author.username},{self.text},{self.date_time}"

class Follower(models.Model):

    #the person that follows
    follows = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follows")
    #the person that is followed
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")

    def __str__(self):
        return f"{self.follows.username},{self.followed.username}"

class Like(models.Model):

    #the user that like a post 
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked")
    #the post liked 
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="post")

    def __str__(self):
        return f"{self.author.username},{self.post}"
