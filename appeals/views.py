from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AppealForm, DocumentForm
from .models import Appeal, AppealDocument

@login_required
def create_appeal(request):
    if request.method == 'POST':
        appeal_form = AppealForm(request.POST)
        document_form = DocumentForm(request.POST, request.FILES)

        if appeal_form.is_valid():
            appeal = appeal_form.save(commit=False)
            appeal.author = request.user
            appeal.save()

            files = request.FILES.getlist('files')
            for f in files:
                AppealDocument.objects.create(appeal=appeal, file=f)

            return redirect('home')

    else:
        appeal_form = AppealForm()
        document_form = DocumentForm()

    return render(request, 'appeals/create_appeal.html', {
        'appeal_form': appeal_form,
        'document_form': document_form
    })