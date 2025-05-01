from ninja import Router
from django.http import JsonResponse
from .schemas import TaskIn, TaskOut, PartialTaskIn
from .models import Task
from functools import wraps

router = Router()

def auth_required(fn):
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User not authenticated"}, status=401)

        return fn(request, *args, **kwargs)

    return wrapper


@router.post("/task", response=TaskIn, url_name="create_todo_task", tags=["Task"])
@auth_required
def create_task(request, payload: TaskIn):
    new_todo_task = Task.objects.create(**payload.dict(), user=request.user)

    return new_todo_task


@router.get("/task", response=list[TaskOut], url_name="list_todo_tasks", tags=["Task"])
@auth_required
def list_tasks(request):
    tasks = Task.objects.filter(user=request.user)

    return tasks


@router.get("/task/{task_id}", response=TaskOut, url_name="retrieve_todo_task", tags=["Task"])
@auth_required
def retrieve_task(request, task_id: int):
    task = Task.objects.get(id=task_id, user=request.user)

    return task


@router.patch("/task/{task_id}", response=TaskOut, url_name="update_todo_task", tags=["Task"])
@auth_required
def update_task(request, task_id: int, payload: PartialTaskIn):
    task = Task.objects.get(id=task_id, user=request.user)

    if payload.title is not None:
        task.title = payload.title
    if payload.description is not None:
        task.description = payload.description
    if payload.complete is not None:
        task.complete = payload.complete

    task.save()

    return task

@router.delete("/task/{task_id}", response=TaskOut, url_name="delete_todo_task", tags=["Task"])
@auth_required
def delete_task(request, task_id: int):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()

    return task

@router.get("/task/complete", response=list[TaskOut], url_name="list_complete_tasks", tags=["Task"])
@auth_required
def list_complete_tasks(request):
    tasks = Task.objects.filter(user=request.user)

    return tasks

@router.post("/task/complete/{task_id}", response=TaskOut, url_name="complete_todo_task", tags=["Task"])
@auth_required
def complete_task(request, task_id: int):
    task = Task.objects.get(id=task_id, user=request.user)
    task.complete = True
    task.save()

    return task
