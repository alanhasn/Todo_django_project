from django.shortcuts import render, redirect, HttpResponseRedirect ,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Todo_list


@login_required  # Ensure the user is logged in if user is not authenticated it will redirect them to home page
def todo(request):
    if request.method == "POST": # ensure that the request is POST
        title = request.POST.get('title') # get title
        completed_task_id = request.POST.get('completed_task_id') # get the completed task id 
        completed_status = request.POST.get('completed')  # Get the status of the checkbox
        delete_task_id = request.POST.get('delete_task_id') # get the id of the task the user want to delete

        # Check if a new task is being added
        if title:
            Todo_list.objects.create(user=request.user, Title=title)  # Create a new task

        # Check if a task's completed status is being toggled
        if completed_task_id:
            try:
                task = Todo_list.objects.get(id=completed_task_id, user=request.user)  # Retrieve the task
                # Update the task's completion status based on the checkbox value
                if completed_status == "True":
                    task.completed = True
                else:
                    task.completed = False
                task.save()  # Save the changes
            except Todo_list.DoesNotExist:
                return HttpResponse('Task not found.', status=404)
                   
        if delete_task_id: # ensure there is id
            try:           
                delete_item=Todo_list.objects.get(id=delete_task_id,user=request.user)# retrieve the task the user want to delete
                delete_item.delete() # delete the task

            except Todo_list.DoesNotExist: # handle Error
                return redirect('todo') 
            
    # Get tasks for the logged-in user
    tasks = Todo_list.objects.filter(user=request.user)  # Retrieve all tasks (both completed and incomplete)
    return render(request, 'todo/todo.html', {'tasks': tasks})  # Pass all tasks to the template

