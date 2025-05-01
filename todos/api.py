from ninja import Router
from .schemas import TaskIn, TaskOut
from .models import Task
from functools import wraps

router = Router()

def auth_required(fn):
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return {"error": "User not authenticated"}
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


@router.put("/task/{task_id}", response=TaskOut, url_name="update_todo_task", tags=["Task"])
@auth_required
def update_task(request, task_id: int, payload: TaskIn):
    task = Task.objects.get(id=task_id, user=request.user)
    for attr, value in payload.dict().items():
        setattr(task, attr, value)
    task.save()

    return task

@router.delete("/task/{task_id}", response=TaskOut, url_name="delete_todo_task", tags=["Task"])
@auth_required
def delete_task(request, task_id: int):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()

    return task

@router.get("/task/complete", response=list[TaskOut], url_name="list_completed_todo_tasks", tags=["Task"])
@auth_required
def list_completed_tasks(request):
    tasks = Task.objects.filter(user=request.user, completed=True)

    return tasks

@router.post("/task/complete/{task_id}", response=TaskOut, url_name="complete_todo_task", tags=["Task"])
@auth_required
def complete_task(request, task_id: int):
    task = Task.objects.get(id=task_id, user=request.user)
    task.completed = True
    task.save()

    return task
