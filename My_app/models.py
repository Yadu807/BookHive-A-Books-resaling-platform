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
    price = models.DecimalField(max_digits=10, decimal_places=2)
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

class SearchKeyword(models.Model):
    user = models.ForeignKey(user_table, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    BookID = models.ForeignKey('book_table', on_delete=models.CASCADE)
    BuyerID = models.ForeignKey('user_table', on_delete=models.CASCADE)
    OrderDate = models.DateField(auto_now_add=True)
    Status = models.CharField(max_length=100, default='Requested')
    Amount = models.IntegerField()
    NStatus = models.CharField(max_length=100, default='pending')

class Feedback(models.Model):
    seller = models.ForeignKey(user_table, on_delete=models.CASCADE,related_name="p")
    user = models.ForeignKey(user_table, on_delete=models.CASCADE,related_name="l")
    feedback = models.TextField()
    rating = models.FloatField()
    datetime = models.DateTimeField(auto_now_add=True)

class BlockStatus(models.Model):
    LOGIN = models.OneToOneField(login_table, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default="Active")  # Status can be 'Active' or 'Blocked'

class Report(models.Model):
    book = models.ForeignKey(book_table, on_delete=models.CASCADE)
    user = models.ForeignKey(user_table, on_delete=models.CASCADE)
    complaint_text = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)


