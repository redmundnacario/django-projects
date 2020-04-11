from rest_framework import serializers
from jobsapi.models import Company, Job

class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.StringRelatedField()

    class Meta:
        model = Job
        exclude = ("id",)

class CompanySerializer(serializers.ModelSerializer):
    jobs = serializers.HyperlinkedRelatedField(many=True,
                                               read_only=True,
                                               view_name="job-detail")
    class Meta:
        model = Company
        exclude = ("id",)