from django.contrib import admin
from .models import Roulette, Group, Bonus, GoogleSheet


class BonusesInline(admin.TabularInline):
    model = Roulette.bonuses.through
    extra = 1  # Количество дополнительных полей, которые будут отображаться по умолчанию


class RouletteAdmin(admin.ModelAdmin):
    inlines = [BonusesInline]
    list_display = ('name', 'unique_id', 'google_table')
    exclude = ('bonuses',)  # Исключаем поле bonuses из формы Roulette, так как оно уже отображается в inlines


class BonusAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'type', 'probability')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('type', 'probability')


admin.site.register(GoogleSheet)
admin.site.register(Bonus, BonusAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Roulette, RouletteAdmin)
