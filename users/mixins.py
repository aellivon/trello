
from django.http import HttpResponseRedirect
from django.urls import reverse


class ThrowHomeIfNotLoggedInMixIn(object):
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse('boards:home' , kwargs={'username':
                	request.user.get_username() 
                }))

