from django.contrib import admin
from .models import info
from .models import wealth
from .models import sector

admin.site.register(info)
admin.site.register(wealth)
admin.site.register(sector)