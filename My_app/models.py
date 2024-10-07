from django.db import models


class login_table(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    type = models.CharField(max_length=100)


class user_table(models.Model):
    LOGIN = models.ForeignKey(login_table, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    email = models.CharField(max_length=254)
    photo = models.FileField()

class category_table(models.Model):
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=100)


class book_table(models.Model):
    category = models.ForeignKey(category_table, on_delete=models.CASCADE)
    Tittle = models.CharField(max_length=100)
    Author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    price = models.BigIntegerField()
    description = models.TextField()
    user_id = models.ForeignKey(user_table, on_delete=models.CASCADE)
    photo = models.FileField()
    status = models.CharField(max_length=100)
    language = models.CharField(max_length=100)


class favorites_table(models.Model):
    user = models.ForeignKey(user_table, on_delete=models.CASCADE)
    book = models.ForeignKey(book_table, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    FROMID = models.ForeignKey(login_table, on_delete=models.CASCADE, related_name="Fromid")
    TOID = models.ForeignKey(login_table, on_delete=models.CASCADE, related_name="Toid")
    message = models.CharField(max_length=100)
    date = models.DateField()
    ctype = models.CharField(max_length=25)
    status = models.CharField(max_length=25)