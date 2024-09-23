from django.contrib import admin
from .models import Specialist, Schedule, Slot, Appointment

# Register your models here.


class SpecialistAdmin(admin.ModelAdmin):
    # list_display = ('id', 'user__last_name', 'user__first_name', 'speciality', 'is_on_vacation', 'schedules')
    list_display = ('id', 'user__last_name', 'user__first_name', 'speciality', 'is_on_vacation')

    def schedule_list(self, obj):
        print('**********************')
        print(obj)
        print('**********************')
        print(obj.schedules.all())
        print('**********************')
        # return ', '.join([str(sch.date) for sch in obj.schedules.all()])
        return obj.schedules.all()


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'work_shift_start_time', 'work_shift_end_time', 'specialist')


class SlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'status', 'duration', 'reserved_for_user')
    list_filter = ('id', 'status')


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'slot')


admin.site.register(Specialist, SpecialistAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Slot, SlotAdmin)
admin.site.register(Appointment, AppointmentAdmin)
