from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _
from .list_objects import *

class SetupForm(forms.ModelForm):

    class Meta:
        model = Setup
        fields = '__all__'

class AmendmentTypeForm(forms.ModelForm):

    class Meta:
        model = AmendmentType
        fields = '__all__'

my_fields_parent = ['parent_vendor_number','parent_vendor_name','parent_contr_name','parent_PGrp','parent_POrg']

PGRps = PGRps_list
POrgs = POrgs_list
currency = currency_list
payment_terms = payment_terms_list
reasons_for_outside = reasons_for_outside_list

form2_parent_fields = \
[
    'form2_contr_num','form2_contr_name','form2_vendor_number','form2_vendor_name','form2_validity_start','form2_validity_end',
    'form2_POrg','form2_PGrp','form2_target_value','form2_currency','form2_payment_terms','form2_reasons_for_outside'
]
form2_child_fields = \
[
    'form2_contr_num','form2_contr_name','form2_vendor_number','form2_vendor_name','form2_validity_start','form2_validity_end',
    'form2_POrg','form2_PGrp','form2_target_value','form2_currency','form2_payment_terms','form2_reasons_for_outside'
]
form2_amendment_fields = \
[
    'form2_contr_num', 'form2_validity_end', 'form2_contr_name', 'form2_PGrp', 'form2_owner_email'
]

class ParentContractForm(forms.ModelForm):

    parent_contr_name = forms.CharField(required=True)
    parent_vendor_number = forms.IntegerField(required=False, min_value=1)
    parent_vendor_name = forms.CharField(required=False)
    parent_PGrp = forms.ChoiceField(choices=PGRps, required=False)
    parent_POrg = forms.ChoiceField(choices=POrgs, required=True)

    class Meta:
        model = ParentContract
        fields = my_fields_parent

    def __init__(self, *args, **kwargs):
        super(ParentContractForm, self).__init__(*args, **kwargs)
        self.fields['parent_vendor_number'].widget.attrs['placeholder'] = _('Vendor #')
        self.fields['parent_vendor_name'].widget.attrs['placeholder'] = _('Vendor name')
        self.fields['parent_contr_name'].widget.attrs['placeholder'] = _('Contract name (max 40 characters, no special characters)')
        self.fields['parent_contr_name'].widget.attrs['maxlength'] = _('40')
        self.fields['parent_contr_name'].widget.attrs['pattern'] = _('[A-Za-z0-9 ]+')
        self.fields['parent_contr_name'].widget.attrs.update({'style' : 'border-color: red;'})
        self.fields['parent_POrg'].widget.attrs.update({'style' : 'border-color: red;'})
        for field in my_fields_parent:
            self.fields[field].label = ''
            self.fields[field].widget.attrs['class'] = 'form-control input-sm'

my_fields_child = ['child_vendor_number','child_vendor_name','child_contr_name','child_PGrp','child_POrg']

class ChildContractForm(forms.ModelForm):

    child_contr_name = forms.CharField(required=True)
    child_vendor_number = forms.IntegerField(required=False, min_value=1)
    child_vendor_name = forms.CharField(required=False)
    child_PGrp = forms.ChoiceField(choices=PGRps, required=False)
    child_POrg = forms.ChoiceField(choices=POrgs, required=True)

    class Meta:
        model = ChildContract
        fields = my_fields_child

    def __init__(self, *args, **kwargs):
        super(ChildContractForm, self).__init__(*args, **kwargs)
        self.fields['child_vendor_number'].widget.attrs['placeholder'] = _('Vendor #')
        self.fields['child_vendor_name'].widget.attrs['placeholder'] = _('Vendor name')
        self.fields['child_contr_name'].widget.attrs['placeholder'] = _('Contract name (max 40 characters, no special characters)')
        self.fields['child_contr_name'].widget.attrs['maxlength'] = _('40')
        self.fields['child_contr_name'].widget.attrs['pattern'] = _('[A-Za-z0-9 ]+')
        #self.fields['child_contr_name'].help_text = '* mandatory field'
        self.fields['child_contr_name'].widget.attrs.update({'style' : 'border-color: red;'})
        self.fields['child_POrg'].widget.attrs.update({'style' : 'border-color: red;'})
        for field in my_fields_child:
            self.fields[field].label = ''
            self.fields[field].widget.attrs['class'] = 'form-control input-sm'

