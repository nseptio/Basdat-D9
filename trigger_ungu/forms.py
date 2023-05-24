from django import forms
from utils.query import *

def get_available_sponsor(atlet_email):
    list_sponsor = []
    cursor.execute(f"""
    SELECT S.nama_brand
    FROM SPONSOR S
    WHERE S.id NOT IN (
        SELECT id_sponsor
        FROM ATLET_SPONSOR ATS
        JOIN ATLET A ON A.id = ATS.id_atlet
        NATURAL JOIN MEMBER M
        WHERE M.email = '{atlet_email}'
    );
    """)
    record = cursor.fetchall()
    list_sponsor = [i[0] for i in record]
    return list_sponsor

class SponsorRegistrationForm(forms.Form):
    def __init__(self, email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        available_sponsors = get_available_sponsor(email)

        self.fields['sponsor'] = forms.ChoiceField(
            choices= [('', 'Pilih Sponsor')] + [(sponsor, sponsor) for sponsor in available_sponsors],
            widget=forms.Select(attrs={'class': 'form-control'})
        )

        self.fields['tanggal_mulai'] = forms.DateField(
            widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        )

        self.fields['tanggal_selesai'] = forms.DateField(
            widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        )
    