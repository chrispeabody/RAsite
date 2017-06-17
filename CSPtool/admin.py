from django.contrib import admin

# Register your models here.
from .models import App, CSP, CSPLoc, Rating, Review

admin.site.register(App)
admin.site.register(CSP)
admin.site.register(CSPLoc)
admin.site.register(Rating)
admin.site.register(Review)