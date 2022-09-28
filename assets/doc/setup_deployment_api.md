# Setup and Deployment "Recipe Star API"

## setup 

### create and activate a virtual environment

1. create a virtual environment in the root of your project folder: (*using PowerShell and calling the folder .venv*)

   ```powershell
   python -m venv .venv
   ```

2. activate the virtual environment:

   ```powershell
   .\.venv\Scripts\activate
   ```

3. to deactivate:

   ```powershell
   deactivate
   ```

### install and create a Django project

1. install Django's latest version: (*for the code institute walk through use `pip3 install 'django<4'`*)

   ```powershell
   pip3 install django
   ```

2.  create a Django project: (*create a project with the name `django_project` in the current directory `.`*)

   ```powershell
   django-admin startproject django_project .
   ```

### install dependency's and register the apps

1. install the "Cloudinary" app: (*allows for image storing in the cloud*)

   ```powershell
   pip3 install django-cloudinary-storage
   ```

2. install the "Pillow" library: (*provides image processing capability's*)

   ```powershell
   pip3 install Pillow
   ```

3. install Django filter:

   ```powershell
   pip install django-filter
   ```

4. install dj-trest-auth for JWT (*Jason web token*) :

   ```powershell
   pip install dj-rest-auth
   ```

5. If you want to enable standard registration process you will need to install

   ```powershell
   pip install 'dj-rest-auth[with_social]'
   ```

6. If you want to use JWT authentication, follow these steps:

   ```python
   pip install djangorestframework-simplejwt
   ```

7. register the cloudinary app's in the settings.py in the "Django project": (*follow the correct order*)

   ```python
   // ... django_project/settings.py
   INSTALLED_APPS = [
   // ...
       'cloudinary_storage',
       'django.contrib.staticfiles',
       'cloudinary',
       'django_filters',
       'rest_framework.authtoken',
       'dj_rest_auth',
       'django.contrib.sites',
       'allauth',
       'allauth.account',
       'allauth.socialaccount',
       'dj_rest_auth.registration',
   ]
   ```

8. set the site id setting to the value of 1

   ```python
   // ... django_project/settings.py
   SITE_ID = 1
   ```

9. update the main urls .py

   ```python
   // ... django_project/urls.py
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('api-auth/', include('rest_framework.urls')),
       path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
   	// ...
   ]
   ```

   create a "env.py" file for the environment variables

1. create the env.py file in the top directory: (*replace "CLOUDINARY_API_ENVIRONMENT_VARIABLE" with the actual variable from Cloudinary*)

   ```python
    // ... env.py
   import os
   os.environ['CLOUDINARY_URL']='cloudinary://CLOUDINARY_API_ENVIRONMENT_VARIABLE'
   os.environ['DEV'] = '1'
   ```

   *line 4*:

   - is needed for Json web token

2. add to the project settings:

   ```python
   // ... django_project/settings.py
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [(
           'rest_framework.authentication.SessionAuthentication'
           if 'DEV' in os.environ
           else 'dj_rest_auth.jwt_auth.JWTCookieAuthentication'
       )]
   }
   
   REST_USE_JWT = True
   JWT_AUTH_SECURE = True
   JWT_AUTH_COOKIE = 'my-app-auth'
   JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'
   
   REST_AUTH_SERIALIZERS = {
       'USER_DETAILS_SERIALIZER': 'django_project.serializers.CurrentUserSerializer'
   }
   ```

3. create the **serializers.py** in the **django_project** folder:

   ```python
   from dj_rest_auth.serializers import UserDetailsSerializer
   from rest_framework import serializers
   
   
   class CurrentUserSerializer(UserDetailsSerializer):
       profile_id = serializers.ReadOnlyField(source='profile.id')
       profile_image = serializers.ReadOnlyField(source='profile.image.url')
   
       class Meta(UserDetailsSerializer.Meta):
           fields = UserDetailsSerializer.Meta.fields + (
               'profile_id', 'profile_image'
           )
   ```

   

4. create the `.gitignore` file in the root project directory and add `env.py` , `.venv/` (*the two files should be greyed out in vscode after adding them*) so they don't get committed to GitHub!!!

   ```
   // ... .gitignore
   .venv/
   env.py
   ```

5. add the condition to `settings.py` to load env.py if exist (*only in local production, uses value from env.py*):

   ```python
   // ... django_project/settings.py
   import os
   
   if os.path.exists('env.py'):
       import env
   
   CLOUDINARY_STORAGE = {
       'CLOUDINARY_URL': os.environ.get('CLOUDINARY_URL')
   }
   ```

6. let Django know where to find media files, like images:

   ```python
   // ... django_project/settings.py
   MEDIA_URL = '/media/'
   ```

7. set the default file storage to Cloudinary:

   ```python
   // ... django_project/settings.py
   DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
   ```

### create file with dependencies

- should be re-run before deployment

  ```powershell
  pip freeze > requirements.txt
  ```

***

## create the profiles app

### create the model

1. create a Django app called "profiles":

   ```powershell
   python manage.py startapp profiles
   ```

2. register the app in settings:

   ```python
   // ... django_project/settings.py
   INSTALLED_APPS = [
   // ...
   	'profiles',
   ]
   ```

3. add following code:

   ```python
   // ... profiles/models.py
   from django.db import models
   from django.contrib.auth.models import User
   from django.db.models.signals import post_save
   
   
   class Profile(models.Model):
       owner = models.OneToOneField(User, on_delete=models.CASCADE)
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)
       name = models.CharField(max_length=255, blank=True)
       content = models.TextField(blank=True)
       image = models.ImageField(
           upload_to='images/', default='../default_profile_ukustm'
       )
   
       class Meta:
           ordering = ['-created_at']
   
       def __str__(self):
           return f"{self.owner}'s profile"
   
   
   def create_profile(sender, instance, created, **kwargs):
       if created:
           Profile.objects.create(owner=instance)
   
   post_save.connect(create_profile, sender=User)
   ```

   *line 3*:

   - import the standard Django "custom-user-model"

   *line 7*:

   - create "Profile model"

   *line 8*:

   - `1 to 1` field pointing to a user instance

   *line 9*-10:

   - create automatically time stamps for when the user was created / updated

   *line 11*:

   - the name character field is optional and has a max length of 255 characters

   *line 12*:

   - the content text field is also optional

   *line 13*-14:

   - where to upload images to, default is the default image from Cloudinary, (**NOTE: the "default_profile_" image gets a different ending (hash) every time the picture is uploaded**)

   *line 17-18*:

   - creates a meta class in which the order is determent in which the profiles appear
   - `'-created_at'` corresponds to line 9,  `-` reverses the resolts

   *line 20-21*:

   - adds information of who the profile owner is

   *line 28*:

   - listen for the post save signal `post_save` with the `.connect()` function
   - 1st parameter: what should happen, run function `create_profile`
   - 2nd parameter: when it should happen, signal is coming from `User`

   *line 4*:

   - import `post_save`

   *line 24-26*:

   - define the `create_profile` function before passing it as argument in line 28 to the `.connect()` function
   - if `created` is "true", create profile who's owner is the user (*user is created as in user name and password*)

	### connect model to admin pannel

```python
// ... profiles/admin.py
from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
```

*line 3*:

- import the "Profile" model

*line 5*:

- register the "Profile" model and register it to "view"

### migrate and create super user

1. make migrations:

   ```powershell
   python manage.py makemigrations
   ```

2. migrate

   ```powershell
   python manage.py migrate
   ```

3. create super user so that we can access the admin panel (*email can be left blank*) (*save admin details as a comment in env.py, so you don't forget*)

   ```powershell
   python manage.py createsuperuser
   ```

4. run server to check (*a new user should get a profile in the admin panel*) (*local http://127.0.0.1:8000/admin*)

   ```powershell
   python manage.py runserver
   ```

***

## Django signal

> Django signals are like notifications which get triggered by an event.

- event notifications
- can listen to the events and run a piece of code every time
- in our example: create a user profile every time a user is created
- built-in model signals are: `pre save` `post save` `pre delete` `post delete`

***

## Rest Framework Serializers

1. install Django REST framework

   ```bash
   pip install djangorestframework
   ```

2. register the app in settings:

   ```python
   // ... django_project/settings.py
   INSTALLED_APPS = [
   // ...
   	'rest_framework',
   	'profiles'
   ]
   ```

3. create a view in "views.py":

   ```python
   // ... profile/views.py
   from rest_framework.views import APIView
   from rest_framework.response import Response
   from .models import Profile
   from .serializers import ProfileSerializer
   
   
   class ProfileList(APIView):
       """
       List all profiles
       No Create view (post method), as profile creation handled by django signals
       """
       def get(self, request):
           profiles = Profile.objects.all()
           serializer = ProfileSerializer(profiles, many=True)
           return Response(serializer.data)
   ```

   *line 2*:

   - is similar to Django's "view" class, but it provides some extra functionality such as receiving request instances in our view, handling parsing errors, and adding context to Response objects

   *line 3*:

   - provides a nicer interface for returning content-negotiated Web API responses that can be rendered to multiple formats

   *line 4*:

   - import the "Profile" model

   *line 5*:

   - import the "ProfileSerializer" (*scroll down to see code*)

   *line 15*:

   - before the Response is returned we create a instance of the "ProfileSerializer", the arguments are `profiles` and `many=True` to specify that there are multiple instances of profile

4. create a "urls.py" file:

   ```python
   // ... profile/urls.py
   from django.urls import path
   from profiles import views
   
   urlpatterns = [
       path('profiles/', views.ProfileList.as_view()),
   ]
   ```

   *line 6*:

   - because "ProfileList" is a class view it needs to be called with `.as_view()`

5. include profiles.urls in the in the main urls:

   ```python
   // ... django_project/urls.py
   // ...
   from django.urls import path, include
   
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('profiles.urls')),
   ]
   ```

   *line 3*:

   - add `include`

   *line 7*:

   - add the path to profiles.urls

### posing and requesting from an API

#### When a user posts data to our API, the following has to happen:

1. we need that data to be deserialized, which means it needs to be converted, from a data format like JSON or XML to Python native data types
2.  we have to make sure the data is valid, once it’s validated, a model instance is saved in the database

#### If our users are requesting data from our API,

1. a queryset or model instance is returned from the database.
2. It is then converted to Python native data types before the data is sent back
3. it is converted  again, or serialized to a given format (most commonly JSON).

#### The profiles can’t be just thrown in as a part of the Response, 

1. we need a serializer to convert Django model instances to JSON. As we’ll only be working with Django Models, we’ll use "**model serializers**" to avoid data replication, just like you would use ModelForm over a regular Form. Before we write a model serializer, 

### model serializers

-  handle validation
- similar syntax to model forms (*can have Meta class, model fields, methods `.is_valid` and `.save`*)
- they handle all the conversions between different data types

1. create the serializer.py file:

   ```python
   // ... profile/serializers.py
   from rest_framework import serializers
   from .models import Profile
   
   
   class ProfileSerializer(serializers.ModelSerializer):
       owner = serializers.ReadOnlyField(source='owner.username')
   
       class Meta:
           model = Profile
           fields = [
               'id', 'owner', 'created_at', 'updated_at', 'name',
               'content', 'image'
           ]
   ```

   *line 7*:

   - is read only so it can only be populated from the source which is `owner.username`

   *line 11*:

   - the array contains the fields which will be serialized

2. update dependencies:

   ```bash
   pip freeze > requirements.txt
   ```

### Resolute

- the should be a interface created by the django rest frame work in which we can switch between Jason data and python data

***

### Profile Details View: GET and PUT

profiles CRUD table

| HTTP   | URI          | CRUD operation           | view name |
| ------ | ------------ | ------------------------ | --------- |
| GET    | /profile     | list all profiles        | LIST      |
| POST   | /profile     | create a profile         | LIST      |
| GET    | /profile/:id | retrieve a profile by id | DETAILS   |
| PUT    | /profile/:id | update a profile by id   | DETAILS   |
| DELETE | /profile/:id | delete  a profile by id  | DETAILS   |

Profile Details View: GET method

1. fetch the profile by id
2. serialize the Profile model instance
3. return serializer data in the response

1. update the views.py:

```python
// ... profile/views.py
from django.http import Http404
// ...


class ProfileList(APIView):
	// ...
	
class ProfileDetail(APIView):
    serializer_class = ProfileSerializer
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            return profile
        except Profile.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
```

*line 10*:

- adds a form to the view in which fields can be edited

2. add the individual profile (*based on its id*) to the urls.py:

   ```python
   // ... django_project/urls.py
   from django.urls import path
   from profiles import views
   
   urlpatterns = [
       path('profiles/', views.ProfileList.as_view()),
       path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
   ]
   ```

### ProfileDetail view: Put method

1. fetch the profile by id
2. call serializer with the profile and request data
3. if data is valid, save and return the instance
4. if data is invalid, return the 400 ERROR

1. update views.py

   ```python
   // ... profile/views.py
   from rest_framework import status
   // ...
   
   
   class ProfileDetail(APIView):
   	// ...
   
       def put(self, request, pk):
           profile = self.get_object(pk)
           serializer = ProfileSerializer(profile, data=request.data)
           if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   ```

### Authentication, authorization and serializer method fields

#### add logout button for user

1. add to main urls.py to use the predefined functionality:

   ```python
   // ... django_project/urls.py
   urlpatterns = [
       / ...
       path('api-auth/', include('rest_framework.urls')),
   ]
   ```

#### Django Rest Framework permission classes

- AllowAny
- IsAuthenticated
- IsAdminUser
- IsAuthenticatedOrReadOnly
- BasePermission - to write custom permissions

#### Custom permission:

- object-level to see if a user is the owner
- allow read-only access to anyone
- allow only the owner to update or delete the resource

1. create a permissions.py file in in the django_project folder:

   ```python
   // ... django_project/permissions.py
   from rest_framework import permissions
   
   
   class IsOwnerOrReadOnly(permissions.BasePermission):
     def has_object_permission(self, request, view, obj):
       if request.method in permissions.SAFE_METHODS:
         return True
       return obj.owner == request.user
   ```

2. connect permission.py to the view.py

   ```python
   // ... profiles/views.py
   from django_project.permissions import IsOwnerOrReadOnly
   
   
   // ...
   class ProfileDetail(APIView):
       serializer_class = ProfileSerializer
       permission_classes = [IsOwnerOrReadOnly]
   
       def get_object(self, pk):
           try:
               profile = Profile.objects.get(pk=pk)
               self.check_object_permissions(self.request, profile)
               return profile
           except Profile.DoesNotExist:
               raise Http404
   	// ...
   ```

### add extra field to serializer

to see if the owner is logged in `"is_owner": true`

1. update code:

   ```python
   // ... profile/serializers.py
   from rest_framework import serializers
   from .models import Profile
   
   
   class ProfileSerializer(serializers.ModelSerializer):
       owner = serializers.ReadOnlyField(source='owner.username')
       is_owner = serializers.SerializerMethodField()
   
       def get_is_owner(self, obj):
           request = self.context['request']
           return request.user == obj.owner
   
       class Meta:
           model = Profile
           fields = [
               'id', 'owner', 'created_at', 'updated_at', 'name',
               'content', 'image', 'is_owner'
           ]
   ```

2. in `profile/views.py` add to every `serializer = ProfileSerializer()` the argument `context={'request': request}`

   ```python
   // ... profile/views.py
   from django.http import Http404
   from rest_framework import status
   from rest_framework.views import APIView
   from rest_framework.response import Response
   from .models import Profile
   from .serializers import ProfileSerializer
   from django_project.permissions import IsOwnerOrReadOnly
   
   
   class ProfileList(APIView):
       """
       List all profiles
       No Create view (post method), as profile creation handled by django signals
       """
       def get(self, request):
           profiles = Profile.objects.all()
           serializer = ProfileSerializer(
               profiles, many=True, context={'request': request}
           )
           return Response(serializer.data)
   
   
   class ProfileDetail(APIView):
       serializer_class = ProfileSerializer
       permission_classes = [IsOwnerOrReadOnly]
   
       def get_object(self, pk):
           try:
               profile = Profile.objects.get(pk=pk)
               self.check_object_permissions(self.request, profile)
               return profile
           except Profile.DoesNotExist:
               raise Http404
   
       def get(self, request, pk):
           profile = self.get_object(pk)
           serializer = ProfileSerializer(
               profile, context={'request': request}
           )
           return Response(serializer.data)
   
       def put(self, request, pk):
           profile = self.get_object(pk)
           serializer = ProfileSerializer(
               profile, data=request.data, context={'request': request}
           )
           if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   ```

   

## deployment

1. Create Heroku App with Heroku PostGres

2. install:

   ```
   pip install dj_database_url psycopg2
   ```

3. import:

   ```python
   // ... django_project/settings.py
   import dj_database_url
   ```

4. Separate the Dev and Prod Environments, over write the DATABASES

   ```python
   // ... django_project/settings.py
   DATABASES = {
       'default': ({
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       } if 'DEV' in os.environ else dj_database_url.parse(
           os.environ.get('DATABASE_URL')
       ))
   }
   ```

5. Install gunicorn:

   ```
   pip install gunicorn
   ```

6. Create Procfile:

   ```
   release: python manage.py makemigrations && python manage.py migrate
   web: gunicorn django_project.wsgi
   ```

   ### in ... django_project/settings.py

7. Set the ALLOWED_HOSTS:

   ```python
   ALLOWED_HOSTS = ['recipe-star-api.herokuapp.com', 'localhost']
   ```

8. Install CORS:

   ```
   pip install django-cors-headers
   ```

9. Add to INSTALLED_APPS and MIDDLEWARE (*must be on top*) list:

   ```python
   INSTALLED_APPS = [
       ...
       'corsheaders',
   ]
   
   MIDDLEWARE = [
       'corsheaders.middleware.CorsMiddleware',
   ]
   ```

10. Set the ALLOWED_ORIGINS for the network requests made to the server (*place under MIDDLEWARE_LIST*)

    ```python
    if 'CLIENT_ORIGIN' in os.environ:
        CORS_ALLOWED_ORIGINS = [
            os.environ.get('CLIENT_ORIGIN')
        ]
    else:
        CORS_ALLOWED_ORIGIN_REGEXES = [
            r"^https://.*\.gitpod\.io$",
        ]
    ```

11. Allow Cookies:

    ```python
    CORS_ALLOW_CREDENTIALS = True
    ```

12. Allow front end app and api be deployed to different platforms

    ```python
    JWT_AUTH_SAMESITE = 'None'
    ```

    ###  Set remaining environment variables

1. Set the remaining env variables

   ```python
   // ... env.py
   os.environ['SECRET_KEY'] = 'CreateRandomValue'
   ```

2. **In django_project/settings.py:** 

   1. Replace the ‘insecure’ key with the environment variable

   ```python
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ```

   1. Replace the DEBUG Setting to be only true in Dev and False in Prod Modes.

   ```python
   DEBUG = 'DEV' in os.environ
   ```

   ### **In Heroku / dashboard:**

1. Add your config vars i.e. copy and paste values from env.py into Heroku Config Vars.

| key                   | value                 |
| --------------------- | --------------------- |
| DATABASE_URL          | ... <already set>...  |
| CLOUDINARY_URL        | ... <check env.py>... |
| SECRET_KEY            | ... <check env.py>... |
| DISABLE_COLLECTSTATIC | 1                     |

2. Update the requirements file

   ```
   pip freeze > requirements.txt
   ```

3. add, commit, push changes to GitHub



