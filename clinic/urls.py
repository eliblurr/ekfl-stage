from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from django.urls import path, re_path
from .views import *

app_name = 'clinic'

r_opt = r'(?:/(?P<id>[0-9]+))?(?:/(?P<search>[a-zA-Z]+))?(?:/(?P<value>[a-zA-Z]+))?(?:/(?P<offset>[0-9]+))?(?:/(?P<limit>[0-9]+))?(?:/(?P<detail>[0-9]+))?(?:/(?P<date>[0-9]{4}-((1[0-2])|([1-9]))-([1-2][0-9])|([1-9])|(3[0-1])))?(?:/(?P<count>[0-9]+))?'
r_c = lambda ls : r'(?P<child>'+ r'|'.join(ls) + ')$' + r'(?:/(?P<search>[a-zA-Z]+))?(?:/(?P<value>[a-zA-Z]+))?(?:/(?P<offset>[0-9]+))?(?:/(?P<limit>[0-9]+))?(?:/(?P<start>[0-9]{4}-((1[0-2])|([1-9]))-([1-2][0-9])|([1-9])|(3[0-1])))?(?:/(?P<end>[0-9]{4}-((1[0-2])|([1-9]))-([1-2][0-9])|([1-9])|(3[0-1])))?'
l_c = r'^(?P<model>(' + r'|'.join(c_s.keys()) + '))' + r'/report(/)?' + r_opt
r_id = r'(?P<id>\w+)'

urlpatterns = [
    path('', index, name='index'),
    re_path(r'authenticate(/)?', Authenticate.as_view()),
    re_path(l_c, aggregate, name='aggregate_on_models'),

    re_path(r'^visits/'+r_id+'/'+r_c(c_s.keys()), VisitView.as_view(),  name='vst_id_mndtry_chld'),
    re_path(r'^doctors/'+r_id+'/'+r_c(c_s.keys()), VisitView.as_view(),  name='doc_id_mndtry_chld'),
    re_path(r'^patients/'+r_id+'/'+r_c(c_s.keys()), PatientView.as_view(),  name='pat_id_mndtry_chld'),
    re_path(r'^bills/'+r_id, BillView.as_view(), name='bil_id_mndtry'),
    re_path(r'^visits/'+r_id, VisitView.as_view(), name='vis_id_mndtry'),
    re_path(r'^patients/'+r_id, PatientView.as_view(), name='pat_id_mndtry'),
    re_path(r'^doctors/'+r_id, ClinicianView.as_view(), name='doc_id_mndtry'),
    path('appointments/available-slots', available_slots, name='available_slots'),
    path('appointments/available-slots/', available_slots, name='available_slots'),
    re_path(r'^appointments/'+r_id, AppointmentView.as_view(), name='apv_id_mndtry'),
    re_path(r'^chart-examination/'+r_id, ChartExaminationView.as_view(), name='che_id_mndtry'),
    re_path(r'^chart-eye-pressure/'+r_id, ChartEyePressureView.as_view(), name='cep_id_mndtry'),
    re_path(r'^chart-refraction/'+r_id, ChartRefractionView.as_view(), name='chr_id_mndtry'),

    re_path(r'^bills(/)?'+r_opt, BillView.as_view(), name='bil_opt_params'),
    re_path(r'^visits(/)?'+r_opt, VisitView.as_view(), name='vis_opt_params'),
    re_path(r'^patients(/)?'+r_opt, PatientView.as_view(), name='pat_opt_params'),
    re_path(r'^doctors(/)?'+r_opt, ClinicianView.as_view(), name='doc_opt_params'),
    re_path(r'^appointments(/)?'+r_opt, AppointmentView.as_view(), name='apv_opt_params'),
    re_path(r'^chart-examination(/)?'+r_opt, ChartExaminationView.as_view(), name='che_opt_params'),
    re_path(r'^chart-eye-pressure(/)?'+r_opt, ChartEyePressureView.as_view(), name='cep_opt_params'),
    re_path(r'^chart-refraction(/)?'+r_opt, ChartRefractionView.as_view(), name='chr_opt_params'),

    path('dashboard/', dashboard, name='dashboard_data'),
    path('appointments/available-slots/', available_slots, name='available_slots'),
    path('openapi', get_schema_view(title="Eye Clinic API", description="", version="0.0.1" ), name='openapi-schema'),
    # Route TemplateView to serve Swagger UI template. * Provide `extra_context` with view name of `SchemaView`.
    path('swagger-ui/', TemplateView.as_view(template_name='swagger-ui.html', extra_context={'schema_url':'openapi-schema'} ), name='swagger-ui'),

]



