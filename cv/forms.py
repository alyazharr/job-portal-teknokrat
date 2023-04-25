# make a form for USER model and CV model
# the form is used to edit the user and cv data

from django import forms
from django.contrib.auth.forms import UserCreationForm
from jobseeker.models import CV, Users
from django.forms import DateInput

class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Users
        fields = ['email', 'name', 'no_telp', 'alamat', 'tempat_lahir', 'tgl_lahir', 'ipk']
        exclude = ['password']    
        widgets= {
            'tgl_lahir': DateInput(attrs={'type': 'date'}),
        } 

class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['prestasi', 'kemampuan', 'keterangan_pendidikan', 'asal_sekolah', 'masa_waktu', 'instansi', 'keterangan_posisi']
        exclude = ['users_id', 'id', 'created_at', 'updated_at', 'status',]
        

