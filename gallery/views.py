from django.shortcuts import render, redirect

from gallery.forms import PhotoForm
from gallery.models import Photo


# Create your views here.
def gallery(request):
    photos = Photo.objects.all()
    return render(request, "gallery/index.html", {'photos': photos})


def uploads(request):
    form = PhotoForm()
    if request.method == 'POST':
        form = PhotoForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("gallery")
    return render(request, "gallery/upload.html", {'form': form})
