import uuid

from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=256)
    director = models.CharField(max_length=256)
    year_of_production = models.IntegerField(verbose_name='year of production')
    type = models.CharField(max_length=80)
    duration_in_minutes = models.IntegerField(verbose_name='duration in minutes')
    description = models.TextField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(year_of_production__gte=1888) & models.Q(year_of_production__lt=3000),
                name='correct_year_of_production'
            ),
            models.CheckConstraint(
                check=models.Q(duration_in_minutes__gte=0),
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
    places = models.IntegerField(verbose_name='amount of places')

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(places__gte=0),
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
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_hour__gte=0) & models.Q(start_hour__lte=23),
                name='correct_start_hour'
            ),
            models.CheckConstraint(
                check=models.Q(start_minutes__gte=0) & models.Q(start_minutes__lte=59),
                name='correct_start_minutes'
            ),
        ]

    def get_time(self):
        start_hour = self.when.time().hour
        start_minutes = self.when.time().minute

        return f'{start_hour:2d}:{start_minutes:2d}'

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
