from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated, SAFE_METHODS
from .utils import date_range, combine_dt_time, get_free_slots, is_overlapped
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse, Http404, JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.core.exceptions import FieldError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
import json, datetime, django
from .serializers import *
from .models import *
import sys

from django.db.utils import IntegrityError

def index(request):
    return HttpResponse('Ekuful EyeCare API link', status=200)

@api_view(['GET'])
@permission_classes([AllowAny,])
def available_slots(request):
    start, end, duration, doctor_id = request.GET.get('start'), request.GET.get('end'), request.GET.get('duration'), request.GET.get('doctor_id')
    if not (start and end):
        return HttpResponse(json.dumps({'detail':'start and end date range required'}), status=422, content_type='application/json')

    try:
        dt_range = date_range(start, end)
    except:
        return HttpResponse(json.dumps({'detail':'date format must match YYYY-MM-DD'}), status=422, content_type='application/json')

    slots = {}

    for date in dt_range:
        appointments = Appointment.objects.all().filter(date__exact=date, status__in=['booked', 'confirmed', 'pending'])
        if doctor_id:
            appointments = appointments.filter(doctor_id__exact=doctor_id)
        start_time, end_time = datetime.time(hour=8, minute=0, second=0), datetime.time(hour=17, minute=0, second=0)
        start_time, end_time = combine_dt_time(date, start_time), combine_dt_time(date, end_time)
        appointments_bk = [(combine_dt_time(date, item["start_time"]), combine_dt_time(date, item["end_time"]), ) for item in list(appointments.values())]
        free_slots = get_free_slots((start_time, end_time), appointments_bk, datetime.timedelta(hours=int(duration)) if duration else datetime.timedelta(hours=1))
        slots.update({f"{date}":free_slots})
    return Response(slots)

@api_view(['GET'])
@permission_classes([AllowAny,])
def aggregate(request, model=None):
    start, end, dt_field, m = request.GET.get('start'), request.GET.get('end'), request.GET.get('dt_field'), c_s.get(model, None)
    qp = m.qp_serializer(data=request.query_params, partial=True)
    
    qp.is_valid(raise_exception=True)

    data = qp.data
    data = {k:v for k,v in data.items() if v is not None}

    base = m.model.objects.all().filter(**{f'{k}__exact':v for k,v in data.items()})
    
    if start and end and dt_field:
        start, end = datetime.strptime(start, '%Y-%m-%d'), datetime.strptime(end, '%Y-%m-%d')
        base = base.filter(**{f'{dt_field}__gte':start, f'{dt_field}__lte':end})
    return Response({"total":base.count()})

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def dashboard(request, model=None):
    user = request.user
    hours = request.GET.get('hours', 24)

    try:
        dt = datetime.datetime.now() - datetime.timedelta(hours = int(hours))
    except:
        return Response({'detail':'hours value to large or is not a valid int'}, status=422)

    patients = {
        'total': Patient.objects.all().count(),
        'registered': Patient.objects.all().filter(is_registered__exact=True).count(),
        'non_registered': Patient.objects.all().filter(is_registered__exact=False).count(),
    }

    appointments = {
        'total': Appointment.objects.all().count(),
        'confirmed': Appointment.objects.all().filter(status__exact='confirmed', date__gte=dt).count(),
        'cancelled': Appointment.objects.all().filter(status__exact='cancelled', date__gte=dt).count(),
        'pending': Appointment.objects.all().filter(status__exact='pending', date__gte=dt).count(),
        'honoured': Appointment.objects.all().filter(status__exact='honoured', date__gte=dt).count(),
        'booked': Appointment.objects.all().filter(status__exact='booked', date__gte=dt).count(),
    }

    screenings = {
        'chart_refraction':{
            'total': ChartRefraction.objects.all().count(),
        },
        'chart_eye_pressure':{
            'total': ChartEyePressure.objects.all().count(),
        },
        'chart_examination':{
            'total': ChartExamination.objects.all().count(),
        }
    }

    visits = {
        'total': Visit.objects.all().count(),
        'screened': Visit.objects.all().filter(status__exact='screened', date__gte=dt, ).count(),
        'examined': Visit.objects.all().filter(status__exact='examined', date__gte=dt).count(),
        'registered': Visit.objects.all().filter(status__exact='registered', date__gte=dt).count(),
    }
    
    if user.role == 'doctor':
        visits.update(
            {   
                'total': Visit.objects.all().filter(id=user.id).count(),
                'screened': Visit.objects.all().filter(status__exact='screened', date__gte=dt, id=user.id).count(),
                'examined': Visit.objects.all().filter(status__exact='examined', date__gte=dt, id=user.id).count(),
                'registered': Visit.objects.all().filter(status__exact='registered', date__gte=dt, id=user.id).count(),
            }
        )
    if user.role == 'screener':
        screenings.update(
            {
                'chart_refraction':{
                    'total': ChartRefraction.objects.all().filter(id=user.id).count(),
                },
                'chart_eye_pressure':{
                    'total': ChartEyePressure.objects.all().filter(id=user.id).count(),
                },
                'chart_examination':{
                    'total': ChartExamination.objects.all().filter(id=user.id).count(),
                }
            }
        )
   
    return Response({'patients':patients, 'appointments':appointments, 'visits':visits, 'screenings':screenings})

