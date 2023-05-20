from django import forms
from utils.query import *

class RegisterFormUmpire(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=50,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')",
                'oninput': "setCustomValidity('')"
            }
        ),
        required=True
    )
    nama = forms.CharField(
        label='Nama',
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nama',
                'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')",
                'oninput': "setCustomValidity('')"
            }
        ),
        required=True
    )
    negara = forms.CharField(
        label='Negara',
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Negara',
                'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')",
                'oninput': "setCustomValidity('')"
            }
        ),
        required=True
    )
    
class RegisterFormAtlet(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email',
               'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')",
               'oninput': "setCustomValidity('')"}))
    nama = forms.CharField(label='Nama', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nama',
               'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')",
               'oninput': "setCustomValidity('')"}))
    negara = forms.CharField(label='Negara', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Negara',
               'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')",
               'oninput': "setCustomValidity('')"}))
    tanggal_lahir = forms.DateField(label='Tanggal Lahir', widget=forms.DateInput({
        'class': 'form-control', 'type': 'date'}))
    play = forms.ChoiceField(label='Play', choices=[('Kanan', 'Kanan'), ('Kiri', 'Kiri')], widget=forms.RadioSelect(
        attrs={'class': 'form-check-input', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')",
               'oninput': "setCustomValidity('')"}))
    tinggi_badan = forms.IntegerField(label='Tinggi Badan', max_value=400, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Tinggi Badan',
               'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')",
               'oninput': "setCustomValidity('')", 'min': '0'}))
    jenis_kelamin = forms.ChoiceField(label='Jenis Kelamin', choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')], widget=forms.RadioSelect(
        attrs={'class': 'form-check-input', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')",
               'oninput': "setCustomValidity('')"}))
    
class RegisterFormPelatih(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 
               'placeholder': 'Email',
               'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    nama = forms.CharField(label='Nama', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nama', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    negara = forms.CharField(label='Negara', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Negara', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    kategori = forms.MultipleChoiceField(label='Kategori', widget=forms.CheckboxSelectMultiple(
        attrs={'class': 'form-control', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}),
        choices=[
            ('dummy1', 'Dummy 1'),
            ('dummy2', 'Dummy 2'),
            ('dummy3', 'Dummy 3'),
        ]
    )

    