class ParentContrNumberForm(forms.ModelForm):

    parent_contr_number = forms.IntegerField(required=True, min_value=4600000000, max_value=4699999999)

    class Meta:
        model = ParentContract
        fields = ['parent_contr_number']

    def __init__(self, *args, **kwargs):
        super(ParentContrNumberForm, self).__init__(*args, **kwargs)
        self.fields['parent_contr_number'].label = ''
        self.fields['parent_contr_number'].widget.attrs['placeholder'] = _('Parent contract #')
        self.fields['parent_contr_number'].widget.attrs['class'] = 'form-control input-sm'
        self.fields['parent_contr_number'].widget.attrs.update({'style' : 'border-color: red;'})


class ParentContrNumberFormFirstRelease(forms.ModelForm):

    parent_contr_number = forms.IntegerField(required=True, min_value=4600000000, max_value=4699999999)

    class Meta:
        model = ParentContract
        fields = ['parent_contr_number']

    def __init__(self, *args, **kwargs):
        super(ParentContrNumberFormFirstRelease, self).__init__(*args, **kwargs)
        self.fields['parent_contr_number'].label = ''
        self.fields['parent_contr_number'].widget.attrs['placeholder'] = _('Parent contract #')
        self.fields['parent_contr_number'].widget.attrs['class'] = 'form-control input-sm'


mult_children = forms.formset_factory(ChildContractForm, min_num=1, max_num=15, extra=14, can_delete=True)