class Authenticate(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class Views:
    def get_object(self, id):
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            raise Http404

    def get(self, request, id=0, child=None, count=None):        
        id, limit, offset, value, search, child = id or request.GET.get('id'), request.GET.get('limit', 100),  request.GET.get('offset', 0), request.GET.get('value', None), request.GET.get('search', None), c_s.get(child, None)
        try:
            base = child.model.objects.all().filter(**{self.alias+'__pk__exact':id}) if id and child else self.get_object(id) if id else self.model.objects.all()
        except FieldError:
            return HttpResponse(json.dumps({'detail':f'{child.alias} is invalid child for {self.alias}'}), status=400, content_type='application/json')
        serializer = child.serializer if id and child else self.serializer
        if search and value:
            try:
                base = base.filter(**{search+'__icontains':value})
            except:
                pass
        base = serializer(base, many=not(id and not child))
        return Response(base.data)

    def post(self, request):
        try:
            serializer = self.serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=201)
        except IntegrityError as e:
            return HttpResponse(json.dumps({'detail':f'{e}'}), status=500, content_type='application/json')

    def put(self, request, id):
        try:
            serializer = self.serializer(self.get_object(id), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=202)
        except IntegrityError as e:
            return HttpResponse(json.dumps({'detail':f'{e}'}), status=500, content_type='application/json')

    def patch(self, request, id):
        try:
            serializer = self.serializer(self.get_object(id), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=202)
        except IntegrityError as e:
            return HttpResponse(json.dumps({'detail':f'{e}'}), status=500, content_type='application/json')
            
    def delete(self, request, id):
        self.get_object(id).delete()
        return Response(status=204)

class BillView(APIView, Views):
    permission_classes = (AllowAny, )
    serializer = BillSerializer
    qp_serializer = QPBillSerializer
    model = Bill
    alias = model.__name__.lower()

class PatientView(APIView, Views):
    permission_classes = (AllowAny, )
    serializer = PatientSerializer
    qp_serializer = QPPatientSerializer
    model = Patient
    alias = model.__name__.lower()

class ClinicianView(APIView, Views):
    permission_classes = (AllowAny, )
    serializer = ClinicianSerializer
    qp_serializer = QPClinicianSerializer
    model = Clinician
    alias = model.__name__.lower()

# add opening and closing hours for doctors
# check for conflicts

