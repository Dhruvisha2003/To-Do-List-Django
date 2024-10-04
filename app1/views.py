from django.shortcuts import *
from .models import todo_task
from django.contrib import messages

# Create your views here.

def home(request):
    data = todo_task.objects.all()
    return render(request,'index.html',{'data':data})

def addTask(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        status = request.POST.get('status')
        completion_date = request.POST.get('completion_date') if status == 'Complete' else None

        if not todo_task.objects.filter(title=title).exists():
            task = todo_task(title=title,desc=desc,status=status,completion_date=completion_date)
            task.save()
            return redirect('home')
        else:
            messages.warning(request, "This item is Already in your list")
            return redirect('add')
    
    return render(request,'add.html')

def delete_task(request, id):
    item = todo_task.objects.get(id=id)             

    if request.method == "POST":
        if request.POST.get("confirm") == "yes":
            item.delete()  
            return redirect('home')
        return redirect('home') 
    
    return render(request, 'delete.html', {'item': item})

def editTask(request, id):
    task = todo_task.objects.get(id=id)

    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        status = request.POST.get('status')

        task.title = title
        task.desc = desc
        task.status = status
        
        if status.lower() == 'complete':
            task.completion_date = request.POST.get('completion_date', None)
        else:
            task.completion_date = None

        task.save()

        messages.success(request, 'Your task has been updated successfully.')
        return redirect('edit_task',id=task.id)  

    return render(request, 'edit.html', {'task': task})

def viewTask(request,id):
    task = todo_task.objects.get(id=id)
    return render(request,'view.html',{'task':task})
