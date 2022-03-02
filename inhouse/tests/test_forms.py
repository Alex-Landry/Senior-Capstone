from django.test import SimpleTestCase
from boardmanlab.forms import FormCreateHelpSession

class FormCreate(SimpleTestCase):
    
    def test_FormCreateHelpSession_is_valid(self):
      
        form = FormCreateHelpSession(data={'date': '2022-03-02','duration': '30', 'topic':'1','time': '14:30:59'})
     
        self.assertTrue(form.is_valid())

    
    def test_FormCreateHelpSession_is_invalid(self):
      
        form = FormCreateHelpSession(data={'date': '03-02-2022','duration': '30', 'topic':'COS125','time': '14:30:59'})
     
        self.assertFalse(form.is_valid())

        
 