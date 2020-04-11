from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from jobsapi.models import Company, Job
from jobsapi.api.serializers import CompanySerializer, JobSerializer

# jobs-list : GET, POST
class JobListCreateAPIView(APIView):

    def get(self, request):
        jobs = Job.objects.filter(available=True)
        serializer = JobSerializer(jobs, many = True)
        return Response(serializer.data)

    def post(self,request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


# jobs : GET, PUT, DELETE
class JobDetailAPIView(APIView):
    def get_object(self,pk):
        job = get_object_or_404(Job, pk=pk)
        return job

    def get(self, request, pk):
        job = self.get_object(pk)
        serializer = JobSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk):
        job = self.get_object(pk)
        serializer = JobSerializer(job, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        job = self.get_object(pk)
        job.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)




# companies-list : GET, POST
class CompanyListCreateAPIView(APIView):
    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, 
                                   many=True,
                                   context={"request":request})
        return Response(serializer.data)

    def post(self,request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


# Company: GET, PUT, DELETE
class CompanyDetailAPIView(APIView):
    def get_object(self,pk):
        company = get_object_or_404(Company, pk=pk)
        return company

    def get(self, request, pk):
        company = self.get_object(pk)
        serializer = CompanySerializer(company, context={"request":request})
        return Response(serializer.data)

    def put(self, request, pk):
        company = self.get_object(pk)
        serializer = CompanySerializer(company, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        company = self.get_object(pk)
        company.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)