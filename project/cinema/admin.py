from django.contrib import admin

from .models import Movie, Hall, Showing

admin.site.register(Movie)
admin.site.register(Hall)
admin.site.register(Showing)
