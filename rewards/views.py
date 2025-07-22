from django.shortcuts import render, redirect
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Rewards app!")

def reward_list(request):
    return render(request, 'rewards/reward_list.html')

def reward_detail(request, reward_id):
    return render(request, 'rewards/reward_detail.html', {'reward_id': reward_id})

def reward_create(request):
    if request.method == 'POST':
        # Process form data and create reward
        # reward = Reward.objects.create(...)
        return redirect('reward_list')
    return render(request, 'rewards/reward_create.html')
def reward_update(request, reward_id):
    if request.method == 'POST':
        # Process form data and update reward
        # reward = Reward.objects.get(id=reward_id)
        # reward.save()
        return redirect('reward_detail', reward_id=reward_id)
def reward_delete(request, reward_id):
    # Logic to handle reward deletion
    if request.method == 'POST':
        # reward = Reward.objects.get(id=reward_id)
        # reward.delete()
        return redirect('reward_list')
    return render(request, 'rewards/reward_delete.html', {'reward_id': reward_id})
