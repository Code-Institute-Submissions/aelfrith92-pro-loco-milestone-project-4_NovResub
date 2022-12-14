from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils import timezone

STATUS = ((0, "Draft"), (1, "Scheduled"), (2, "Cancelled"))
AUDIENCE = ((0, "Admin"), (1, "Everyone"))


class Event(models.Model):
    '''This class defines the Event model'''
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_events"
    )
    featured_image = CloudinaryField('image', default='placeholder')
    text_preview = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    joins = models.ManyToManyField(
        User, related_name='blogevent_like', blank=True)
    # The next field sets the date +14 days at the time of creation
    # to give enough time to admins to approve and organize the event
    # if JS is disabled on front-end, the date+14 automatically pre-populates
    # the field in the form
    scheduled_on = models.DateTimeField(default=timezone.now() +
                                        timedelta(days=14))

    class Meta:
        '''The following line defines the ascending order that data is
           retrieved by, based on the field scheduled_on:
           the closer the date, the higher in the page'''
        ordering = ["scheduled_on"]

    def __str__(self):
        '''Returns the title field of the created instance'''
        return self.title

    def number_of_joins(self):
        '''Returns the number of entries/values within the field joins'''
        return self.joins.count()


class Comment(models.Model):
    '''This class defines the comment model'''
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                              related_name="comments")
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    audience = models.IntegerField(choices=AUDIENCE, default=1)
    approved = models.BooleanField(default=False)

    class Meta:
        '''Meta class defining the order of retrieved comments'''
        ordering = ["created_on"]

    def __str__(self):
        '''Returns a string which facilitates a concise approach'''
        return f"Comment {self.body} by {self.name}"