class AppointmentView(APIView, Views):
    permission_classes = (AllowAny, )
    serializer = AppointmentSerializer
    qp_serializer = QPAppointmentSerializer
    model = Appointment
    alias = model.__name__.lower()

    def post(self, request):    
        start_time = datetime.datetime.strptime(request.data['start_time'], "%H:%M:%S").time()
        end_time = datetime.datetime.strptime(request.data['end_time'], "%H:%M:%S").time() 
        appointments = Appointment.objects.all().filter(
            date__exact=datetime.datetime.strptime(request.data['date'], '%Y-%m-%d'), 
            doctor_id__exact=request.data['doctor'], status__in=['booked', 'confirmed', 'pending']
        )
        for appointment in appointments:
            if is_overlapped((appointment.start_time, appointment.end_time), (start_time, end_time)):
                return HttpResponse(json.dumps({'detail':'timeslots not available'}), status=409, content_type='application/json')
        return super().post(request)
        
    def put(self, request, id):
        appointment = self.get_object(id)
        if request.data.get('status')=='honoured':
            if appointment.status=='honoured':
                return JsonResponse({'message': 'appointment already honoured'}, status=400)
            new_visit = Visit(patient=appointment.patient,  doctor=appointment.doctor, date = datetime.date.today(), start_time =  datetime.datetime.now().time())
            with django.db.transaction.atomic():
                appointment.status = 'honoured'
                appointment.save()
                new_visit.save()
                return JsonResponse({'visit_id':new_visit.id})

        serializer = self.serializer(self.get_object(id), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=202)

    def get(self, request, id=0, child=None):
        id, limit, offset, value, search, child, start, end, date = id or request.GET.get('id'), request.GET.get('limit', 100),  request.GET.get('offset', 0), request.GET.get('value', None), request.GET.get('search', None), c_s.get(child, None), request.GET.get('start', None), request.GET.get('end', None), request.GET.get('date', None)
        try:
            base = child.model.objects.all().filter(**{self.alias+'__pk__exact':id}) if id and child else self.get_object(id) if id else self.model.objects.all()
        except FieldError:
            return HttpResponse(json.dumps({'detail':f'{child.alias} is invalid child for {self.alias}'}), status=400, content_type='application/json')
        serializer = child.serializer if id and child else self.serializer
        if search and value:
            try:
                base = base.filter(**{search+'__icontains':value})
            except:
                pass
        if (start and end) and (start < end):
            try:
                start, end = start.split('-'), end.split('-')
                start = list(map(int, start))
                end = list(map(int, end))
                base = base.filter(date__gte=datetime.date(start[0], start[1], start[2]), date__lte=datetime.date(end[0], end[1], end[2]))
            except:
                print(sys.exc_info())
                pass
        elif date:
            try:
                date = date.split('-')
                date = list(map(int, date))
                base = base.filter(date__exact=datetime.date(date[0], date[1], date[2]))
            except:
                pass
        base = serializer(base, many=not(id and not child))
        return Response(base.data)        

class VisitView(APIView, Views):
    permission_classes = (AllowAny, )
    # permission_classes = (IsAuthenticated|ReadOnly,) 
    serializer = VisitSerializer
    qp_serializer = QPVisitSerializer
    detail_serializer = VisitSerializerDetail
    model = Visit
    alias = model.__name__.lower()

    def get(self, request, id=0, child=None):
        id, limit, offset, value, search, child, tr_no, start, end, name, detail = id or request.GET.get('id'), request.GET.get('limit', 100),  request.GET.get('offset', 0), request.GET.get('value', None), request.GET.get('search', None), c_s.get(child, None), request.GET.get('tr_no', None), request.GET.get('start', None), request.GET.get('end', None), request.GET.get('name', None), request.GET.get('detail', None)
        try:
            base = child.model.objects.all().filter(**{self.alias+'__pk__exact':id}) if id and child \
            else self.model.objects.all().filter(patient__tr_no__exact=tr_no) if tr_no \
            else self.model.objects.all().filter(Q(patient__first_name__icontains=name)|Q(patient__other_names__icontains=name)|Q(patient__last_name__icontains=name)) if name \
            else self.get_object(id) if id \
            else self.model.objects.all()
        except FieldError:
            return HttpResponse(json.dumps({'detail':f'{child.alias} is invalid child for {self.alias}'}), status=400, content_type='application/json')
        serializer = child.serializer if id and child else self.detail_serializer if detail=='full' else self.serializer
        if search and value:
            try:
                base = base.filter(**{search+'__icontains':value})
            except:
                pass
        if (start and end) and (start < end):
            try:
                start, end = start.split('-'), end.split('-')
                start = list(map(int, start))
                end = list(map(int, end))
                base = base.filter(date__gte=datetime.date(start[0], start[1], start[2]), date__lte=datetime.date(end[0], end[1], end[2]))
            except:
                pass 
        base = serializer(base, many=not(id and not child))
        return Response(base.data)