'''
    # l_c = r'^' + '(' +r'|'.join(c_s.keys()) + ')' + r'/aggregate(/)?' + r_opt
    # pat_switcher = {'visits':VisitView, 'appointments':AppointmentView}
    # pat_switcher = {'visits':Visit, 'appointments':Appointment}
    # patient_re = '(?:'+'|'.join(pat_switcher.keys())+')'

    # re_path(r'^patients/'+r_id+r'/(?P<child>'+r'|'.join(pat_switcher.keys()+r')(/)?', PatientView.as_view(), name='pat_id_mndtry_chld')
    
    # re_path(r'^patients/'+r_id+r'/'+patient_re+r'(/)?'+r_opt, PatientView.as_view(), name='pat_id_chd_mndtry'),
    path('bulma-admin/', admin_index, name='index'),
    re_path(r'bulma-admin/doctors', DoctorAdminView.get, name='doctor_home'),
    re_path(r'authenticate(/)?', Authenticate.as_view()),
    re_path(r'^doctors/'+r_id, DoctorView.as_view(), name='doc_id_mndtry'),
    re_path(r'^patients/'+r_id, PatientView.as_view(), name='pat_id_mndtry'),
    re_path(r'^screening-iops/'+r_id, ScreeningIOPsView.as_view(), name='sio_id_mndtry'),
    re_path(r'^diagnosis-balance/'+r_id, DiagnosisBalanceView.as_view(), name='dgb_id_mndtry'),
    re_path(r'^diagnosis-oculomotor/'+r_id, DiagnosisOculomotorView.as_view(), name='dgo_id_mndtry'),
    re_path(r'^final-prescription-rx/'+r_id, FinalPrescriptionRxView.as_view(), name='fpr_id_mndtry'),
    re_path(r'^screening-current-spec-rx/'+r_id, ScreeningCurrentSpecRxView.as_view(), name='scs_id_mndtry'),
    re_path(r'^screening-history-and-symptoms/'+r_id, ScreeningHistoryAndSymptonsView.as_view(), name='shs_id_mndtry'),
    re_path(r'^screening-objective-refraction-rx/'+r_id, ScreeningObjectiveRefractionRxView.as_view(), name='sor_id_mndtry'),
    re_path(r'^diagnosis-subjective-refraction-rx/'+r_id, DiagnosisSubjectiveRefractionRxView.as_view(), name='dsr_id_mndtry'),

    re_path(r'^doctors(/)?'+r_opt, DoctorView.as_view(), name='doc_opt_params'),
    re_path(r'^patients(/)?'+r_opt, PatientView.as_view(), name='pat_opt_params'), 
    re_path(r'^screening-iops(/)?'+r_opt, ScreeningIOPsView.as_view(), name='sio_opt_params'),
    re_path(r'^diagnosis-balance(/)?'+r_opt, DiagnosisBalanceView.as_view(), name='dgb_opt_params'),
    re_path(r'^diagnosis-oculomotor(/)?'+r_opt, DiagnosisOculomotorView.as_view(), name='dgo_opt_params'),
    re_path(r'^final-prescription-rx(/)?'+r_opt, FinalPrescriptionRxView.as_view(), name='fpr_opt_params'),
    re_path(r'^screening-current-spec-rx(/)?'+r_opt, ScreeningCurrentSpecRxView.as_view(), name='scs_opt_params'),
    re_path(r'^screening-history-and-symptoms(/)?'+r_opt, ScreeningHistoryAndSymptonsView.as_view(), name='shs_opt_params'),
    re_path(r'^screening-objective-refraction-rx(/)?'+r_opt, ScreeningObjectiveRefractionRxView.as_view(), name='sor_opt_params'),
    re_path(r'^diagnosis-subjective-refraction-rx(/)?'+r_opt, DiagnosisSubjectiveRefractionRxView.as_view(), name='dsr_opt_params'),
'''