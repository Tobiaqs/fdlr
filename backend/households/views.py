from rest_framework import views

from common.utils import as_of_qs
from households.models import ExpenseGroupStake

def get_stakes_as_of(date, expense_group_id):
    return as_of_qs(ExpenseGroupStake.history, date).filter(expense_group_id=expense_group_id)


class TransactionAPIView(views.APIView):
    def get(self, request):
        print(get_stakes_as_of(request))
