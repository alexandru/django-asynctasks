from django_asynctasks.tasks import task

@task(label='Say Hello', bucket='tests')
def say_hello(name):
    return "Hello " + name

@task(label='task that throws exceptions', bucket='tests')
def throw_something(what):
    raise Exception(what)

@task(label='task that throws exceptions', bucket='tests', schedule='hourly')
def hourly_say_hi(what='Alex'):
    return "Hello " + what
