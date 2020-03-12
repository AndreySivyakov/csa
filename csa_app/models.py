from django.db import models

class Setup(models.Model):
    date = models.DateTimeField(null=True)
    user_name = models.CharField(max_length=50, null=True)
    contract_type = models.CharField(max_length=100, null=True)
    request_type = models.CharField(max_length=100, null=True)
    paper_contr_type = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, null=True)
    sub_category = models.CharField(max_length=100, null=True)

    def __unicode__(self):
       return self.name

class AmendmentType(models.Model):
    setup_reference = models.ForeignKey(Setup, on_delete=models.CASCADE, blank=True, null=True)
    amendment_type = models.CharField(max_length=500, null=True)

    def __unicode__(self):
       return self.name

class ParentContract(models.Model):
    parent_contract_setup_ref = models.ForeignKey(Setup, on_delete=models.CASCADE, blank=True, null=True)
    parent_vendor_number = models.PositiveIntegerField(null=True, default=None)
    parent_vendor_name = models.CharField(max_length=100, null=True, blank=True)
    parent_contr_name = models.CharField(max_length=40, null=True, blank=True)
    parent_PGrp = models.CharField(max_length=50, null=True, blank=True)
    parent_POrg = models.CharField(max_length=50, null=True, blank=True)
    parent_contr_number = models.BigIntegerField(null=True, default=None)

    def __unicode__(self):
       return self.name

class ChildContract(models.Model):
    child_contract_setup_ref = models.ForeignKey(Setup, on_delete=models.CASCADE, blank=True, null=True)
    child_vendor_number = models.PositiveIntegerField(null=True, default=None)
    child_vendor_name = models.CharField(max_length=100, null=True, blank=True)
    child_contr_name = models.CharField(max_length=100, null=True, blank=True)
    child_PGrp = models.CharField(max_length=50, null=True, blank=True)
    child_POrg = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
       return self.name

class Form2(models.Model):
    form2_setup_ref = models.ForeignKey(Setup, on_delete=models.CASCADE, blank=True, null=True)
    form2_parent_field_ref = models.IntegerField(null=True, default=None)
    form2_contr_num = models.BigIntegerField(null=True, default=None)
    form2_contr_name = models.CharField(max_length=100, null=True, blank=True)
    form2_vendor_number = models.PositiveIntegerField(null=True, default=None)
    form2_vendor_name = models.CharField(max_length=100, null=True, blank=True)
    form2_validity_start = models.DateTimeField(null=True)
    form2_validity_end = models.DateTimeField(null=True)
    form2_POrg = models.CharField(max_length=100, null=True, blank=True)
    form2_PGrp = models.CharField(max_length=100, null=True, blank=True)
    form2_target_value = models.BigIntegerField(null=True, default=None)
    form2_currency = models.CharField(max_length=100, null=True, blank=True)
    form2_payment_terms = models.CharField(max_length=100, null=True, blank=True)
    form2_incoterm = models.CharField(max_length=100, null=True, blank=True)
    form2_reasons_for_outside = models.CharField(max_length=100, null=True, blank=True)
    form2_child_or_parent = models.CharField(max_length=20, null=True, blank=True)
    form2_owner_email = models.EmailField(max_length=100, null=True, blank=True)
    form2_plant_location = models.CharField(max_length=100, null=True, blank=True)
    form2_lock_unlock = models.CharField(max_length=10, null=True, blank=True)

    def __unicode__(self):
       return self.name

class Form5(models.Model):
    form5_setup_ref = models.ForeignKey(Setup, on_delete=models.CASCADE, blank=True, null=True)
    form5_1 = models.BooleanField(default=False)
    form5_2 = models.BooleanField(default=False)
    form5_3 = models.BooleanField(default=False)
    form5_4 = models.BooleanField(default=False)
    form5_5 = models.BooleanField(default=False)
    form5_6 = models.BooleanField(default=False)
    form5_7 = models.BooleanField(default=False)
    form5_8 = models.BooleanField(default=False)
    form5_9 = models.BooleanField(default=False)
    form5_10 = models.BooleanField(default=False)
    form5_11 = models.BooleanField(default=False)
    form5_12 = models.BooleanField(default=False)
    form5_13 = models.BooleanField(default=False)
    form5_14 = models.BooleanField(default=False)
    form5_15 = models.BooleanField(default=False)

    def __unicode__(self):
       return self.name
