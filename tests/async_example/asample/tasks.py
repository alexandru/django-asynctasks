from django_asynctasks.tasks import task

@task(label='Say Hello')
def say_hello(name):
    return "Hello " + name

@task(label='task that throws exceptions')
def throw_something(what):
    raise Exception(what)