# not used, keep for reference on how to raise validation erros in formset
class BaseChildContrFormSet (forms.BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            contr_name = form.cleaned_data.get('child_contr_name')
            child_POrg = form.cleaned_data.get('child_POrg')
            if contr_name is None:
                raise forms.ValidationError("Contract Names cannot be blank.")
            elif contr_name.isspace():
                raise forms.ValidationError("Contract Names cannot be blank.")
            elif not contr_name.isalnum():
                raise forms.ValidationError("Contract Name must include only alphanumeric characters.")
            elif child_POrg is None:
                raise forms.ValidationError("Select Child Contract POrg from the list.")

class DateInput(forms.DateInput):
    input_type = 'date'

class Form2FormParent (forms.ModelForm):


    form2_contr_name = forms.CharField(required=True)
    form2_vendor_number = forms.IntegerField(required=True, min_value=1)
    form2_vendor_name = forms.CharField(required=True)
    form2_PGrp = forms.ChoiceField(choices=PGRps, required=True)
    form2_POrg = forms.ChoiceField(choices=POrgs, required=True)
    form2_currency = forms.ChoiceField(choices=currency, required=True)
    form2_payment_terms = forms.ChoiceField(choices=payment_terms, required=True)
    form2_reasons_for_outside = forms.ChoiceField(choices=reasons_for_outside, required=False)
    form2_target_value = forms.IntegerField(required=False)
    form2_contr_num = forms.IntegerField(required=True, min_value=4600000000, max_value=4699999999)

    class Meta:
        model = Form2
        widgets = {'form2_validity_start' : DateInput(), 'form2_validity_end' : DateInput()}
        fields = form2_parent_fields

    def __init__(self, *args, **kwargs):
        super(Form2FormParent, self).__init__(*args, **kwargs)
        self.fields['form2_vendor_number'].widget.attrs['placeholder'] = _('Vendor #')
        self.fields['form2_vendor_name'].widget.attrs['placeholder'] = _('Vendor name')
        self.fields['form2_contr_name'].widget.attrs['placeholder'] = _('Contract name (max 40 characters, no special characters)')
        self.fields['form2_contr_name'].widget.attrs['pattern'] = _('[A-Za-z0-9 ]+')
        self.fields['form2_contr_name'].widget.attrs['maxlength'] = _('40')
        self.fields['form2_contr_num'].widget.attrs['placeholder'] = _('Contract #')
        self.fields['form2_target_value'].widget.attrs['placeholder'] = _('Overal SRM contract target value ($)')
        self.fields['form2_currency'].widget.attrs['placeholder'] = _('Currency')
        self.fields['form2_payment_terms'].widget.attrs['placeholder'] = _('Payment Terms')
        self.fields['form2_validity_start'].help_text = 'Validity Start Date'
        self.fields['form2_validity_end'].help_text = 'Validity End Date'
        self.fields['form2_contr_name'].help_text = 'Contract Name must not contain special characters'
        for field in form2_parent_fields:
            self.fields[field].label = ''
            self.fields[field].widget.attrs['class'] = 'form-control input-sm'



class Form2FormChild (forms.ModelForm):

    class Meta:
        model = Form2
        widgets = {'form2_validity_start' : DateInput(), 'form2_validity_end' : DateInput()}
        fields = form2_child_fields



class Form2Amendment(forms.ModelForm):

    form2_contr_num = forms.IntegerField(required=True, min_value=4600000000, max_value=4699999999)
    form2_contr_name = forms.CharField(required=True)
    form2_PGrp = forms.ChoiceField(choices=PGRps, required=True)
    form2_owner_email = forms.EmailField(required=True, max_length=100)

    class Meta:
        model = Form2
        widgets = {'form2_validity_end' : DateInput()}
        fields = form2_amendment_fields

    def __init__(self, *args, **kwargs):
        super(Form2Amendment, self).__init__(*args, **kwargs)
        self.fields['form2_contr_num'].widget.attrs['placeholder'] = _('Contract #')
        self.fields['form2_validity_end'].help_text = 'Validity End Date'
        self.fields['form2_contr_name'].widget.attrs['placeholder'] = _('Contract name (max 40 characters, no special characters)')
        self.fields['form2_contr_name'].widget.attrs['pattern'] = _('[A-Za-z0-9 ]+')
        self.fields['form2_contr_name'].widget.attrs['maxlength'] = _('40')
        self.fields['form2_owner_email'].widget.attrs['placeholder'] = _('New contract owner email')
        for field in form2_amendment_fields:
            self.fields[field].label = ''
            self.fields[field].widget.attrs['class'] = 'form-control input-sm'

class Form2AmendmentHeader(forms.ModelForm):

    form2_contr_num = forms.IntegerField(required=True, min_value=4600000000, max_value=4699999999)
    form2_contr_name = forms.CharField(required=True)
    form2_PGrp = forms.ChoiceField(choices=PGRps, required=True)
    form2_owner_email = forms.EmailField(required=True, max_length=100)

    class Meta:
        model = Form2
        fields = ['form2_contr_num','form2_contr_name','form2_PGrp','form2_owner_email']

    def __init__(self, *args, **kwargs):
        super(Form2AmendmentHeader, self).__init__(*args, **kwargs)
        self.fields['form2_contr_num'].widget.attrs['placeholder'] = _('Contract #')
        self.fields['form2_contr_name'].widget.attrs['placeholder'] = _('Contract name (max 40 characters, no special characters)')
        self.fields['form2_contr_name'].widget.attrs['pattern'] = _('[A-Za-z0-9 ]+')
        self.fields['form2_contr_name'].widget.attrs['maxlength'] = _('40')
        self.fields['form2_owner_email'].widget.attrs['placeholder'] = _('New contract owner email')
        for field in self.fields:
            self.fields[field].label = ''
            self.fields[field].widget.attrs['class'] = 'form-control input-sm'


class Form2AmendmentDate(forms.ModelForm):

    class Meta:
        model = Form2
        widgets = {'form2_validity_end' : DateInput()}
        fields = ['form2_contr_num','form2_validity_end']

    def __init__(self, *args, **kwargs):
        super(Form2AmendmentDate, self).__init__(*args, **kwargs)
        self.fields['form2_contr_num'].widget.attrs['placeholder'] = _('Contract #')
        self.fields['form2_validity_end'].help_text = 'Validity End Date'
        for field in self.fields:
            self.fields[field].label = ''
            self.fields[field].widget.attrs['class'] = 'form-control input-sm'


class Form5Form(forms.ModelForm):

    form5_1 = forms.BooleanField(required=False)
    form5_2 = forms.BooleanField(required=False)
    form5_3 = forms.BooleanField(required=False)
    form5_4 = forms.BooleanField(required=False)
    form5_5 = forms.BooleanField(required=False)
    form5_6 = forms.BooleanField(required=False)
    form5_7 = forms.BooleanField(required=False)
    form5_8 = forms.BooleanField(required=False)
    form5_9 = forms.BooleanField(required=False)
    form5_10 = forms.BooleanField(required=False)
    form5_11 = forms.BooleanField(required=False)
    form5_12 = forms.BooleanField(required=False)
    form5_13 = forms.BooleanField(required=False)
    form5_14 = forms.BooleanField(required=False)
    form5_15 = forms.BooleanField(required=False)

    class Meta:
        model = Form5
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(Form5Form, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = ''
            self.fields[field].widget.attrs['class'] = 'form-check-input'


class Form2ChildFirstReleaseForm (forms.ModelForm):

    form2_contr_name = forms.CharField(required=True)
    form2_vendor_number = forms.IntegerField(required=True, min_value=1)
    form2_vendor_name = forms.CharField(required=True)
    form2_PGrp = forms.ChoiceField(choices=PGRps, required=True)
    form2_POrg = forms.ChoiceField(choices=POrgs, required=True)
    form2_currency = forms.ChoiceField(choices=currency, required=True)
    form2_payment_terms = forms.ChoiceField(choices=payment_terms, required=True)
    form2_reasons_for_outside = forms.ChoiceField(choices=reasons_for_outside, required=False)
    form2_target_value = forms.IntegerField(required=True)
    form2_contr_num = forms.IntegerField(required=True, min_value=4600000000, max_value=4699999999)
    form2_incoterm = forms.ChoiceField(choices=incoterms_list, required=True)

    class Meta:
        model = Form2
        widgets = {'form2_validity_start' : DateInput(), 'form2_validity_end' : DateInput()}
        fields = ['form2_contr_name','form2_vendor_number','form2_vendor_name','form2_PGrp','form2_POrg',
            'form2_currency','form2_payment_terms','form2_reasons_for_outside','form2_target_value',
            'form2_contr_num','form2_incoterm','form2_validity_start','form2_validity_end']

    def __init__(self, *args, **kwargs):
        super(Form2ChildFirstReleaseForm, self).__init__(*args, **kwargs)
        self.fields['form2_vendor_number'].widget.attrs['placeholder'] = _('Vendor #')
        self.fields['form2_vendor_name'].widget.attrs['placeholder'] = _('Vendor name')
        self.fields['form2_contr_name'].widget.attrs['placeholder'] = _('Contract name (max 40 characters, no special characters)')
        self.fields['form2_contr_name'].widget.attrs['pattern'] = _('[A-Za-z0-9 ]+')
        self.fields['form2_contr_name'].widget.attrs['maxlength'] = _('40')
        self.fields['form2_contr_num'].widget.attrs['placeholder'] = _('Contract #')
        self.fields['form2_target_value'].widget.attrs['placeholder'] = _('Overall SRM contract target value ($)')
        self.fields['form2_currency'].widget.attrs['placeholder'] = _('Currency')
        self.fields['form2_payment_terms'].widget.attrs['placeholder'] = _('Payment Terms')
        self.fields['form2_validity_start'].help_text = 'Validity Start Date'
        self.fields['form2_validity_end'].help_text = 'Validity End Date'
        self.fields['form2_contr_name'].help_text = 'Contract Name must not contain special characters'
        for field in self.fields:
            self.fields[field].label = ''
            self.fields[field].widget.attrs['class'] = 'form-control input-sm'


class Form2AmendTargetValueOption1Form (forms.ModelForm):

    form2_POrg = forms.ChoiceField(choices=POrgs, required=True)
    form2_payment_terms = forms.ChoiceField(choices=payment_terms, required=True)
    form2_target_value = forms.IntegerField(required=True)
    form2_contr_num = forms.IntegerField(required=True, min_value=4600000000, max_value=4699999999)
    form2_plant_location = forms.ChoiceField(choices=plant_location_list, required=False)

    class Meta:
        model = Form2
        fields = ['form2_POrg','form2_payment_terms','form2_target_value','form2_contr_num','form2_plant_location']

    def __init__(self, *args, **kwargs):
        super(Form2AmendTargetValueOption1Form, self).__init__(*args, **kwargs)
        self.fields['form2_contr_num'].widget.attrs['placeholder'] = _('Contract #')
        self.fields['form2_target_value'].widget.attrs['placeholder'] = _('New target $ value at distribution')
        self.fields['form2_payment_terms'].widget.attrs['placeholder'] = _('Payment Terms')
        for field in self.fields:
            self.fields[field].label = ''
            self.fields[field].widget.attrs['class'] = 'form-control input-sm'
            if field != 'form2_plant_location':
                self.fields[field].widget.attrs.update({'style' : 'border-color: red;'})

class Form2AmendTargetValueOption2Form (forms.ModelForm):

    form2_target_value = forms.IntegerField(required=True)
    form2_contr_num = forms.IntegerField(required=True, min_value=4600000000, max_value=4699999999)

    class Meta:
        model = Form2
        fields = ['form2_target_value','form2_contr_num']

    def __init__(self, *args, **kwargs):
        super(Form2AmendTargetValueOption2Form, self).__init__(*args, **kwargs)
        self.fields['form2_contr_num'].widget.attrs['placeholder'] = _('Contract #')
        self.fields['form2_target_value'].widget.attrs['placeholder'] = _('Overall SRM contract target $ value')
        for field in self.fields:
            self.fields[field].label = ''
            self.fields[field].widget.attrs['class'] = 'form-control input-sm'

class Form2AmendDateExtensionOption1Form (forms.ModelForm):

    form2_contr_num = forms.IntegerField(required=True, min_value=4600000000, max_value=4699999999)

    class Meta:
        model = Form2
        fields = ['form2_validity_end','form2_contr_num']
        widgets = {'form2_validity_end' : DateInput()}

    def __init__(self, *args, **kwargs):
        super(Form2AmendDateExtensionOption1Form, self).__init__(*args, **kwargs)
        self.fields['form2_validity_end'].help_text = 'Validity End Date'
        self.fields['form2_contr_num'].widget.attrs['placeholder'] = _('Contract #')
        for field in self.fields:
            self.fields[field].label = ''
            self.fields[field].widget.attrs['class'] = 'form-control input-sm'

class Form2AmendHeaderDetailsOption1FormParent (forms.ModelForm):

    form2_contr_name = forms.CharField(required=True)
    form2_PGrp = forms.ChoiceField(choices=PGRps, required=True)
    form2_contr_num = forms.IntegerField(required=True, min_value=4600000000, max_value=4699999999)
    form2_owner_email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control',
        'placeholder':'New contract owner email'}))

    class Meta:
        model = Form2
        fields = ['form2_contr_name','form2_PGrp','form2_contr_num','form2_owner_email']

    def __init__(self, *args, **kwargs):
        super(Form2AmendHeaderDetailsOption1FormParent, self).__init__(*args, **kwargs)
        self.fields['form2_contr_name'].widget.attrs['placeholder'] = _('Contract name (max 40 characters, no special characters)')
        self.fields['form2_contr_name'].widget.attrs['pattern'] = _('[A-Za-z0-9 ]+')
        self.fields['form2_contr_name'].widget.attrs['maxlength'] = _('40')
        self.fields['form2_contr_num'].widget.attrs['placeholder'] = _('Contract #')
        self.fields['form2_contr_name'].help_text = 'Contract Name must not contain special characters'
        for field in self.fields:
            self.fields[field].label = ''
            self.fields[field].widget.attrs['class'] = 'form-control input-sm'

