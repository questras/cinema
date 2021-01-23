import uuid

from django.db import models
from django.core.validators import MinValueValidator

from cinema.models import Showing
from users.models import CustomUser


class Order(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now_add=True)
    tickets_amount = models.IntegerField(validators=[MinValueValidator(1)])
    accepted = models.BooleanField(default=False)
    showing = models.ForeignKey(Showing, on_delete=models.CASCADE)
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='my_orders')
    cashier_who_accepted = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                             null=True, blank=True, related_name='accepted_orders')

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='correct_tickets_amount',
                check=models.Q(tickets_amount__gte=1)
            )
        ]

    def is_accepted(self):
        return self.accepted

    def is_rejected(self):
        return (not self.is_accepted()) and self.cashier_who_accepted is not None

    def is_not_accepted(self):
        return (not self.is_accepted()) and (not self.is_rejected())

    def is_accepted_string(self):
        if self.is_accepted():
            string = 'accepted'
        elif self.is_rejected():
            string = 'rejected'
        else:
            string = 'not accepted'
        return string

    def __str__(self):
        accepted = self.is_accepted_string()
        client = self.client.get_full_name()
        return f'Ticket #{self.uuid}: {self.showing} bought by {client} ({accepted})'
