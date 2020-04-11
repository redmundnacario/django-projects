from django.db import models

# Create your models here.

class Company(models.Model):
    class Meta:
        verbose_name_plural = "Companies"
    name = models.CharField(max_length =60)
    email = models.CharField(max_length = 60)
    city = models.CharField(max_length = 60)
    province = models.CharField(max_length = 60)

    def __str__(self):
        return f" { self.name }"

class Job(models.Model):
    company_name = models.ForeignKey(Company, 
                                     on_delete=models.CASCADE,
                                     related_name="jobs")
    job_title = models.CharField(max_length = 100)
    job_description = models.TextField(null=True)
    salary = models.FloatField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" {self.job_title} {self.company_name}"


