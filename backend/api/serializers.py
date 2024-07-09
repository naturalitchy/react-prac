from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
	date = serializers.DateTimeField()
	
	class Meta:
		model = Expense
		fields = ['id', 'date', 'product', 'price']