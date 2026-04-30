from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import User
from .models import Complaint
from .forms import ComplaintForm

@login_required
def complain(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    
    if request.user == target_user:
        messages.error(request, 'Нельзя пожаловаться на самого себя')
        return redirect('profile', user_id=user_id)
    
    existing = Complaint.objects.filter(complainant=request.user, target_user=target_user, status='pending').first()
    if existing:
        messages.warning(request, 'Вы уже отправили жалобу на этого пользователя. Она на рассмотрении.')
        return redirect('profile', user_id=user_id)
    
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.complainant = request.user
            complaint.target_user = target_user
            complaint.save()
            messages.success(request, 'Жалоба отправлена. Администратор рассмотрит её в ближайшее время.')
            return redirect('profile', user_id=user_id)
    else:
        form = ComplaintForm()
    
    return render(request, 'complaints/complain.html', {
        'form': form,
        'target_user': target_user
    })