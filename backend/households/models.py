from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL

from common.models import BigCharField
from common.storages import MinioStorageInline
from simple_history.models import HistoricalRecords

class Household(models.Model):
    name = BigCharField('name')
    description = BigCharField('description', blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='owner', related_name='+', on_delete=CASCADE)

    def __str__(self):
        return self.name

class HouseholdInvite(models.Model):
    household = models.ForeignKey(Household, verbose_name='household', related_name='invites', on_delete=CASCADE)
    expiry = models.DateTimeField('expiry', null=True, blank=True)
    token = BigCharField('token')


class Housemate(models.Model):
    name = BigCharField('name')
    phone = BigCharField('phone', blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='user', related_name='housemates', on_delete=SET_NULL, null=True, blank=True)
    household = models.ForeignKey(Household, verbose_name='household', related_name='housemates', on_delete=CASCADE)
    avatar = models.FileField('avatar', storage=MinioStorageInline, blank=True)
    deleted = models.BooleanField('deleted', default=False)

    def __str__(self):
        return f'{self.name} ({self.household.name})'

class ExpenseGroup(models.Model):
    household = models.ForeignKey(Household, verbose_name='household', related_name='expense_groups', on_delete=CASCADE)
    name = BigCharField('name')
    description = BigCharField('description', blank=True)
    
    history = HistoricalRecords()

    def __str__(self):
        return self.name

class ExpenseGroupStake(models.Model):
    expense_group = models.ForeignKey(ExpenseGroup, verbose_name='expense group', related_name='stakes', on_delete=CASCADE)
    housemate = models.ForeignKey(Housemate, verbose_name='housemate', related_name='stakes', on_delete=PROTECT)
    stake = models.PositiveSmallIntegerField('stake')

    def __str__(self):
        return f'{self.housemate.name} has {self.stake}x stake in {self.expense_group.name}'
    
    history = HistoricalRecords()

class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        MEAL = 'meal', 'Meal'
        EXPENSE_GROUP = 'expense_group', 'Expense group'
        OTHER = 'other', 'Other'
        INITIAL = 'initial', 'Initial'
    
    household = models.ForeignKey(Household, verbose_name='household', related_name='transactions', on_delete=CASCADE)
    expense_group = models.ForeignKey(ExpenseGroup, verbose_name='expense group', related_name='+', on_delete=SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    creator = models.ForeignKey(Housemate, verbose_name='creator', related_name='+', on_delete=PROTECT)
    description = BigCharField('description', blank=True)
    transaction_type = BigCharField('transaction type', choices=TransactionType.choices)
    amount = models.PositiveIntegerField('amount', help_text='in cents')


    def __str__(self):
        return f'{self.TransactionType(self.transaction_type).label} transaction ({self.description})'

class Transfer(models.Model):
    household = models.ForeignKey(Household, verbose_name='household', related_name='transfers', on_delete=CASCADE)
    transaction = models.ForeignKey(Transaction, related_name='transfers', on_delete=CASCADE)
    beneficiary = models.ForeignKey(Housemate, related_name='+', on_delete=PROTECT)
    benefactor = models.ForeignKey(Housemate, related_name='+', on_delete=PROTECT)
    amount = models.PositiveIntegerField('amount', help_text='in cents')

    def __str__(self):
        return f'€{(self.amount / 100):.2f} from {self.benefactor.name} to {self.beneficiary.name}'
