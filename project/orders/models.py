import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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

    def __str__(self):
        accepted = 'accepted' if self.accepted else 'not accepted'
        client = self.client.get_full_name()
        return f'Ticket #{self.uuid}: {self.showing} bought by {client} ({accepted})'
