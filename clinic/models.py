
from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from .utils import gen_tr_no
import uuid

'''
class Doctor(models.Model):
    #user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    gender_choices = (('male', 'male'),
                      ('female', 'female'),
                       ('other', 'other'))
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=59)
    other_name = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(choices=gender_choices, max_length=7)
    dob = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message=
                                    "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    cellphone_1 = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    cellphone_2 = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list

    address = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    ghana_post = models.CharField(max_length=50,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class Patient(models.Model):
    #id = models.models.IntegerField(unique=True)
    #auto_increment_id = models.AutoField(primary_key=True)
    gender_choices = (('male', 'male'),
                      ('female', 'female'),
                      ('other', 'others'))
    tr_no = models.CharField( max_length=50,null=False,blank=False,unique=True)
    first_name = models.CharField(max_length=256,blank=False,null=False)
    other_names = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=255,blank=False,null=False)
    gender = models.CharField(choices=gender_choices, max_length=7)
    date_of_birth = models.DateField(null=True,blank=True)
    age = models.IntegerField(null=True, blank=True)
    email = models.EmailField( max_length=254,null=True)
    location  = models.CharField(max_length=60)
    ghana_post = models.CharField(max_length=50,null=True,blank=True)
    last_eye_test = models.DateField(auto_now=False, auto_now_add=False)
    remarks = models.TextField(null=True,blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    #created_by = models.ForeignKey(User, related_name='patient_entries', on_delete=models.PROTECT)
    #updated_by = models.ForeignKey(User, related_name='patient_entries', on_delete=models.PROTECT)
    #date_added = models.DateTimeField(auto_now_add=True)
    #date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return '{0} {1} {2}'.format(self.first_name, self.other_names, self.last_name)

    def get_absolute_url(self):
        pass
        #return reverse('clinic:patient-detail', args=[str(self.id)])

class ScreeningHistoryAndSymptons(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.SET_NULL, null=True)
    history_and_symptons = models.TextField()

class ScreeningCurrentSpecRx(models.Model):
    reading_choices = (
        ('first','first'),
        ('second','second')
    )
    reading = models.CharField( max_length=8,choices=reading_choices)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    right_sph = models.CharField(max_length=6, null=True, blank=True)
    right_cyl = models.CharField(max_length=6, null=True, blank=True)
    right_axis= models.CharField(max_length=6, null=True, blank=True)
    right_prism = models.CharField(max_length=6, null=True, blank=True)
    right_va = models.CharField(max_length=6, null=True, blank=True)

    left_sph = models.CharField(max_length=6, null=True, blank=True)
    left_cyl = models.CharField(max_length=6, null=True, blank=True)
    leftt_axis= models.CharField(max_length=6, null=True, blank=True)
    left_prism = models.CharField(max_length=6, null=True, blank=True)
    left_va = models.CharField(max_length=6, null=True, blank=True)

    #common for both eyes
    bin_va = models.CharField(max_length=6, null=True, blank=True)
    add = models.CharField(max_length=6, null=True, blank=True)
    date = models.DateField( auto_now=False, auto_now_add=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

class ScreeningIOPs(models.Model):
    screener = models.ForeignKey("auth.User", on_delete=models.PROTECT,related_name="iops")
    patient = models.ForeignKey('Patient', on_delete=models.PROTECT, null=True,related_name="screenings_iops")
    right_iops = models.CharField(max_length=6, null=True, blank=True)
    right_fields = models.CharField(max_length=6, null=True, blank=True)
    left_iops = models.CharField(max_length=6, null=True, blank=True)
    left_fields = models.CharField(max_length=6, null=True, blank=True)
    time = models.DateTimeField( auto_now=False, auto_now_add=False)
    drug_concentraion = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

class ScreeningObjectiveRefractionRx(models.Model):
    obj_choices = (
        ('OBJ1','OBJ1'),
        ('OBJ2','OBJ2')
    )
    screener = models.ForeignKey("auth.User", on_delete=models.PROTECT)
    patient = models.ForeignKey('Patient', on_delete=models.PROTECT, null=True)
    objective = models.CharField( max_length=8,choices=obj_choices)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    right_sph = models.CharField(max_length=6, null=True, blank=True)
    right_cyl = models.CharField(max_length=6, null=True, blank=True)
    right_axis= models.CharField(max_length=6, null=True, blank=True)
    right_pd = models.CharField(max_length=6, null=True, blank=True)

    left_sph = models.CharField(max_length=6, null=True, blank=True)
    left_cyl = models.CharField(max_length=6, null=True, blank=True)
    left_axis= models.CharField(max_length=6, null=True, blank=True)
    left_pd = models.CharField(max_length=6, null=True, blank=True)
    date = models.DateField( auto_now=False, auto_now_add=False)


    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

class DiagnosisSubjectiveRefractionRx(models.Model):
    doctor = models.ForeignKey("Doctor", on_delete=models.PROTECT,
                                related_name="subjective_refractions")
    patient = models.ForeignKey('Patient', on_delete=models.PROTECT, null=True,
                related_name="subjective_refraction")

class DiagnosisBalance(models.Model):
    doctor = models.ForeignKey("Doctor", on_delete=models.PROTECT)
    patient = models.ForeignKey('Patient', on_delete=models.PROTECT, null=True,related_name="diagnosis_balance")
    ocolomotor_balance = models.CharField( max_length=50)
    amsler = models.CharField( max_length=50)
    color_vision = models.CharField( max_length=50)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

class DiagnosisOculomotor(models.Model):
    doctor = models.ForeignKey("Doctor", on_delete=models.PROTECT)
    patient = models.ForeignKey('Patient', on_delete=models.PROTECT, null=True)
    right_ant = models.CharField(max_length=12)
    right_post = models.CharField( max_length=50)
    right_cpu_disc = models.CharField( max_length=50)
    left_ant = models.CharField(max_length=12)
    left_post = models.CharField( max_length=50)
    right_cpu_disc = models.CharField( max_length=50)


    #created = models.DateTimeField(auto_now_add=True,default=timezone.now())
    #updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

class FinalPrescriptionRx(models.Model):
    doctor = models.ForeignKey("Doctor", on_delete=models.PROTECT)
    patient = models.ForeignKey('Patient', on_delete=models.PROTECT, null=True)

    right_sph = models.CharField(max_length=6, null=True, blank=True)
    right_cyl = models.CharField(max_length=6, null=True, blank=True)
    right_axis= models.CharField(max_length=6, null=True, blank=True)
    right_prism = models.CharField(max_length=6, null=True, blank=True)
    right_va = models.CharField(max_length=6, null=True, blank=True)

    left_sph = models.CharField(max_length=6, null=True, blank=True)
    left_cyl = models.CharField(max_length=6, null=True, blank=True)
    left_axis= models.CharField(max_length=6, null=True, blank=True)
    left_prism = models.CharField(max_length=6, null=True, blank=True)
    left_va = models.CharField(max_length=6, null=True, blank=True)

    bin_va = models.CharField(max_length=6, null=True, blank=True)
    add = models.CharField(max_length=6, null=True, blank=True)
    pd = models.CharField(max_length=6, null=True, blank=True)

    recall = models.DateTimeField(null=True)
    clinical_advice_remarks = models.TextField()

    #created = models.DateTimeField(auto_now_add=True)
    #updated = models.DateTimeField(auto_now=True)
    #status = models.BooleanField(default=True)
'''

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class Bill(models.Model):
    bill_statuses = (
        ('pending','Pending'),
        ('partialyment','Partpayment'),
        ('cancelled','Cancelled'),
        ('paid','Paid'),
        ('waived','Waived')
    )

    uuid = models.UUIDField(
        unique = True,
        default = uuid.uuid4,
        editable = False
    )

    amount = models.FloatField(_("amount"))
    status = models.CharField(_("status"), max_length=15,choices=bill_statuses)
    visit = models.ForeignKey("Visit", verbose_name=_(""), on_delete=models.PROTECT, related_name='bill')

