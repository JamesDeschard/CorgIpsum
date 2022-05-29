from django.conf import settings

import os
import random

corgi_file = os.path.join(settings.BASE_DIR, 'main', 'static', 'assets')
length = len(os.listdir(corgi_file))

def get_random_img():
    return os.path.join(
        settings.BASE_DIR, 
        'main', 
        'static', 
        'assets', 
        'corgi_{}.jpg'.format(str(random.randint(1, length)))
    )