from django.db.models.functions import TruncDate
from django.utils.dateparse import parse_date
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Expense
from .serializers import ExpenseSerializer
import logging

logger = logging.getLogger('django')

class ExpenseViewSet(viewsets.ModelViewSet):
	logger.info("Starting ExpenseViewSet...")

	queryset = Expense.objects.all()
	serializer_class = ExpenseSerializer

	def create(self, request, *args, **kwargs):
		logger.info('Creating an expense... => %s', request.data)
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


	def list(self, request, *args, **kwargs):
		logger.info('Fetching expenses... => %s', request.query_params)
		
		date_param = request.query_params.get('date')
		
		if date_param:
			try:
				filter_date = parse_date(date_param)
				if filter_date is None:
					raise ValueError("Invalid date format")
			except ValueError:
				raise ValidationError({"date": "Invalid date format. Use YYYY-MM-DD."})

			queryset = self.get_queryset().filter(date=filter_date)
		else:
			queryset = self.get_queryset()

		queryset = self.filter_queryset(queryset)
		page = self.paginate_queryset(queryset)
		
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)
		


	