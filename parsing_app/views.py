from django.shortcuts import render, HttpResponse
from ParsingPackage.parser import Parsing
from django.core.files.storage import default_storage
import os
import json
from .models import Skill
from django.views.decorators.csrf import csrf_exempt
from .forms import UploadFileForm

def index(request):
    if request.method == 'POST':
        data = request.POST
        pri_skills = data.getlist('pri_skills[]')
        sec_skills = data.getlist('sec_skills[]')
        # return HttpResponse(pri_skills)
        # print(pri_skills,sec_skills)
        request.session['pri_skills'] = pri_skills
        request.session['sec_skills'] = sec_skills
        return render(request, 'final.html')
    skills = Skill.objects.all()
    return render(request,'index.html',{'skills':skills,})

@csrf_exempt
def fetch(request):
    settings_dir = os.path.dirname(__file__)
    PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
    FOLDER = os.path.join(PROJECT_ROOT, 'parsing_app/resumes/temp/name.pdf')
    parsing_object = Parsing()
    result = []

    f = request.FILES.get('file')
    handle_uploaded_file(f,'temp/name')
    result_object = parsing_object.parse(request.session['pri_skills'],request.session['sec_skills'],FOLDER)
    # if result_object[0] == 1:
    handle_uploaded_file(f,result_object[2])
    result.append([(result_object[1]*0.70)+(result_object[0]*0.30),result_object[2],result_object[3]])
    return HttpResponse(json.dumps(result))

@csrf_exempt
def final(request):
    return render(request,'result.html')

def resume(request):
    settings_dir = os.path.dirname(__file__)
    PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
    FOLDER = os.path.join(PROJECT_ROOT, 'parsing_app/resumes/')
    test_file = open(FOLDER+request.GET.get('email'), 'rb')
    response = HttpResponse(content=test_file)
    response['Content-Type'] = 'application/pdf'
    return response

def handle_uploaded_file(f,path):
    with open('parsing_app/resumes/'+path+'.pdf', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
