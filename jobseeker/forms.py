from .models import Lowongan
from django.forms import ModelForm, DateInput, TextInput, Textarea
from django.utils.translation import gettext_lazy as _

class BukaLowonganForm(ModelForm):
    class Meta:
        model = Lowongan
        exclude = [
            'users_id',
            'id',
            'created_at',
            'updated_at',
            'status',
        ]

        widgets = {
        'posisi' : TextInput(
            attrs= {
                'placeholder' : "Posisi Pekerjaan",
                'class' : 'form-control',
            }
        ),
        'gaji' : TextInput(
            attrs= {
                'placeholder' : "Gaji",
                'class' : 'form-control',
                'type' : 'number'
            }
        ),
        'lama_pengalaman' : TextInput(
            attrs= {
                'placeholder' : "Pengalaman tahun yang dibutuhkan",
                'class' : 'form-control',
                'type': 'number'      
            }
        ),
        'buka_lowongan': DateInput(
            format=('%m/%d/%Y'), 
            
            attrs={
                'class' : 'form-control',
                'type' : 'date',
            }
        ),
        'batas_pengumpulan' : DateInput(
            format=('%m/%d/%Y'), 
            attrs={
                'class' : 'form-control',
                'type' :'date'
            }
        ),
    }