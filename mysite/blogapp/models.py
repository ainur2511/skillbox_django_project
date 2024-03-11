from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    bio = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=40, db_index=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=40, db_index=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField()
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')

    def __str__(self):
        return self.title
