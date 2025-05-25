from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import CourseMaterial
from .forms import CourseMaterialForm


def home(request):
    return render(request, 'core/home.html')



@login_required
def dashboard(request):
    if request.user.groups.filter(name='Professors').exists():
        form = CourseMaterialForm(request.POST or None, request.FILES or None)
        if request.method == 'POST' and form.is_valid():
            material = form.save(commit=False)
            material.uploaded_by = request.user
            material.save()
            return redirect('dashboard')

        # Professors will see only their own uploaded materials
        materials = CourseMaterial.objects.filter(uploaded_by=request.user)
        return render(request, 'core/professor_dashboard.html', {
            'form': form,
            'materials': materials
        })

    elif request.user.groups.filter(name='Students').exists():
        # Students will see all course materials
        materials = CourseMaterial.objects.all()
        return render(request, 'core/student_dashboard.html', {
            'materials': materials
        })

    else:
        return render(request, 'core/home.html', {
            'error': 'You are not assigned to a role (Student/Professor).'
        })





