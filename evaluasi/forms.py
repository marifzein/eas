from django import forms

class FormEvaluasi(forms.Form):
       
    def __init__(self, soals, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # widget_attrs = {}
        

        for soal in soals:
            choices = [(pilihan.kode, pilihan.teks) for pilihan in soal.pilihan.all()]
            self.fields[f"soal_{soal.id}"] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect,
                label=soal.pertanyaan
            )
            # widget=forms.RadioSelect(attrs=widget_attrs),
        