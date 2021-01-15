import uuid

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.conf import settings

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
        ordering = ['year_of_production']

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

    def check_is_not_colliding(self):
        """Check whether there are not any collisions with
        current showing.
        """

        day_before = self.get_datetime() - timezone.timedelta(days=1)
        day_after = self.get_datetime() + timezone.timedelta(days=1)

        showings_that_might_collide = Showing.objects.filter(
            when__gte=day_before, when__lte=day_after, hall=self.hall
        )

        new_start_time = self.get_datetime()
        new_end_time = self.get_end_time()

        for showing in showings_that_might_collide:
            existing_start_time = showing.get_datetime()
            existing_end_time = showing.get_end_time()

            if existing_start_time < new_start_time < existing_end_time or \
                    existing_start_time < new_end_time < existing_end_time or \
                    (new_start_time < existing_start_time and new_end_time > existing_end_time):
                colliding_showing = str(showing)
                raise ValidationError(
                    '%(value)s collides with showing that is to be added',
                    params={'value': colliding_showing}
                )

    def check_is_between_open_hours(self):
        """Check whether current showing is between opening and
        closing hours."""

        validation_error = ValidationError(
            '%(value)s collides with cinema open hours',
            params={'value': str(self)}
        )

        opening_h = settings.CINEMA_OPENING_HOUR
        opening_m = settings.CINEMA_OPENING_MINUTE
        closing_h = settings.CINEMA_CLOSING_HOUR
        closing_m = settings.CINEMA_CLOSING_MINUTE

        showing_time = self.get_datetime()
        closing_on_showing_day = showing_time.replace(hour=closing_h, minute=closing_m)
        opening_on_showing_day = showing_time.replace(hour=opening_h, minute=opening_m)

        # Check whether closing is before opening e.g closing: 3:00, opening 9:00 or
        # after opening e.g closing: 23:00, opening 9:00
        closing_before_opening = closing_on_showing_day < opening_on_showing_day

        if closing_before_opening:
            if closing_on_showing_day <= showing_time < opening_on_showing_day:
                raise validation_error
        else:
            if showing_time < opening_on_showing_day or showing_time >= closing_on_showing_day:
                raise validation_error

        # Here showing start time is during cinema open hours.
        # Check if its duration doesn't exceed open hours.
        closing_after_showing_started = closing_on_showing_day

        if closing_after_showing_started < self.get_datetime():
            # Case when cinema closing is the next day of showing start.
            closing_after_showing_started = closing_after_showing_started + \
                                            timezone.timedelta(days=1)

        if self.get_end_time() > closing_after_showing_started:
            # Showing ends when cinema is close
            raise validation_error

    def clean(self):
        self.check_is_not_colliding()
        self.check_is_between_open_hours()

    def save(self, *args, **kwargs):
        self.full_clean()

        return super(Showing, self).save(*args, **kwargs)

    def get_datetime(self):
        tz = timezone.get_default_timezone()
        return self.when.astimezone(tz)

    def get_date(self):
        return self.get_datetime().date()

    def get_time(self):
        return self.get_datetime().time()

    def get_formatted_time(self):
        t = self.get_time()
        start_hour = t.hour
        start_minutes = t.minute

        return f'{start_hour:02}:{start_minutes:02}'

    def get_end_time(self):
        return self.get_datetime() + timezone.timedelta(minutes=self.movie.duration_in_minutes)

    def get_numerical_weekday(self):
        """Return week day where Monday is 0 and Sunday is 6"""
        return self.get_datetime().weekday()

    def get_weekday(self):
        return self.get_datetime().strftime('%A')

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
        start_time = self.get_formatted_time()
        start_date = self.get_date()
        weekday = self.get_weekday()

        return f'{self.movie.title} on {weekday} ({start_date} {start_time})'