class Patient(models.Model):
    uuid = models.UUIDField(unique = True, default = uuid.uuid4, editable = False)

    gender_choices = (
        ('male', 'male'),
        ('female', 'female'),
        ('other', 'other')
    )

    tr_no = models.CharField(max_length=50,null=False,blank=False,unique=True,default=gen_tr_no)
    first_name = models.CharField(max_length=256,blank=False,null=False)
    other_names = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=255,blank=False,null=False)
    gender = models.CharField(choices=gender_choices, max_length=7)
    date_of_birth = models.DateField(null=True,blank=True)
    age = models.IntegerField(null=True, blank=True) # auto-calculate age
    email = models.EmailField( max_length=254, null=True, blank=True)
    location  = models.CharField(max_length=60, null=True, blank=True)
    ghana_post = models.CharField(max_length=50,null=True,blank=True)
    last_eye_test = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    remarks = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    cellphone_1 = models.CharField(validators=[phone_regex], max_length=17, null=True, blank=True)
    cellphone_2 = models.CharField(validators=[phone_regex], max_length=17, null=True, blank=True)
    is_registered = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        constraints = [
            models.CheckConstraint(
                check = (
                    models.Q(email__isnull=True, cellphone_1__isnull=False, cellphone_2__isnull=False) |
                    models.Q(email__isnull=False, cellphone_1__isnull=True, cellphone_2__isnull=False) |
                    models.Q(email__isnull=False, cellphone_1__isnull=False, cellphone_2__isnull=True) |

                    models.Q(email__isnull=False, cellphone_1__isnull=True, cellphone_2__isnull=True) |
                    models.Q(email__isnull=True, cellphone_1__isnull=False, cellphone_2__isnull=True) |
                    models.Q(email__isnull=True, cellphone_1__isnull=True, cellphone_2__isnull=False) |
                    
                    models.Q(email__isnull=False, cellphone_1__isnull=False, cellphone_2__isnull=False) 
                ),
                name = 'check_either_email_cellphone_1_cellphone_2',
            ),
        ]

    def __str__(self):
        return '{0} {1} {2}'.format(self.last_name, self.first_name,self.last_name)

    def get_absolute_url(self):
        pass
        #return reverse('clinic:patient-detail', args=[str(self.id)])

