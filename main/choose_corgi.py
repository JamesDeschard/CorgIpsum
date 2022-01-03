from django.conf import settings

import os
import random

def get_random_img():
    return os.path.join(
        settings.BASE_DIR, 
        'main', 
        'static', 
        'assets', 
        'corgi_{}.jpg'.format(str(random.randint(1, 400)))
    )