from django.contrib import admin

# Register your models here.
from .models import App, CSP, CSPLoc, Rating, Review, TrustScore

class ReviewAdmin(admin.ModelAdmin):
	list_display = ('CSP', 'dateMade', 'locMade', 'plaintext')

class RatingAdmin(admin.ModelAdmin):
	list_display = ('CSP', 'dateMade', 'locMade', 'value')

admin.site.register(App)
admin.site.register(CSP)
admin.site.register(CSPLoc)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(TrustScore)