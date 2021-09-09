from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class ClinicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinician
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'
    
    def to_representation(self, instance):
        self.fields['patient'], self.fields['doctor']  =  PatientSerializer(many=False, read_only=True, required=False), ClinicianSerializer(many=False, read_only=True, required=False)
        return super(VisitSerializer, self).to_representation(instance)

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'
    
    def to_representation(self, instance):
        self.fields['visit'] = VisitSerializer(many=False, read_only=True, required=False)
        return super(BillSerializer, self).to_representation(instance)

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['patient'], self.fields['doctor']  =  PatientSerializer(many=False, read_only=True, required=False), ClinicianSerializer(many=False, read_only=True, required=False)
        return super(AppointmentSerializer, self).to_representation(instance)

class ChartRefractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartRefraction
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['visit'] = VisitSerializer(many=False, read_only=True, required=False)
        return super(ChartRefractionSerializer, self).to_representation(instance)

class ChartEyePressureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartEyePressure
        fields = '__all__'
    
    def to_representation(self, instance):
        self.fields['visit'] = VisitSerializer(many=False, read_only=True, required=False)
        return super(ChartEyePressureSerializer, self).to_representation(instance)

class ChartExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartExamination
        fields = '__all__'
    
    def to_representation(self, instance):
        self.fields['visit'] = VisitSerializer(many=False, read_only=True, required=False)
        return super(ChartExaminationSerializer, self).to_representation(instance)


class VisitSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['patient'], self.fields['doctor'], self.fields['chart_refraction'], self.fields['chart_eye_pressure'], self.fields['chart_examinations'], self.fields['bill'] = PatientSerializer(many=False, read_only=True, required=False), ClinicianSerializer(many=False, read_only=True, required=False), \
        ChartRefractionSerializer(many=True, read_only=True, required=False), ChartEyePressureSerializer(many=True, read_only=True, required=False), ChartExaminationSerializer(many=True, read_only=True, required=False), BillSerializer(many=True, read_only=True, required=False)
        return super(VisitSerializerDetail, self).to_representation(instance)

# query param serializers

class QPPatientSerializer(PatientSerializer):
    class Meta:
        model = Patient
        fields = ('age', 'is_active' , 'gender', 'is_registered',)
        extra_kwargs = {k:{'required': False, 'allow_null':True} for k in fields}

class QPClinicianSerializer(ClinicianSerializer):
    class Meta:
        model = Clinician
        fields = ('gender', 'age', 'is_active', 'ghana_post',)
        extra_kwargs = {k:{'required': False, 'allow_null':True} for k in fields}

class QPVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ('status', 'doctor', 'patient',)
        extra_kwargs = {k:{'required': False, 'allow_null':True} for k in fields}

class QPBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ('status', 'visit',)
        extra_kwargs = {k:{'required': False, 'allow_null':True} for k in fields}

class QPAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('status', 'patient', 'doctor',)
        extra_kwargs = {k:{'required': False, 'allow_null':True} for k in fields}

class QPChartRefractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartRefraction
        fields = ('rx_type', 'visit', 'clinician',)
        extra_kwargs = {k:{'required': False, 'allow_null':True} for k in fields}

class QPChartEyePressureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartEyePressure
        fields = ('visit', 'clinician',)
        extra_kwargs = {k:{'required': False, 'allow_null':True} for k in fields}

class QPChartExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartExamination
        fields = ('visit',)
        extra_kwargs = {k:{'required': False, 'allow_null':True} for k in fields}

'''
class UserSerializer(serializers.ModelSerializer):
    # iops
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class DoctorSerializer(serializers.ModelSerializer):
    # subjective_refractions

    class Meta:
        model = Doctor
        fields = '__all__'
    
class PatientSerializer(serializers.ModelSerializer):
    # screenings_iops = ScreeningIOPsSerializer(many=True, read_only=True, required=False)
    # subjective_refraction 
    # diagnosis_balance

    class Meta:
        model = Patient
        fields = '__all__'

class ScreeningHistoryAndSymptonsSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(many=False, read_only=True, required=False)
    
    class Meta:
        model = ScreeningHistoryAndSymptons
        fields = '__all__'

class ScreeningCurrentSpecRxSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(many=False, read_only=True, required=False)

    class Meta:
        model = ScreeningCurrentSpecRx
        fields = '__all__'

class ScreeningIOPsSerializer(serializers.ModelSerializer):
    screener = UserSerializer(many=False, read_only=True)
    patient = PatientSerializer(many=False, read_only=True, required=False)

    class Meta:
        model = ScreeningIOPs
        fields = '__all__'

class ScreeningObjectiveRefractionRxSerializer(serializers.ModelSerializer):
    screener = UserSerializer(many=False, read_only=True)
    patient = PatientSerializer(many=False, read_only=True, required=False)

    class Meta:
        model = ScreeningObjectiveRefractionRx
        fields = '__all__'

class DiagnosisSubjectiveRefractionRxSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(many=False, read_only=True, required=False)
    doctor = DoctorSerializer(many=False, read_only=True, required=False)

    class Meta:
        model = DiagnosisSubjectiveRefractionRx
        fields = '__all__'

class DiagnosisBalanceSerializer(serializers.ModelSerializer):
    # doctor
    # patient

    class Meta:
        model = DiagnosisBalance
        fields = '__all__'

class DiagnosisOculomotorSerializer(serializers.ModelSerializer):
    # doctor
    # patient

    class Meta:
        model = DiagnosisOculomotor
        fields = '__all__'

class FinalPrescriptionRxSerializer(serializers.ModelSerializer):
    # doctor
    # patient

    class Meta:
        model = FinalPrescriptionRx
        fields = '__all__'
'''