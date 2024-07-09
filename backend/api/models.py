from django.db import models

class Expense(models.Model):
	date = models.DateField(auto_now_add=True)
	product = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return f"{self.date} - {self.product}: ${self.price}"