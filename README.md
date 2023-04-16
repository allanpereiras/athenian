# Usage

In summary, I used Django and Django REST Framework to build an asynchronous API server thaat uses PostgreSQL as a SQL database through a docker container. To deploy for a development env I used Docker and Daphne, a pure-Python ASGI server, to take advantage of the benefits of an async stack. Celery is used for asynchronous task processing. 
pre-commit and black were setup for code quality, Pandas for data manipulation, Redis for caching, and drf-spectacular for generating OpenAPI documentation.

<pre>docker-compose up --build</pre>

You can access the API and its OpenAPI documentation at http://localhost:8000/

You can access the admin interface for easy inspection of the data being persisted.  http://localhost:8000/admin/ you will need to create a superuser first:

<pre>docker-compose exec web python manage.py createsuperuser</pre>

For testing, you can run the following command:

<pre>docker-compose exec web python manage.py test</pre>


# Technologies Used

**Django**

Django is a high-level Python web framework that enables rapid development of secure and maintainable websites. It follows a Model-View-Controller (MVC) like architecture pattern and comes with several pre-built features, including a built-in admin interface, ORM, and authentication system.

**Django REST Framework**

Django REST Framework is a toolkit for building Web APIs based on Django. It provides a set of powerful and flexible tools to build APIs quickly and with minimal fuss, including support for authentication, serialization, and testing.

**Redis**

Redis is an open-source, in-memory data structure store that is used as a database, cache, and message broker. It supports data structures such as strings, hashes, lists, sets, sorted sets, bitmaps, hyperloglogs, geospatial indexes, and streams. Redis has built-in replication, Lua scripting, LRU eviction, transactions, and different levels of on-disk persistence, and provides high availability via Redis Sentinel and automatic partitioning with Redis Cluster.

I also used Redis as a **cache backend** for Django. Redis is an in-memory data structure store that supports a wide range of data structures such as strings, hashes, lists, and sets. It provides high availability and automatic partitioning, making it easy to scale our application.

**Daphne**

Daphne is a pure-Python ASGI server for UNIX that is maintained by members of the Django project. It is used to run Django applications in an asynchronous environment and is capable of servicing hundreds of connections without using Python threads.

**Docker**

Docker is used as the platform that allows developers to build, ship, and run applications in containers. It provides an efficient and flexible way to deploy applications, enabling developers to create a consistent environment across development, testing, and production environments.

**Celery**
Celery is a task queue system used to distribute work across threads or machines. It communicates via messages, using a broker to mediate between clients and workers. It is used to run background tasks in Django. You can see the Celery Log using the command docker-compose logs -f celery.

**Pre-commit**

Pre-commit is a framework for managing and maintaining pre-commit hooks in Git. It allows developers to automatically run checks on their code before committing, enabling them to catch issues before they reach the code review process. Here it is used to ensure code quality by identifying and fixing common issues such as missing semicolons, trailing whitespace, and debug statements. We also enforce a consistent code style using the black formatter.

**Pandas**

Pandas is a data manipulation library that provides data structures and functions for manipulating numerical tables and time series data. In this project it is used for CSV parsing and data manipulation.

