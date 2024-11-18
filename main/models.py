from django.db import models

class Country(models.Model):
    cname = models.CharField(max_length=50, primary_key=True)
    population = models.BigIntegerField()

    class Meta:
        db_table = 'country'

class Users(models.Model):
    email = models.CharField(max_length=60, primary_key=True, db_column='email')
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=40)
    salary = models.IntegerField()
    phone = models.CharField(max_length=20)
    cname = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        db_table = 'users'

class Patients(models.Model):
    email = models.OneToOneField(
        Users,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='email'  # Explicitly set the column name
    )

    class Meta:
        db_table = 'patients'


class DiseaseType(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=140)

class Disease(models.Model):
    disease_code = models.CharField(max_length=50, primary_key=True)
    pathogen = models.CharField(max_length=20)
    description = models.CharField(max_length=140)
    id = models.ForeignKey(DiseaseType, on_delete=models.CASCADE, db_column='id')

    class Meta:
        db_table = 'disease'
        managed = False

class Discover(models.Model):
    cname = models.ForeignKey(Country, on_delete=models.CASCADE)
    disease_code = models.ForeignKey(Disease, on_delete=models.CASCADE)
    first_enc_date = models.DateField()

    class Meta:
        unique_together = ('cname', 'disease_code')

class PatientDisease(models.Model):
    email = models.ForeignKey(Users, on_delete=models.CASCADE)
    disease_code = models.ForeignKey(Disease, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('email', 'disease_code')

class PublicServant(models.Model):
    email = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    department = models.CharField(max_length=50)

class Doctor(models.Model):
    email = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    degree = models.CharField(max_length=20)

class Specialize(models.Model):
    id = models.ForeignKey('DiseaseType', on_delete=models.CASCADE, primary_key=True)
    email = models.ForeignKey('Doctor', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('id', 'email')  # Ensure the pair of id and email are unique
        # Alternatively, if you prefer to use constraints for better readability:
        # constraints = [
        #     models.UniqueConstraint(fields=['id', 'email'], name='unique_specialize')
        # ]

    def __str__(self):
        return f"Specialization of {self.email} in Disease Type {self.id}"

class Record(models.Model):
    record_pkey = models.AutoField(primary_key=True)
    email = models.ForeignKey(PublicServant, on_delete=models.CASCADE, db_column='email')
    cname = models.ForeignKey(Country, on_delete=models.CASCADE , db_column='cname')
    disease_code = models.ForeignKey(Disease, on_delete=models.CASCADE, db_column='disease_code')
    total_deaths = models.IntegerField()
    total_patients = models.IntegerField()

    class Meta:
        db_table = 'record'
        managed = False
