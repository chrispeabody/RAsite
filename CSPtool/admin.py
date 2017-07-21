from django.contrib import admin

# Register your models here.
from .models import App, CSP, CSPLoc, Rating, Review, TrustScore, CatScore, CtrlGrpWeight

class ReviewAdmin(admin.ModelAdmin):
	list_display = ('CSP', 'dateMade', 'locMade', 'plaintext')

class RatingAdmin(admin.ModelAdmin):
	list_display = ('CSP', 'dateMade', 'locMade', 'type', 'value')

class CSPAdmin(admin.ModelAdmin):
	list_display = ('codename', 'name', 'avgRating', 'opPositive', 'opNeutral', 'opNegative')

class CatScoreAdmin(admin.ModelAdmin):
	list_display = ('CSP', 'type', 'value')

class TrustScoreAdmin(admin.ModelAdmin):
	list_display = ('user', 'CSP', 'value')

#admin.site.register(App)
admin.site.register(CSP, CSPAdmin)
#admin.site.register(CSPLoc)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(TrustScore, TrustScoreAdmin)
admin.site.register(CatScore, CatScoreAdmin)
admin.site.register(CtrlGrpWeight)