from genericpath import exists
from urllib import response
from django.test import SimpleTestCase
from django.urls import reverse,resolve
from boardmanlab.views import login, index, success
    #tests that urls are up and running correctly
class TestUrls(SimpleTestCase):
    #SC stands for status code
    def test_url_index_SC(self):
        response = self.client.get('/home')
        self.assertEquals(response.status_code, 200)
    
    def test_url_login_SC(self):
        response = self.client.get('')
        self.assertEquals(response.status_code, 200)
    
    def test_url_helpsessions_SC(self):
        response = self.client.get('/helpsessions')
        self.assertEquals(response.status_code, 200)

    def test_url_managehelpsessions_SC(self):
        response = self.client.get('/manageHelpSession')
        self.assertEquals(response.status_code, 200)

    
        
    
      