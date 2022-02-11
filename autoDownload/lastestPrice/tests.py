from django.test import TestCase

# Create your tests here.

import  redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.set('name','zhangwenju')
print(r.get('name'))