from django.db import models

#this table records the patient information
class PatientInfo(models.Model):
    ids = models.IntegerField(primary_key=True)
    Oral_Health_Index = models.FloatField(null=True, blank=True, default=None)
    Bitewing_Series = models.FloatField(null=True, blank=True, default=None)
    Tobacco_Counsel = models.FloatField(null=True, blank=True, default=None)
    Age = models.FloatField(null=True, blank=True, default=None)
    Completed_Tx = models.FloatField(null=True, blank=True, default=None)
    Recall_Exams = models.FloatField(null=True, blank=True, default=None)
    Fluoride = models.FloatField(null=True, blank=True, default=None)
    Nutritional_Counsel = models.FloatField(null=True, blank=True, default=None)
    Class_II_Restorations = models.FloatField(null=True, blank=True, default=None)
    Other_Composite_restorations = models.FloatField(null=True, blank=True, default=None)
    Fixed_Pros_Natural_Teeth = models.FloatField(null=True, blank=True, default=None)
    Fixed_Pros_Implant_or_Other = models.FloatField(null=True, blank=True, default=None)
    Removable_Prosthesis = models.FloatField(null=True, blank=True, default=None)
    Periodontal_Tx = models.FloatField(null=True, blank=True, default=None)
    Gender = models.FloatField(null=True, blank=True, default=None)
    RyanWhite_Insurance = models.FloatField(null=True, blank=True, default=None)
    Basic_Complexity = models.FloatField(null=True, blank=True, default=None)
    Complex_Complexity = models.FloatField(null=True, blank=True, default=None)
