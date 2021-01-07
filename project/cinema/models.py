from django.db import models


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
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
    class Weekday(models.IntegerChoices):
        MONDAY = 1
        TUESDAY = 2
        WEDNESDAY = 3
        THURSDAY = 4
        FRIDAY = 5
        SATURDAY = 6
        SUNDAY = 7

    id = models.AutoField(primary_key=True)
    week_day_numerical = models.IntegerField(choices=Weekday.choices)
    start_hour = models.IntegerField()
    start_minutes = models.IntegerField()
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

    def __str__(self):
        start_hour = str(self.start_hour).zfill(2)
        start_minutes = str(self.start_minutes).zfill(2)
        weekday = self.Weekday(self.week_day_numerical).label

        return f'{self.movie.title} on {weekday} ({start_hour}:{start_minutes})'

    def get_formatted_time(self):
        start_hour = str(self.start_hour).zfill(2)
        start_minutes = str(self.start_minutes).zfill(2)

        return f'{start_hour}:{start_minutes}'
