from django.test import SimpleTestCase
from boardmanlab.forms import FormCreateHelpSession
from boardmanlab.forms import FormEditHelpSession
from boardmanlab.forms import FormFilterDate

class FormCreate(SimpleTestCase):
    #boardmanlab app unit tests
    def test_FormCreateHelpSession_is_valid(self):
      
        form = FormCreateHelpSession(data={'date': '2022-03-02','duration': '30', 'topic':'1','time': '14:30:59'})
     
        self.assertTrue(form.is_valid())

        #tests invalid strings
    def test_FormCreateHelpSession_is_invalid(self):
      
        form = FormCreateHelpSession(data={'date': '03-02-2022','duration': '30', 'topic':'COS125','time': '14:30:59'})
     
        self.assertFalse(form.is_valid())

        #Edit helpsession under progress
    
        #tests that filter accepts valid data
    def test_Form_Filter_Date_is_valid(self):
        form = FormFilterDate(data={'month': '5', 'year': '2023'})

        self.assertTrue(form.is_valid())
        #tests that filter doesnt accept invalid data
    def test_Form_Filter_Date_is_invalid(self): 
        form = FormFilterDate(data={'month': '23', 'year': '202988'})

        self.assertFalse(form.is_valid())

    