from django.test import TestCase, Client, override_settings
from PIL import Image

from .models import Counter
from .resize import GetAndModifyImage

client = Client()

MONOCHROMATIC_MAX_VARIANCE = 0.005
COLOR = 1000
MAYBE_COLOR = 100

def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png')
    return temp_file

def is_grey_scale(img):
    img = img.convert('RGB')
    w, h = img.size
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i,j))
            if r != g != b: 
                return False
    return True

class TestCounter(TestCase):
    def test_counter(self):
        counter = Counter.objects.first()
        self.assertTrue(type(counter), int)

class TestImageView(TestCase):
    def test_home_page(self):
        Counter.objects.create(counter=0)
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')
        
    def test_image_view(self):
        Counter.objects.create(counter=0)
        response = client.get('/100')
        self.assertEqual(response.status_code, 200)
        
        response = client.get('/100/100')
        self.assertEqual(response.status_code, 200)
        
        response = client.get('/100/100/sepia')
        self.assertEqual(response.status_code, 200)
        
        response = client.get('/100/100/sepia/helloworld')
        self.assertEqual(response.status_code, 404)
        
        response = client.get('/helloworld')
        self.assertEqual(response.status_code, 404)
        
        response = client.get('/0/')
        self.assertEqual(response.status_code, 404)


class TestResize(TestCase):
    def test_image(self):        
        image = GetAndModifyImage(100, 100).resize()
        self.assertEqual(image.size, (100, 100))
        
        image = GetAndModifyImage(100, 200).resize()
        self.assertEqual(image.size, (100, 200))
        
        image = GetAndModifyImage(200, 100, 'blackandwhite').resize()
        image = is_grey_scale(image)
        self.assertEqual(image, True)
        
        image = GetAndModifyImage(200, 100, 'grayscale').resize()
        image = is_grey_scale(image)
        self.assertEqual(image, True)
        
        
        
        
    
        

        
