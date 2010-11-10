from setuptools import setup, find_packages

setup(
    name = "django-asynctasks",
    version = "0.1",
    packages = find_packages('src'),
    package_dir = {'':'src'},

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['README', 'LICENSE', '*.txt'],
    },

    install_requires = ['Django>=1.2.3', 'django-extensions>=0.5'],

    author = "Alexandru Nedelcu",
    author_email = "me@alexn.org",
    description = """Django App that does asynchronous tasks processing.""",    
    license = "BSD",
    keywords = "django asynchronous tasks",
    url = "https://github.com/alexandru/django-asynctasks",
)
