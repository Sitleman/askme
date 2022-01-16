from django.contrib.auth.models import User
from django.db import models

class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-pub_date')
    def hot(self):
        return self.order_by('likes')
    def by_tag(self, tag):
        return self.filter(tags__name=tag)
    def by_id(self, req_id):
        return self.get(id=req_id)

# class Profile(models.Model):
#     avatar = models.FileField()
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Question(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    count_answers = models.IntegerField(default=0)
    m = QuestionManager()

class Answer(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')

class Tag(models.Model):
    name = models.CharField(max_length=50)
    questions = models.ManyToManyField('Question', related_name='tags')

class Like(models.Model):
    status = models.BooleanField()
    like_object = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='likes')