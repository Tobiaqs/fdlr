from django.contrib import admin

from households.models import ExpenseGroup, ExpenseGroupStake, Household, HouseholdInvite, Housemate, Transaction, Transfer

admin.site.register(Household)
admin.site.register(HouseholdInvite)
admin.site.register(Housemate)
admin.site.register(ExpenseGroup)
admin.site.register(ExpenseGroupStake)
admin.site.register(Transaction)
admin.site.register(Transfer)
