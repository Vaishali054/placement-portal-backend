from django.db import models
from company.models import Company
from course.models import Cluster,Specialization, Course
from validators import Validate_file_size
from django.core.validators import RegexValidator, FileExtensionValidator, MaxValueValidator
from tpr.models import TPR

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name

jtype = [
    ('intern','Internship'),
    ('placement','Placement'),
    ('intern and fte', 'Internship+Placement')
]
class Drive(models.Model):
    # def job_desc_directory_path(instance, filename):
    #     return 'drive/job_desc/{0}/{1}/{2}.pdf'.format(instance.session,instance.job_type,instance.company.name)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    # job_desc_pdf = models.FileField(upload_to=job_desc_directory_path, null=True, blank=True, validators=[FileExtensionValidator(['docx','doc','pdf']), Validate_file_size(5,"MB")])
    modeOfHiring = models.CharField(default="virtual", choices = [('virtual','Virtual'),('onsite','On-Site')], max_length=20)
    prePlacementTalk = models.BooleanField(default=True)
    aptitudeTest = models.BooleanField(default=True)
    technicalTest = models.BooleanField(default=True)
    groupDiscussion = models.BooleanField(default=True)
    personalInterview = models.BooleanField(default=True)
    noOfPersonsVisiting = models.IntegerField(default=0) # 0 if drive is virtual
    jobLocation = models.CharField(max_length=100) # Separate different job locations with any delimeter
    starting_date = models.DateField()
    courses = models.ManyToManyField(Course)
    branches = models.ManyToManyField(Specialization)
    cgpi = models.IntegerField(default=0)
    allowStudentsWithBacklogs = models.BooleanField(default=True)
    jobProfile = models.CharField(max_length=100, default="SDE1")
    # closed_date = models.DateField()
    drive_status = models.CharField(default="pending", choices = [('Pending','pending'),('Approved','approved')], max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # job_roles = models.ManyToManyField(JobRoles) #=> it one to many relation so there should be foreignkey in jobrole table
    ctc = models.FloatField(default=0) # Store ctc of the expected ppo offer
    # drive type based on company type for e.g. IT, Mech Core, EE Core, etc..
    session = models.CharField(max_length=7,validators=[RegexValidator(regex=r'\d{4}[-]\d{2}$')])
    job_type = models.CharField(max_length=15, choices=jtype)
    # tpr = models.ForeignKey(TPR,on_delete=models.CASCADE,null=True)
    closed_date = models.DateTimeField(null=True)
    drive_status = models.CharField(default="Upcoming", choices = [('Upcoming','Upcoming'),('Ongoing','Ongoing'),('Completed','Completed')], max_length=20)

    class Meta:
        unique_together = ('company','job_type','session')

    def __str__(self) -> str:
        return self.company.name + " " + self.session + " " +self.job_type



class JobRoles(models.Model):
    drive = models.ForeignKey(Drive,on_delete=models.CASCADE,related_name="job_roles")
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    ctc = models.FloatField()
    cgpi = models.FloatField(validators=[MaxValueValidator(10)])
    eligible_batches = models.ManyToManyField(Specialization) # add only specialisations which are eligible
    cluster = models.ForeignKey(Cluster,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.drive.__str__()) + " " + self.role.name