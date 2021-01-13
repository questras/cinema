import uuid

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError

from .validators import (
    validate_correct_year_of_production,
    validate_correct_duration,
    validate_correct_no_places
)


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=256)
    director = models.CharField(max_length=256)
    year_of_production = models.IntegerField(
        verbose_name='year of production',
        validators=[validate_correct_year_of_production]
    )
    type = models.CharField(max_length=80)
    duration_in_minutes = models.IntegerField(
        verbose_name='duration in minutes',
        validators=[validate_correct_duration])
    description = models.TextField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(year_of_production__gte=1888) & models.Q(year_of_production__lt=3000),
                name='correct_year_of_production'
            ),
            models.CheckConstraint(
                check=models.Q(duration_in_minutes__gte=0) & models.Q(duration_in_minutes__lte=600),
                name='correct_duration_in_minutes'
            ),
        ]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Movie, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('movie-detail-view', args=(self.slug,))

    def __str__(self):
        return f'{self.title}({self.year_of_production}) by {self.director}'


class Hall(models.Model):
    number = models.AutoField(primary_key=True)
    places = models.IntegerField(
        verbose_name='amount of places',
        validators=[validate_correct_no_places]
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(places__gte=0) & models.Q(places__lte=400),
                name='correct_amount_of_places'
            ),
        ]

    def __str__(self):
        return f'Hall number {self.number} ({self.places} places)'


class Showing(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    when = models.DateTimeField(null=False, blank=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)

    class Meta:
        ordering = ['when']

    def clean(self):
        """Check if there are not any collisions with
        showing that is to be added.
        """

        day_before = self.when - timezone.timedelta(days=1)
        day_after = self.when + timezone.timedelta(days=1)

        showings_that_might_collide = Showing.objects.filter(
            when__gte=day_before, when__lte=day_after, hall=self.hall
        )

        new_start_time = self.when
        new_end_time = self.when + timezone.timedelta(minutes=self.movie.duration_in_minutes)

        for showing in showings_that_might_collide:
            existing_start_time = showing.when
            existing_end_time = showing.when + timezone.timedelta(minutes=showing.movie.duration_in_minutes)

            if existing_start_time < new_start_time < existing_end_time or \
                    existing_start_time < new_end_time < existing_end_time or \
                    (new_start_time < existing_start_time and new_end_time > existing_end_time):
                colliding_showing = str(showing)
                raise ValidationError(
                    '%(value)s collides with showing that is to be added',
                    params={'value': colliding_showing}
                )

    def save(self, *args, **kwargs):
        self.full_clean()

        return super(Showing, self).save(*args, **kwargs)

    def get_time(self):
        tz = timezone.get_default_timezone()
        start_hour = self.when.astimezone(tz).time().hour
        start_minutes = self.when.astimezone(tz).time().minute

        return f'{start_hour:02}:{start_minutes:02}'

    def get_date(self):
        return self.when.date()

    def get_numerical_weekday(self):
        """Return week day where Monday is 0 and Sunday is 6"""
        return self.when.weekday()

    def get_weekday(self):
        return self.when.strftime('%A')

    def get_absolute_url(self):
        return reverse('showing-detail-view', args=(self.uuid,))

    def all_places(self):
        return self.hall.places

    def taken_places(self):
        taken_places = self.order_set.exclude(accepted=False, cashier_who_accepted__isnull=False)
        return taken_places.aggregate(taken=models.Sum('tickets_amount'))['taken'] or 0

    def free_places(self):
        return self.all_places() - self.taken_places()

    def __str__(self):
        start_time = self.get_time()
        start_date = self.get_date()
        weekday = self.get_weekday()

        return f'{self.movie.title} on {weekday} ({start_date} {start_time})'