class Clinician(models.Model):
    clinician_type = (
       ('doctor','doctor'),
       ('screener','screener')
    )

    gender_choices = (
        ('male', 'male'),
        ('female', 'female'),
        ('other', 'other')
    )

    category = models.CharField(_("category"), max_length=10,choices=clinician_type)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=59)
    other_name = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(choices=gender_choices, max_length=7)
    dob = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    
    cellphone_1 = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    cellphone_2 = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    address = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    ghana_post = models.CharField(max_length=50,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    # opening_hour = models.TimeField(_("opening_hour"), auto_now=False, auto_now_add=False)
    # closing_hour = models.TimeField(_("closing_hour"), auto_now=False, auto_now_add=False)

    def __str__(self):
        return 'Dr.{0} {1}'.format(self.first_name, self.last_name)


class Appointment(models.Model):
    appointment_status =(
        ('booked','booked'),
        ('confirmed','confirmed'),
        ('cancelled','cancelled'),
        ('rescheduled','rescheduled'),
        ('available','available'),
        ('honoured','honoured'),
        ('pending','pending'),   
    )

    patient = models.ForeignKey('Patient', verbose_name=_('Patient'), on_delete=models.DO_NOTHING,related_name='appointments')
    doctor = models.ForeignKey("Clinician", verbose_name=_('Clinician'), on_delete=models.DO_NOTHING,related_name='appointements')

    date = models.DateField(_("date"), auto_now=False, auto_now_add=False)
    start_time = models.TimeField(_("start_time"), auto_now=False, auto_now_add=False)
    end_time = models.TimeField(_("end_time"), auto_now=False, auto_now_add=False)
    status = models.CharField(choices=appointment_status, max_length=15)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return '{0} {1}'.format(self.patient, self.doctor)

    def get_absolute_url(self):
        pass

class Visit(models.Model):
    visit_statuses = (
        ('registered','registered'),
        ('screened','screened'),
        ('examined','examined'),
    )
    status = models.CharField( max_length=25,choices=visit_statuses,default='registered')
    uuid = models.UUIDField(
        #primary_key = True,
        unique = True,
        default = uuid.uuid4,
        editable = False
    )

    doctor = models.ForeignKey('Clinician', verbose_name=_(""), on_delete=models.PROTECT)
    patient = models.ForeignKey('Patient', on_delete=models.PROTECT, null=False,related_name = "refractions")
    date = models.DateField(_("date"), auto_now=False, auto_now_add=False)
    start_time = models.TimeField(_("start_time"), auto_now=False, auto_now_add=False)

    class Meta:
        ordering = ['-id']


    def __str__(self):
        return '{0} {1} '.format(self.patient, self.doctor)

    def get_absolute_url(self):
        pass


class ChartRefraction(models.Model):
    rx_types = (
        ('current_spec1','current_spec1'),
        ('current_spec2','current_spec2'),
        ('objective1','Objective 1'),
        ('objective2','Objective 2'),
        ('subjective','subjective'),
        ('final','final'),
    )

    uuid = models.UUIDField(unique = True, default = uuid.uuid4, editable = False)
    visit = models.ForeignKey(Visit, verbose_name=_(""), on_delete=models.PROTECT, related_name = "chart_refraction")
    rx_type = models.CharField(max_length=25,choices=rx_types, default='current_spec1')
    #patient = models.ForeignKey('Patient', on_delete=models.PROTECT, null=False,related_name = "refractions")
    clinician = models.ForeignKey("Clinician", on_delete=models.PROTECT, related_name = "refractions",null=True,blank=True)
    right_sph = models.CharField(max_length=6, null=True, blank=True)
    right_cyl = models.CharField(max_length=6, null=True, blank=True)
    right_axis= models.CharField(max_length=6, null=True, blank=True)
    right_prism = models.CharField(max_length=6, null=True, blank=True)
    right_va = models.CharField(max_length=6, null=True, blank=True)
    left_sph = models.CharField(max_length=6, null=True, blank=True)
    left_cyl = models.CharField(max_length=6, null=True, blank=True)
    left_axis= models.CharField(max_length=6, null=True, blank=True)
    left_prism = models.CharField(max_length=6, null=True, blank=True)
    left_va = models.CharField(max_length=6, null=True, blank=True)
    bin_va = models.CharField(max_length=6, null=True, blank=True)
    add = models.CharField(max_length=6, null=True, blank=True)
    pd = models.CharField(max_length=6, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class ChartEyePressure(models.Model):
    uuid = models.UUIDField(unique = True, default = uuid.uuid4, editable = False)
    visit = models.ForeignKey('Visit', verbose_name=_(""), on_delete=models.PROTECT, related_name="chart_eye_pressure")
    clinician = models.ForeignKey("Clinician", on_delete=models.PROTECT, related_name = "chart_eyepressure", null=True,blank=True)
    right_iops = models.CharField(max_length=6, null=True, blank=True)
    right_fields = models.CharField(max_length=6, null=True, blank=True)
    left_iops = models.CharField(max_length=6, null=True, blank=True)
    left_fields = models.CharField(max_length=6, null=True, blank=True)
    time = models.DateTimeField( auto_now=False, auto_now_add=False)
    drug_concentraion = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    symptoms_and_history = models.TextField(_("symptoms_and_history"),null=True,blank=True)

class ChartExamination(models.Model):

    uuid = models.UUIDField(unique = True, default = uuid.uuid4, editable = False)
    visit = models.ForeignKey('Visit', verbose_name=_(""), on_delete=models.PROTECT, related_name="chart_examinations")
    #patient = models.ForeignKey('Patient', on_delete=models.PROTECT, null=False,related_name = "chart_examinations")
    #clinician = models.ForeignKey("Clinician", on_delete=models.PROTEC, related_name = "chart_examinations",null=True,blank=True)
    oculomotor_balance = models.CharField( max_length=50)
    amsler = models.CharField( max_length=50)
    color_vision = models.CharField( max_length=50)
    right_ant = models.CharField(max_length=12, null=True,blank=True)
    right_post = models.CharField( max_length=50,null=True, blank=True)
    right_cpu_disc = models.CharField( max_length=50, null=True,blank=True)
    left_ant = models.CharField(max_length=12, null=True,blank=True)
    left_post = models.CharField( max_length=50,null = True,blank=True)
    left_cpu_disc = models.CharField( max_length=50, null=True,blank=True)
    clinical_advice_remarks = models.TextField(_("clinical_advice_remarks"))
    recall = models.TextField(null=True,blank=True)