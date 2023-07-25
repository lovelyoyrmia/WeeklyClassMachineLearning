from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from PIL import Image
import datetime
import requests
from kue.utils import Model
from kue.models import KueIndonesia

class Home(generic.View):
    template_name = 'index.html'
    context = {}

    def get(self, request):
        return render(self.request, self.template_name, self.context)

    
class Predict(generic.View):
    template_name = 'predict.html'
    context = {}

    def get(self, request):
        return render(self.request, self.template_name, self.context)
    
    def post(self, request):
        image_url = self.request.POST.get('url_image')
        image = self.request.FILES.get('image')
        model = Model()
        if image:
            imageBinaryBytes = image.file.read()
            imageStream = io.BytesIO(imageBinaryBytes)
            imagePil = Image.open(imageStream)
            prediction = model.predict(imagePil)
            name = image.name
            model_kue = KueIndonesia(image=image, name=name, prediction=prediction)
            model_kue.save()
            return redirect(f'/predict/{str(model_kue.pk)}')
        if image_url:
            response = requests.get(image_url, stream=True)
            imageStream = io.BytesIO(response.content)
            imagePil = Image.open(imageStream)
            prediction = model.predict(imagePil)
            imageName = image_url.split('/')[-1]
            imageFile = InMemoryUploadedFile(
                file=imageStream,
                field_name=None,
                name=imageName,
                content_type=response.headers.get("content-type"),
                size=len(response.content),
                charset=None
            )
            model_kue = KueIndonesia(image=imageFile, name=imageName, prediction=prediction)
            model_kue.save()
            return redirect(f'/predict/{str(model_kue.pk)}')
        return render(self.request, self.template_name, self.context)
    
class Result(generic.View):
    template_name = 'results.html'
    context = {}
    
    def get(self, request, pk):
        model = KueIndonesia.objects.get(pk=pk)
        self.context = {
            'name': model.name,
            'image': model.image.url,
            'label': model.prediction.replace('_', ' ').title()
        }
        return render(self.request, self.template_name, self.context)


    