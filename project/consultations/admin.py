from django.contrib import admin
from .models import Specialist, Schedule, Slot

# Register your models here.


class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user__last_name', 'user__first_name', 'speciality', 'is_on_vacation', 'schedules')

    def schedule_list(self, obj):
        print('**********************')
        print(obj)
        print('**********************')
        print(obj.schedules.all())
        print('**********************')
        # return ', '.join([str(sch.date) for sch in obj.schedules.all()])
        return obj.schedules.all()


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('date', 'work_shift_start_time', 'work_shift_end_time',)


admin.site.register(Specialist, SpecialistAdmin)
admin.site.register(Schedule, ScheduleAdmin)
