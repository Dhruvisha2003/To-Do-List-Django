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
        if status == 'Complete':
            completion_date = request.POST.get('completion_date')

        else:
            task.completion_date = None

        dropdown_submit = request.POST.get('dropdown_submit', False)
        if dropdown_submit:
            return render(request, 'add.html', {
                'task': {'title': title,'desc': desc,'status': status,'completion_date': completion_date}
            })
        if not todo_task.objects.filter(title=title).exists():
            task = todo_task(title=title, desc=desc, status=status, completion_date=completion_date)
            task.save() 
            return redirect('home')
        else:
            messages.warning(request, "This item is already in your list")
            return redirect('add')
    print()
    return render(request, 'add.html')
    
def delete_task(request, id):
    item = todo_task.objects.get(id=id)             

    if request.method == "POST":
        if request.POST.get("confirm") == "Yes":
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
        dropdown_submit = request.POST.get('dropdown_submit', False)

        task.title = title
        task.desc = desc
        task.status = status
        
        if task.status == 'Complete':
            task.completion_date = request.POST.get('completion_date')
    
        else:
            task.completion_date = None

        if not dropdown_submit:
            task.save()
        
        if not dropdown_submit:
            messages.success(request, 'Task updated successfully.')
        return render(request, 'edit.html', {'task': task})

    return render(request, 'edit.html', {'task': task})

def viewTask(request,id):
    task = todo_task.objects.get(id=id)
    return render(request,'view.html',{'task':task})
