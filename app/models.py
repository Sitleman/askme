from django.db import models

class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-pub_date')
    def hot(self):
        return self.order_by('likes')
    def by_tag(self, tag):
        return self.filter(tags__name=tag)

class Question(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    count_answers = models.IntegerField(default=0)
    m = QuestionManager()

class Answer(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='answers')

class Tag(models.Model):
    name = models.CharField(max_length=50)
    questions = models.ManyToManyField('Question', related_name='tags')

class Profile(models.Model):
    #avatar = models.ImageField()
    avatar = models.CharField(max_length=50)

class Like(models.Model):
    status = models.BooleanField()
    like_object = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='likes')