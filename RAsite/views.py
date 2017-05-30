from django.http import HttpResponse
import random

def hello_world(request):
	return HttpResponse("Hello World! Yay!")

def root_page(request):
	return HttpResponse("Root home page.")

def random_number(request, min_rand=0, max_rand=100):
	random_num = random.randrange(int(min_rand), int(max_rand))

	msg = "Random number between %s and %s : %d" % (min_rand, max_rand, random_num)

	return HttpResponse(msg)