from django.forms import ModelForm
from .models import Animal,Fact

class AnimalForm(ModelForm):
    class Meta:
        model = Animal
        fields = '__all__'
        
class FactForm(ModelForm):
    class Meta:
        model = Fact
        fields = '__all__'