class ChartRefractionView(APIView, Views):
    permission_classes = (AllowAny, )
    # permission_classes = (IsAuthenticated|ReadOnly,) 
    serializer = ChartRefractionSerializer
    qp_serializer = QPChartRefractionSerializer
    model = ChartRefraction
    alias = model.__name__.lower()

class ChartEyePressureView(APIView, Views):
    permission_classes = (AllowAny, )
    # permission_classes = (IsAuthenticated|ReadOnly,) 
    serializer = ChartEyePressureSerializer
    qp_serializer = QPChartEyePressureSerializer
    model = ChartEyePressure
    alias = model.__name__.lower()

class ChartExaminationView(APIView, Views):
    permission_classes = (AllowAny, )
    # permission_classes = (IsAuthenticated|ReadOnly,) 
    serializer = ChartExaminationSerializer
    qp_serializer = QPChartExaminationSerializer
    model = ChartExamination
    alias = model.__name__.lower()

c_s = {'visits':VisitView, 'appointments':AppointmentView, 'bills':BillView, 'doctors':ClinicianView, 'chart-examination':ChartExaminationView, 'chart-eye-pressure':ChartEyePressureView, 'chart-refraction':ChartRefractionView, 'patients':PatientView} 

'''
class DoctorView(APIView, Views):
    permission_classes = (IsAuthenticated,) 
    serializer = DoctorSerializer
    model = Doctor

class PatientView(APIView, Views):
    permission_classes = (IsAuthenticated|ReadOnly,) 
    serializer = PatientSerializer
    model = Patient

class ScreeningHistoryAndSymptonsView(APIView, Views):
    permission_classes = (IsAuthenticated|ReadOnly,) 
    serializer = ScreeningHistoryAndSymptonsSerializer
    model = ScreeningHistoryAndSymptons

class ScreeningCurrentSpecRxView(APIView, Views):
    permission_classes = (IsAuthenticated|ReadOnly,) 
    serializer = ScreeningCurrentSpecRxSerializer
    model = ScreeningCurrentSpecRx

class ScreeningIOPsView(APIView, Views):
    permission_classes = (IsAuthenticated|ReadOnly,) 
    serializer = ScreeningIOPsSerializer
    model = ScreeningIOPs

class ScreeningObjectiveRefractionRxView(APIView, Views):
    permission_classes = (IsAuthenticated|ReadOnly,) 
    serializer = ScreeningObjectiveRefractionRxSerializer
    model = ScreeningObjectiveRefractionRx

class DiagnosisSubjectiveRefractionRxView(APIView, Views):
    permission_classes = (IsAuthenticated|ReadOnly,) 
    serializer = DiagnosisSubjectiveRefractionRxSerializer
    model = DiagnosisSubjectiveRefractionRx

class DiagnosisBalanceView(APIView, Views):
    permission_classes = (IsAuthenticated|ReadOnly,) 
    serializer = DiagnosisBalanceSerializer
    model = DiagnosisBalance

class DiagnosisOculomotorView(APIView, Views):
    permission_classes = (IsAuthenticated|ReadOnly,) 
    serializer = DiagnosisOculomotorSerializer
    model = DiagnosisOculomotor

class FinalPrescriptionRxView(APIView, Views):
    permission_classes = (IsAuthenticated|ReadOnly,) 
    serializer = FinalPrescriptionRxSerializer
    model = FinalPrescriptionRx

def test(request):
    start_date, end_date = request.GET.get('start_date'), request.GET.get('end_date')
    appointments = Appointment.objects.all()
    # .filter(date__range=[start_date, end_date],status__in=['booked','confirmed'])
    # a = [ ( datetime.datetime.combine(apt.date, apt.start_time), datetime.datetime.combine( apt.date, apt.end_time) ) for apt in appointments]
    return JsonResponse({'message': 'appointments'})
'''