class Form2AmendHeaderDetailsOption1FormChild (forms.ModelForm):

    form2_contr_name = forms.CharField(required=True)
    form2_PGrp = forms.ChoiceField(choices=PGRps, required=True)
    form2_contr_num = forms.IntegerField(required=True, min_value=4600000000, max_value=4699999999)
    form2_incoterm = forms.ChoiceField(choices=incoterms_list, required=True)
    form2_owner_email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control',
        'placeholder':'New contract owner email'}))

    class Meta:
        model = Form2
        fields = ['form2_contr_name','form2_PGrp','form2_contr_num','form2_owner_email','form2_incoterm']

    def __init__(self, *args, **kwargs):
        super(Form2AmendHeaderDetailsOption1FormChild, self).__init__(*args, **kwargs)
        self.fields['form2_contr_name'].widget.attrs['placeholder'] = _('Contract name (max 40 characters, no special characters)')
        self.fields['form2_contr_name'].widget.attrs['pattern'] = _('[A-Za-z0-9 ]+')
        self.fields['form2_contr_name'].widget.attrs['maxlength'] = _('40')
        self.fields['form2_contr_num'].widget.attrs['placeholder'] = _('Contract #')
        self.fields['form2_contr_name'].help_text = 'Contract Name must not contain special characters'
        for field in self.fields:
            self.fields[field].label = ''
            self.fields[field].widget.attrs['class'] = 'form-control input-sm'

