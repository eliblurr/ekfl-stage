from django.utils.html import format_html
from django.utils.http import urlencode
from django.contrib import admin
from django.urls import reverse
from .models import *

from .forms import PatientForm

admin.site.site_header = 'Ekuful Eyecare Practice'

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ("id", "uuid", "amount", "status", "visits")
    search_fields = ("amount",)
    list_filter = ("status",)

    def visits(self, obj):
        obj = obj.visit
        url = (reverse("admin:clinic_visit_changelist") + f"?id={obj.id}")
        return format_html(f'<a href="{url}">{obj.date} {obj.start_time}</a>',)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    form = PatientForm
    list_display = ("uuid", "tr_no", "first_name", "other_names", "last_name", "gender", "date_of_birth", "email", "location", "ghana_post", "last_eye_test", "remarks", "is_active",)
    search_fields = ("first_name", "other_names", "last_name", "email",)
    list_filter = ("is_active", "gender",)

@admin.register(Clinician)
class ClinicianAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "other_name", "last_name", "category", "dob", "cellphone_1", "cellphone_2", "address", "email", "ghana_post", "category", "gender", "is_active",)
    search_fields = ("first_name", "other_name", "last_name", "email",)
    list_filter = ("is_active", "gender", "category",)
    
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "patients", "doctors", "start_time", "end_time", "status",)
    search_fields = ("patients", "doctors",)
    list_filter = ("status",)

    def patients(self, obj):
        obj = obj.patient
        url = (reverse("admin:clinic_patient_changelist") + f"?id={obj.id}")
        return format_html(f'<a href="{url}">{obj.first_name} {obj.last_name}</a>',)

    def doctors(self, obj):
        obj = obj.doctor
        url = (reverse("admin:clinic_clinician_changelist") + f"?id={obj.id}")
        return format_html(f'<a href="{url}">Dr.{obj.first_name} {obj.last_name}</a>',)

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("uuid", "patients", "doctors", "start_time", "date", "status")
    search_fields = ("patients", "doctors",)
    list_filter = ("date",)

    def patients(self, obj):
        obj = obj.patient
        url = (reverse("admin:clinic_patient_changelist") + f"?id={obj.id}")
        return format_html(f'<a href="{url}">{obj.first_name} {obj.last_name}</a>',)

    def doctors(self, obj):
        obj = obj.doctor
        url = (reverse("admin:clinic_clinician_changelist") + f"?id={obj.id}")
        return format_html(f'<a href="{url}">Dr.{obj.first_name} {obj.last_name}</a>',)

@admin.register(ChartRefraction)
class ChartRefractionAdmin(admin.ModelAdmin):
    list_display = ("uuid", "right_sph", "right_cyl", "right_axis", "right_prism", "right_va", "left_sph", "left_cyl", "left_axis", "left_prism", "left_va", "bin_va", "add", "pd", "visits", "rx_type")
    search_fields = ("patients", "doctors",)

    def visits(self, obj):
        obj = obj.visit
        url = (reverse("admin:clinic_visit_changelist") + f"?id={obj.id}")
        return format_html(f'<a href="{url}">{obj.date} {obj.start_time}</a>',)

@admin.register(ChartEyePressure)
class ChartEyePressureAdmin(admin.ModelAdmin):
    list_display = ("uuid", "right_iops", "right_fields", "left_iops", "left_fields", "drug_concentraion", "time", "visits")
    search_fields = ("right_iops", "right_fields", "left_iops", "left_fields", "drug_concentraion",)

    def visits(self, obj):
        obj = obj.visit
        url = (reverse("admin:clinic_visit_changelist") + f"?id={obj.id}")
        return format_html(f'<a href="{url}">{obj.date} {obj.start_time}</a>',)

@admin.register(ChartExamination)
class ChartExaminationAdmin(admin.ModelAdmin):
    list_display = ("uuid", "oculomotor_balance", "amsler", "color_vision", "right_ant", "right_post", "right_cpu_disc", "left_ant", "left_post", "right_cpu_disc", "clinical_advice_remarks", "recall", "visits")
    search_fields = ("oculomotor_balance", "amsler", "color_vision", "right_ant", "right_post", "right_cpu_disc", "left_ant", "left_post", "right_cpu_disc",)

    def visits(self, obj):
        obj = obj.visit
        url = (reverse("admin:clinic_visit_changelist") + f"?id={obj.id}")
        return format_html(f'<a href="{url}">{obj.date} {obj.start_time}</a>',)