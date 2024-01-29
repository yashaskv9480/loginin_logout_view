from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save,post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out,user_login_failed
from django.dispatch import receiver


class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now = True)
    logout_time = models.DateTimeField(null=True, blank=True)
    total_time_spent = models.DurationField(null=True, blank=True)

    def __str__(self) :
        return f"{self.user}"
    
@receiver(user_logged_in)
def user_logged_in(sender,request,user,**kwargs):
    UserLog.objects.create(user=user)


@receiver(user_logged_out)
def user_logged_out(sender,request,user, **kwargs):
    user_log=UserLog.objects.filter(user=user,logout_timeis_null=True).first()
    if user_log:
        user_log.logout_time=user_log.login_time
        user_log.save()

# @receiver(user_logged_in)
# def user_logged_in(sender, instance, created, **kwargs) :
#     if created :
#         UserLog.objects.create(user = instance)


# @receiver(user_logged_out)
# def user_logged_out(sender, instance, **kwargs) :
#     instance.account.save()



# post_save.connect(user_logged_in,sender=User)
# post_save.connect(user_logged_out,sender=User)

@receiver(pre_save, sender=UserLog)
def calculate_total_time_spent(sender, instance, **kwargs):
    if instance.logout_time and instance.login_time:
        instance.total_time_spent = instance.logout_time - instance.login_time


# class UserLog(models.Model):
#     action = models.CharField(max_length=64)
#     ip = models.GenericIPAddressField(null=True)
#     username = models.CharField(max_length=256, null=True)

#     def __unicode__(self):
#         return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)

#     def __str__(self):
#         return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)


# @receiver(user_logged_in)
# def user_logged_in_callback(sender, request, user, **kwargs):  
#     ip = request.META.get('REMOTE_ADDR')
#     UserLog.objects.create(action='user_logged_in', ip=ip, username=user.username)


# @receiver(user_logged_out)
# def user_logged_out_callback(sender, request, user, **kwargs):  
#     ip = request.META.get('REMOTE_ADDR')
#     UserLog.objects.create(action='user_logged_out', ip=ip, username=user.username)


# @receiver(user_login_failed)
# def user_login_failed_callback(sender, credentials, **kwargs):
#     UserLog.objects.create(action='user_login_failed', username=credentials.get('username', None))