class Form2AmendHeaderDetailsOption2FormParent (forms.ModelForm):

    form2_contr_num = forms.IntegerField(required=True, min_value=4600000000, max_value=4699999999)

    class Meta:
        model = Form2
        fields = ['form2_contr_num', 'form2_owner_email']

    def __init__(self, *args, **kwargs):
        super(Form2AmendHeaderDetailsOption2FormParent, self).__init__(*args, **kwargs)
        self.fields['form2_contr_num'].widget.attrs['placeholder'] = _('Contract #')
        for field in self.fields:
            self.fields[field].label = ''
            self.fields[field].widget.attrs['class'] = 'form-control input-sm'

class Form2AmendPaymentTermsFormOpt1 (forms.ModelForm):

    form2_contr_num = forms.IntegerField(required=True, min_value=4600000000, max_value=4699999999)
    form2_payment_terms = forms.ChoiceField(choices=payment_terms, required=True)

    class Meta:
        model = Form2
        fields = ['form2_contr_num','form2_payment_terms']

    def __init__(self, *args, **kwargs):
        super(Form2AmendPaymentTermsFormOpt1, self).__init__(*args, **kwargs)
        self.fields['form2_contr_num'].widget.attrs['placeholder'] = _('Contract #')
        for field in self.fields:
            self.fields[field].label = ''
            self.fields[field].widget.attrs['class'] = 'form-control input-sm'

class UnlockForm(forms.ModelForm):

    form2_contr_num = forms.IntegerField(required=False, min_value=4600000000, max_value=4699999999)
    form2_lock_unlock = forms.ChoiceField(choices=[(None,'Select Lock or Unlock'),('Lock','Lock'),('Unlock','Unlock')], required=False)

    class Meta:
        model = Form2
        fields = ['form2_contr_num','form2_lock_unlock']

    def __init__(self, *args, **kwargs):
        super(UnlockForm, self).__init__(*args, **kwargs)
        self.fields['form2_contr_num'].widget.attrs['placeholder'] = _('Contract #')
        for field in self.fields:
            self.fields[field].label = ''
            self.fields[field].widget.attrs['class'] = 'form-control input-sm'
