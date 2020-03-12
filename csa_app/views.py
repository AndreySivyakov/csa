from django.shortcuts import render, redirect
from .forms import *
from .models import *
from datetime import date as today_date
from django.forms.formsets import formset_factory
import csv
from django.http import HttpResponse
from django.contrib import messages
import json
import os
from django.conf import settings
from .list_objects import form5_items_dict


# Create your views here.
form_5_for_lock_unlock_non_NDA = False

def home_page(request):
    global lock_unlock_NDA
    lock_unlock_NDA = True
    if request.method == 'POST':
        if request.POST.get('submission_check') == 'yes':

            clear_variables()

            global REC_ID
            REC_ID = None

            # save record's data
            record = Setup.objects.create(
                date = today_date.today(),
                user_name = request.POST.get('user_name'),
                contract_type = request.POST.get('contract_type'),
                request_type = request.POST.get('type_of_request'),
                paper_contr_type = request.POST.get('paper_contr_type'),
                category = request.POST.get('optcat'),
                sub_category = request.POST.get('optsubcat')
            )
            # get record id
            REC_ID = Setup.objects.get(id=record.id)
            # save amendment data
            for i in range(1,6):
                boxInd = 'box'+str(i)
                amendInstance = request.POST.get(boxInd)
                if amendInstance is not None:
                    AmendmentType.objects.create(
                    setup_reference=REC_ID,
                    amendment_type=amendInstance)

            if request.POST.get('contract_type') == "Non-Disclosure Agreement":
                if request.POST.get('type_of_request') == "First Release (Parent and/or Child)":
                    return redirect('/redirect-form2-first-release_NDA/', permanent=True)
                elif request.POST.get('type_of_request') == "First Create (Parent and/or Child)":
                    return redirect('/redirect-form1-first-create_NDA/', permanent=True)
                elif request.POST.get('type_of_request') == "Amendment":
                    return redirect('/redirect-form2-amendment/', permanent=True)
                else:
                    return redirect('/redirect-lock-unlock/', permanent=True)

            elif request.POST.get('type_of_request') == "First Release (Parent and/or Child)":
                form_5_for_lock_unlock_non_NDA = True
                return redirect('/redirect-form2_first_release_option_selector', permanent=True)

            elif request.POST.get('type_of_request') == "First Create (Parent and/or Child)":
                return redirect('/redirect-form1/', permanent=True)

            elif request.POST.get('type_of_request') == "Amendment":
                return redirect('/redirect-form2_amendment_selector', permanent=True)

            elif request.POST.get('type_of_request') == "Lock/Unlock Contract":
                lock_unlock_NDA = False
                return redirect('/redirect-lock-unlock/', permanent=True)

            else:
                return render(request, 'csa_app/coming_soon.html')

    # get taxonomy and pass it to the template
    path_to_taxonomy = os.path.join(settings.BASE_DIR, 'static/json/taxonomy.json')
    taxonomy_json = open(path_to_taxonomy)
    taxonomy_deserialized = json.load(taxonomy_json)
    taxonomy = json.dumps(taxonomy_deserialized)

    return render(request, 'csa_app/home_page.html', {'taxonomy':taxonomy})

global form1_activity
form1_activity = 'Create NDA for single contract (no parent-child relationship)'

def form_1(request):
    global form1_activity
    if request.method == 'POST':
        request_type = request.POST.getlist('request_type', None)[0]
        if request_type == "Create only parent contract":
            response = redirect('/redirect-form1-parent-only/', permanent=True)
            form1_activity = "Create only parent contract"
            return response
        elif request_type == "Create parent and children contracts":
            response = redirect('/redirect-form1-parent-and-children/', permanent=True)
            form1_activity = "Create parent and children contracts"
            return response
        elif request_type == "Add children contracts to existing parent contract":
            response = redirect('/redirect-form1-add-children/', permanent=True)
            form1_activity = "Add children contracts to existing parent contract"
            return response
        else:
             render(request, 'csa_app/base.html')
    return render(request, 'csa_app/base.html')

def form1_parent_only(request):
    parent_contr_record = ParentContractForm()
    if request.method == 'POST':
        parent_contr_record = ParentContractForm(request.POST)
    if parent_contr_record.is_valid():
        parent_contr_record.save(commit=True)
        parent_contr_record_obj = parent_contr_record.save()
        temp = ParentContract.objects.get(id=parent_contr_record_obj.id)
        temp.parent_contract_setup_ref = REC_ID
        temp.save()
        response = redirect('/redirect-dummy_page/', permanent=True)
        return response
    return render(request, 'csa_app/form1_parent_only.html', {'ParentContractForm':ParentContractForm()})

def form1_parent_and_children(request):
    mult_children = formset_factory(ChildContractForm, min_num=1,extra=14, max_num=15)
    parent_contr_record = ParentContractForm()
    if request.method == 'POST':
        parent_contr_record = ParentContractForm(request.POST)
        formset = mult_children(request.POST)
        if parent_contr_record.is_valid() and formset.is_valid():
            #save parent data
            parent_contr_record.save(commit=True)
            parent_contr_record_obj = parent_contr_record.save()
            temp = ParentContract.objects.get(id=parent_contr_record_obj.id)
            temp.parent_contract_setup_ref = REC_ID
            temp.save()
            # save children data
            for form in formset:
                form.save(commit=True)
                obj = form.save()
                temp = ChildContract.objects.get(id=obj.id)
                temp.child_contract_setup_ref = REC_ID
                temp.save()
            response = redirect('/redirect-dummy_page/', permanent=True)
            return response
    return render(request, 'csa_app/form1_parent_and_children.html', {'ParentContractForm':ParentContractForm(), 'mult_children':mult_children})


def form1_add_children(request):
    mult_children = formset_factory(ChildContractForm, min_num=1,extra=14, max_num=15)
    parent_contr_num = ParentContrNumberForm()
    if request.method == 'POST':
        parent_contr_num = ParentContrNumberForm(request.POST)
        formset = mult_children(request.POST)
        if parent_contr_num.is_valid() and formset.is_valid():
            parent_contr_num.save(commit=True)
            parent_contr_num_obj = parent_contr_num.save()
            temp = ParentContract.objects.get(id=parent_contr_num_obj.id)
            temp.parent_contract_setup_ref = REC_ID
            temp.save()
            for form in formset:
                print("got here")
                form.save(commit=True)
                obj = form.save()
                temp = ChildContract.objects.get(id=obj.id)
                temp.child_contract_setup_ref = REC_ID
                temp.save()
            response = redirect('/redirect-dummy_page/', permanent=True)
            return response
    return render(request, 'csa_app/form1_add_children.html',
        {'ParentContrNumberForm':ParentContrNumberForm(), 'mult_children':mult_children})

def dummy_page(request):

    if request.method == 'POST':
        setup = Setup.objects.get(id=int(REC_ID.id))
        parent = ParentContract.objects.get(parent_contract_setup_ref=int(REC_ID.id))
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="CSA request.csv"'

        writer = csv.writer(response)
        writer.writerow(['User Name', 'Contract Type', 'Request Type', 'Paper Contr. Type', 'Category', 'Sub-category'])
        writer.writerow([setup.user_name, setup.contract_type, setup.request_type, setup.paper_contr_type, setup.category, setup.sub_category])
        writer.writerow([" "])
        writer.writerow([form1_activity])
        if form1_activity == "Create only parent contract" or form1_activity == 'Create NDA for single contract (no parent-child relationship)':
            writer.writerow([" "])
            writer.writerow(["Parent Contract"])
            writer.writerow(['Vendor #', 'Vendor Name', 'Contr. Name', 'PGrp', 'POrg'])
            writer.writerow([parent.parent_vendor_number, parent.parent_vendor_name, parent.parent_contr_name, parent.parent_PGrp, parent.parent_POrg])
        elif form1_activity == "Create parent and children contracts":
            children = ChildContract.objects.filter(child_contract_setup_ref=int(REC_ID.id))
            writer.writerow([" "])
            writer.writerow(["Parent Contract"])
            writer.writerow(['Vendor #', 'Vendor Name', 'Contr. Name', 'PGrp', 'POrg'])
            writer.writerow([parent.parent_vendor_number, parent.parent_vendor_name, parent.parent_contr_name, parent.parent_PGrp, parent.parent_POrg])
            writer.writerow([" "])
            writer.writerow(["Children Contracts"])
            for child in children:
                writer.writerow(['Vendor #', 'Vendor Name', 'Contr. Name', 'PGrp', 'POrg'])
                writer.writerow([child.child_vendor_number, child.child_vendor_name, child.child_contr_name, child.child_PGrp, child.child_POrg])
        else:
            children = ChildContract.objects.filter(child_contract_setup_ref=int(REC_ID.id))
            writer.writerow([" "])
            writer.writerow(["Parent Contract Number:", parent.parent_contr_number])
            writer.writerow([" "])
            writer.writerow(["Children Contracts"])
            for child in children:
                writer.writerow(['Vendor #', 'Vendor Name', 'Contr. Name', 'PGrp', 'POrg'])
                writer.writerow([child.child_vendor_number, child.child_vendor_name, child.child_contr_name, child.child_PGrp, child.child_POrg])

        return response

    return render(request, 'csa_app/dummy_page.html')

def form2_amendment(request):
    amend_list = AmendmentType.objects.values_list('amendment_type', flat=True).filter(setup_reference=int(REC_ID.id))
    if len(amend_list)==1:
        if amend_list[0]=='Date Extension':
            amend_items=Form2AmendmentDate()
            if request.method=='POST':
                amend_items=Form2AmendmentDate(request.POST)
                if amend_items.is_valid():
                    amend_items.save(commit=True)
                    amend_items_obj = amend_items.save()
                    temp = Form2.objects.get(id=amend_items_obj.id)
                    temp.form2_setup_ref = REC_ID
                    temp.save()
                    return redirect('/redirect-dummy_page2_amendment_date/', permanent=True)
            return render(request, 'csa_app/form2_amendment_date.html', {'Form2AmendmentDate':Form2AmendmentDate()})
        else:
            amend_items=Form2AmendmentHeader()
            if request.method=='POST':
                amend_items=Form2AmendmentHeader(request.POST)
                if amend_items.is_valid():
                    amend_items.save(commit=True)
                    amend_items_obj = amend_items.save()
                    temp = Form2.objects.get(id=amend_items_obj.id)
                    temp.form2_setup_ref = REC_ID
                    temp.save()
                    return redirect('/redirect-dummy_page2_amendment_header/', permanent=True)
            return render(request, 'csa_app/form2_amendment_header.html', {'Form2AmendmentHeader':Form2AmendmentHeader()})
    else:
        amend_items=Form2Amendment()
        if request.method=='POST':
            amend_items=Form2Amendment(request.POST)
            if amend_items.is_valid():
                amend_items.save(commit=True)
                amend_items_obj = amend_items.save()
                temp = Form2.objects.get(id=amend_items_obj.id)
                temp.form2_setup_ref = REC_ID
                temp.save()
                return redirect('/redirect-dummy_page2_amendment_date_plus_header/', permanent=True)
        return render(request, 'csa_app/form2_amendment_date_plus_header.html', {'Form2Amendment':Form2Amendment()})

def form2_first_release_NDA(request):
    parent_contr_record = Form2FormParent()
    if request.method == 'POST':
        parent_contr_record = Form2FormParent(request.POST)
        print(parent_contr_record.is_valid())
        if parent_contr_record.is_valid():
            parent_contr_record.save(commit=True)
            parent_contr_record_obj = parent_contr_record.save()
            temp = Form2.objects.get(id=parent_contr_record_obj.id)
            temp.form2_target_value = 0.22
            temp.form2_child_or_parent = "parent"
            temp.form2_setup_ref = REC_ID
            temp.save()
            return redirect('/redirect-dummy_page2_first_release_NDA/', permanent=True)
    return render(request, 'csa_app/form_2_first_release_parent_only.html', {'Form2FormParent':Form2FormParent()})

def dummy_page2_first_release_NDA(request):
    if request.method == 'POST':
        setup = Setup.objects.get(id=int(REC_ID.id))
        parentf2 = Form2.objects.get(form2_setup_ref=int(REC_ID.id))
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="CSA request.csv"'

        writer = csv.writer(response)
        writer.writerow(['User Name', 'Contract Type', 'Request Type', 'Paper Contr. Type', 'Category', 'Sub-category'])
        writer.writerow([setup.user_name, setup.contract_type, setup.request_type, setup.paper_contr_type, setup.category, setup.sub_category])
        writer.writerow([" "])
        writer.writerow(["Non-Disclosure Agreement - NDA First Release"])
        writer.writerow([" "])
        writer.writerow(["Parent Contract"])
        writer.writerow([\
        'Contr. #', 'Contr. Name', 'Vendor #', 'Vendor Name', 'Validity Start', 'Validity End', 'PGrp', \
        'POrg', 'Target Value', 'Currency', 'Payment Terms (PT)', 'Reasons for PT outside of 60N if applicable'])
        writer.writerow([parentf2.form2_contr_num, parentf2.form2_contr_name, parentf2.form2_vendor_number, parentf2.form2_vendor_name, \
            parentf2.form2_validity_start, parentf2.form2_validity_end, parentf2.form2_PGrp, parentf2.form2_POrg, parentf2.form2_target_value, \
            parentf2.form2_currency, parentf2.form2_payment_terms, parentf2.form2_reasons_for_outside])

        return response

    return render(request, 'csa_app/dummy_page.html')


def dummy_page2_amendment_date(request):
    if request.method == 'POST':
        setup = Setup.objects.get(id=int(REC_ID.id))
        amend_items = Form2.objects.get(form2_setup_ref=int(REC_ID.id))
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="CSA request.csv"'

        writer = csv.writer(response)
        writer.writerow(['User Name', 'Contract Type', 'Request Type', 'Paper Contr. Type', 'Category', 'Sub-category'])
        writer.writerow([setup.user_name, setup.contract_type, setup.request_type, setup.paper_contr_type, setup.category, setup.sub_category])
        writer.writerow([" "])
        writer.writerow(["Contr. # ","Contr. Validity End Date"])
        writer.writerow([amend_items.form2_contr_num, amend_items.form2_validity_end])

        return response

    return render(request, 'csa_app/dummy_page.html')

def dummy_page2_amendment_header(request):
    if request.method == 'POST':
        setup = Setup.objects.get(id=int(REC_ID.id))
        amend_items = Form2.objects.get(form2_setup_ref=int(REC_ID.id))
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="CSA request.csv"'

        writer = csv.writer(response)
        writer.writerow(['User Name', 'Contract Type', 'Request Type', 'Paper Contr. Type', 'Category', 'Sub-category'])
        writer.writerow([setup.user_name, setup.contract_type, setup.request_type, setup.paper_contr_type, setup.category, setup.sub_category])
        writer.writerow([" "])
        writer.writerow(["Contr # ","Contr. Name","PGrp","New Contr. Owner Email"])
        writer.writerow([amend_items.form2_contr_num, amend_items.form2_contr_name, amend_items.form2_PGrp, amend_items.form2_owner_email])

        return response

    return render(request, 'csa_app/dummy_page.html')


def dummy_page2_amendment_date_plus_header(request):
    if request.method == 'POST':
        setup = Setup.objects.get(id=int(REC_ID.id))
        amend_items = Form2.objects.get(form2_setup_ref=int(REC_ID.id))
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="CSA request.csv"'

        writer = csv.writer(response)
        writer.writerow(['User Name', 'Contract Type', 'Request Type', 'Paper Contr. Type', 'Category', 'Sub-category'])
        writer.writerow([setup.user_name, setup.contract_type, setup.request_type, setup.paper_contr_type, setup.category, setup.sub_category])
        writer.writerow([" "])
        writer.writerow(["Contr # ","Contr. Name","Contr. Validity End Date","PGrp","New Contr. Owner Email"])
        writer.writerow([amend_items.form2_contr_num, amend_items.form2_contr_name, amend_items.form2_validity_end, amend_items.form2_PGrp, amend_items.form2_owner_email])

        return response

    return render(request, 'csa_app/dummy_page.html')

def form2_first_release_option_selector(request):
    global form2_activity
    if request.method == 'POST':
        request_type = request.POST.getlist('request_type', None)[0]
        if request_type == "Release only parent contract":
            response = redirect('/redirect-form2-first-release-parent-only/', permanent=True)
            form2_activity = "Release only parent contract"
            return response
        elif request_type == "Release parent and children contracts":
            response = redirect('/redirect-form2-first-release-parent-and-children/', permanent=True)
            form2_activity = "Release parent and children contracts"
            return response
        elif request_type == "Parent contract exists, release children contracts only":
            response = redirect('/redirect-form2-first-release-add-children/', permanent=True)
            form2_activity = "Parent contract exists, release children contracts only"
            return response
        else:
             render(request, 'csa_app/base_form2_first_release_option_selector.html')
    return render(request, 'csa_app/base_form2_first_release_option_selector.html')


def form2_first_release_parent_only(request):
    parent_contr_record = Form2FormParent()
    if request.method == 'POST':
        parent_contr_record = Form2FormParent(request.POST)
        if parent_contr_record.is_valid():
            parent_contr_record.save(commit=True)
            parent_contr_record_obj = parent_contr_record.save()
            temp = Form2.objects.get(id=parent_contr_record_obj.id)
            temp.form2_target_value = 0.88
            temp.form2_child_or_parent = "parent"
            temp.form2_setup_ref = REC_ID
            temp.save()
            return redirect('/redirect-form5/', permanent=True)
    return render(request, 'csa_app/form_2_first_release_parent_only.html', {'Form2FormParent':Form2FormParent()})


def form5(request):
    Form5_items = Form5Form()
    if request.method == 'POST':
        Form5_items = Form5Form(request.POST)
        if Form5_items.is_valid():
            Form5_items.save(commit=True)
            Form5_items_obj=Form5_items.save()
            temp = Form5.objects.get(id=Form5_items_obj.id)
            temp.form5_setup_ref=REC_ID
            temp.save()
            if form_5_for_lock_unlock_non_NDA:
                return redirect('/redirect-dummy_page2_lock_unlock_NDA', permanent=True)
            else:
                return redirect('/redirect-dummy_page2_forms2_5/', permanent=True)
    return render(request, 'csa_app/form5.html', {'Form5Form':Form5Form()})


def dummy_page2_forms2_5(request):#########################################################################################
    if request.method == 'POST':
        setup = Setup.objects.get(id=int(REC_ID.id))
        form5_record = Form5.objects.filter(form5_setup_ref=int(REC_ID.id)).values('form5_1','form5_2','form5_3','form5_4','form5_5','form5_6','form5_7','form5_8',
                                                                                    'form5_9','form5_10','form5_11','form5_12','form5_13','form5_14','form5_15')[0]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="CSA request.csv"'

        def write_children():
            children_contr_record = Form2.objects.filter(form2_setup_ref=int(REC_ID.id), form2_child_or_parent='child').values()
            writer.writerow([" "])
            writer.writerow(["Children Contracts - First Release Header Details"])
            writer.writerow(["Contr # ","Contr. Name","Vendor#","Vendor Name", "POrg", "PGrp", "Currency", "Payment Terms","Reason for Payment Terms outside 60N (if applicable)",
                            "Overall SRM contract target value ($)", "Validity Start day", "Validity End day", "Inco-Term"])
            for child in children_contr_record:
                writer.writerow([child['form2_contr_num'], child['form2_contr_name'], child['form2_vendor_number'],
                                child['form2_vendor_name'], child['form2_POrg'], child['form2_PGrp'], child['form2_currency'],
                                child['form2_payment_terms'], child['form2_reasons_for_outside'], child['form2_target_value'],
                                child['form2_validity_start'], child['form2_validity_end'], child['form2_incoterm']])

        writer = csv.writer(response)
        writer.writerow(['User Name', 'Contract Type', 'Request Type', 'Paper Contr. Type', 'Category', 'Sub-category'])
        writer.writerow([setup.user_name, setup.contract_type, setup.request_type, setup.paper_contr_type, setup.category, setup.sub_category])
        writer.writerow([" "])

        if form2_activity == "Release only parent contract" or form2_activity == "Release parent and children contracts":
            parent_contr_record = Form2.objects.get(form2_setup_ref=int(REC_ID.id), form2_child_or_parent='parent')
            writer.writerow(["Parent Contract - First Release Header Details"])
            writer.writerow(["Contr # ","Contr. Name","Vendor#","Vendor Name", "POrg", "PGrp", "Currency", "Payment Terms","Reason for Payment Terms outside 60N (if applicable)",
                            "Validity Start day", "Validity End day"])
            writer.writerow([parent_contr_record.form2_contr_num, parent_contr_record.form2_contr_name, parent_contr_record.form2_vendor_number,
                            parent_contr_record.form2_vendor_name, parent_contr_record.form2_POrg, parent_contr_record.form2_PGrp, parent_contr_record.form2_currency,
                            parent_contr_record.form2_payment_terms, parent_contr_record.form2_reasons_for_outside,parent_contr_record.form2_validity_start,
                            parent_contr_record.form2_validity_end])
            if form2_activity == "Release parent and children contracts":
                write_children()
        else:
            parent_contr_num = ParentContract.objects.get(parent_contract_setup_ref=int(REC_ID.id))
            writer.writerow(["Parent Contract # - First Release Header Details"])
            writer.writerow([parent_contr_num.parent_vendor_number])
            writer.writerow([])
            write_children()
        #iterate through form5 queryset. If value=True, return and write value description from the dictionary saved in list_objects.py
        writer.writerow([" "])
        writer.writerow(["Lease Questionnaire"])
        for k,v in form5_record.items():
            if v:
                writer.writerow([form5_items_dict[k]])

        return response

    return render(request, 'csa_app/dummy_page.html')


def form2_first_release_parent_and_children(request):
    parent_contr_record = Form2FormParent()
    mult_children = formset_factory(Form2ChildFirstReleaseForm, min_num=1,extra=14, max_num=15)
    if request.method == 'POST':
        parent_contr_record = Form2FormParent(request.POST)
        formset = mult_children(request.POST)
        if parent_contr_record.is_valid() and formset.is_valid():
            parent_contr_record.save(commit=True)
            parent_contr_record_obj = parent_contr_record.save()
            temp = Form2.objects.get(id=parent_contr_record_obj.id)
            temp.form2_setup_ref = REC_ID
            temp.form2_child_or_parent = 'parent'
            temp.save()
            for form in formset:
                form.save(commit=True)
                obj = form.save()
                temp = Form2.objects.get(id=obj.id)
                temp.form2_setup_ref = REC_ID
                temp.form2_child_or_parent = 'child'
                temp.save()
            response = redirect('/redirect-form5/', permanent=True)
            return response
    return render(request, 'csa_app/form2_first_release_parent_and_children.html', {'Form2FormParent':Form2FormParent(),
        'mult_children':mult_children})


def form2_first_release_add_children(request):
    parent_contr_num = ParentContrNumberFormFirstRelease()
    mult_children = formset_factory(Form2ChildFirstReleaseForm, min_num=1,extra=14, max_num=15)
    if request.method == 'POST':
        print('pass POST')
        parent_contr_num = ParentContrNumberFormFirstRelease(request.POST)
        formset = mult_children(request.POST)
        print('parent valid: ', parent_contr_num.is_valid())
        print('child valid :', formset.is_valid())
        if parent_contr_num.is_valid() and formset.is_valid():
            print('forms valid')
            parent_contr_num.save(commit=True)
            parent_contr_num_obj = parent_contr_num.save()
            temp = ParentContract.objects.get(id=parent_contr_num_obj.id)
            temp.parent_contract_setup_ref = REC_ID
            temp.save()
            for form in formset:
                form.save(commit=True)
                obj = form.save()
                temp = Form2.objects.get(id=obj.id)
                temp.form2_setup_ref = REC_ID
                temp.form2_child_or_parent = 'child'
                temp.save()
            response = redirect('/redirect-form5/', permanent=True)
            return response
    return render(request, 'csa_app/form2_first_release_add_children.html', {'ParentContrNumberForm':ParentContrNumberFormFirstRelease(),
        'mult_children':mult_children})

form2_amendment_items_redirect_links = {
    'Target value':'/redirect-form2_nonNDA_amendment_target_value_selector/',
    'Items update':'/redirect-form2_nonNDA_amendment_items_update/',
    'Date Extension':'/redirect-form2_nonNDA_amendment_date_extension/',
    'Header Information':'/redirect-form2_nonNDA_amendment_header_details',
    'Payment terms':'/redirect-form2_nonNDA_amendment_payment_terms'
    }

amendments_to_print = {}
counter = 0

def form2_amendment_selector(request):
    global amend_list
    amend_list = AmendmentType.objects.values_list('amendment_type', flat=True).filter(setup_reference=int(REC_ID.id))
    global counter
    if counter <= len(amend_list)-1:
        current_item = amend_list[counter]  # get next item in amend list
        redirect_url = form2_amendment_items_redirect_links[current_item] # get redirect url for current item
        counter += 1
        return redirect (redirect_url, permanent=True)
    else:
        return redirect('/redirect-dummy_page2_form2_amendments/',permanent=True)
    return redirect('/redirect-dummy_page2_form2_amendments/',permanent=True)

def form2_nonNDA_amendment_target_value_selector(request):
    if request.method == 'POST':
        if request.POST.get("optradio")=="option1":
            return redirect('/redirect-form2_nonNDA_amendment_target_value_opt1/', permanent=True)
        else:
            return redirect('/redirect-form2_nonNDA_amendment_target_value_opt2/', permanent=True)
    return render(request, 'csa_app/form2_nonNDA_amendment_target_value_selector.html')


def form2_nonNDA_amendment_target_value_opt1(request):
    ParentContrNumber = ParentContrNumberForm()
    mult_children = formset_factory(Form2AmendTargetValueOption1Form, min_num=1,extra=14, max_num=15)
    if request.method == 'POST':
        parent_contr_num = ParentContrNumberForm(request.POST)
        formset = mult_children(request.POST)
        if parent_contr_num.is_valid() and formset.is_valid():
            parent_contr_num.save(commit=True)
            parent_contr_num_obj = parent_contr_num.save()
            temp = ParentContract.objects.get(id=parent_contr_num_obj.id)
            temp.parent_contract_setup_ref = REC_ID
            temp.save()
            for form in formset:
                form.save(commit=True)
                obj = form.save()
                temp = Form2.objects.get(id=obj.id)
                temp.form2_setup_ref = REC_ID
                temp.form2_parent_field_ref = parent_contr_num_obj.id
                temp.save()

            parent = ParentContract.objects.get(parent_contract_setup_ref=int(REC_ID.id), id=int(parent_contr_num_obj.id))
            children = Form2.objects.filter(form2_setup_ref=int(REC_ID.id), form2_parent_field_ref = int(parent_contr_num_obj.id)).values()
            out = []
            for i in children:
                out.append([i['form2_contr_num'],i['form2_POrg'],i['form2_payment_terms'],i['form2_plant_location'],i['form2_target_value']])
            amendments_to_print.update(
            {'Target value':
                {'header':["Amendment Header Details - Add 'NEW' Target Values for specific Porg's/Plant locations/Payment terms"],
                'br1':[" "],
                'parent_contr_num_header_and_value':['Parent Contr#', parent.parent_contr_number],
                'br2':[" "],
                'children_details':['Children contracts'],
                'db_fields_headers':['Contr Number','POrg','Payment Terms','Plant Location (if applicable)', 'Target Value'],
                'db_fileds_values':out,
                }
              }
            )
            return redirect('/redirect-form2_amendment_selector', permanent=True)
    return render(request, 'csa_app/form2_nonNDA_amendment_target_value_opt1.html', {'ParentContrNumberForm':ParentContrNumberForm(),'mult_children':mult_children})

def form2_nonNDA_amendment_target_value_opt2(request):
    ParentContrNumber = ParentContrNumberFormFirstRelease()
    mult_children = formset_factory(Form2AmendTargetValueOption2Form, min_num=1,extra=14, max_num=15)

    if request.method == 'POST':
        parent_contr_num = ParentContrNumberFormFirstRelease(request.POST)
        formset = mult_children(request.POST)
        if parent_contr_num.is_valid() and formset.is_valid():
            parent_contr_num.save(commit=True)
            parent_contr_num_obj = parent_contr_num.save()
            temp = ParentContract.objects.get(id=parent_contr_num_obj.id)
            temp.parent_contract_setup_ref = REC_ID
            temp.save()
            for form in formset:
                form.save(commit=True)
                obj = form.save()
                temp = Form2.objects.get(id=obj.id)
                temp.form2_setup_ref = REC_ID
                temp.form2_parent_field_ref = parent_contr_num_obj.id
                temp.save()

        parent = ParentContract.objects.get(parent_contract_setup_ref=int(REC_ID.id), id=int(parent_contr_num_obj.id))
        children = Form2.objects.filter(form2_setup_ref=int(REC_ID.id), form2_parent_field_ref = int(parent_contr_num_obj.id)).values()
        out = []
        for i in children:
            out.append([i['form2_contr_num'],i['form2_target_value']])
        amendments_to_print.update(
        {'Target value':
            {'header':["Amendment Header Details - Add 'NEW' Target Values for specific Porg's/Plant locations/Payment terms"],
            'br1':[" "],
            'parent_contr_num_header_and_value':['Parent Contr#', parent.parent_contr_number],
            'br2':[" "],
            'children_details':['Children contracts'],
            'db_fields_headers':['Contr Number','Target Value'],
            'db_fileds_values':out,
            }
          }
        )
        return redirect('/redirect-form2_amendment_selector', permanent=True)
    return render(request, 'csa_app/form2_nonNDA_amendment_target_value_opt2.html', {'ParentContrNumberForm':ParentContrNumberFormFirstRelease(),'mult_children':mult_children})

def form2_nonNDA_amendment_items_update(request):
    return render(request, 'csa_app/coming_soon.html')

def coming_soon(request):
    return render(request, 'csa_app/coming_soon.html')

def clear_variables():
    global counter
    counter = 0
    amendments_to_print.clear()

def dummy_page2_form2_amendments(request):
    if request.method == 'POST':
        setup = Setup.objects.get(id=int(REC_ID.id))
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="CSA request.csv"'

        writer = csv.writer(response)
        writer.writerow(['User Name', 'Contract Type', 'Request Type', 'Paper Contr. Type', 'Category', 'Sub-category'])
        writer.writerow([setup.user_name, setup.contract_type, setup.request_type, setup.paper_contr_type, setup.category, setup.sub_category])
        writer.writerow([" "])

        for item in amend_list:
            for k_atp, v_atp in amendments_to_print.items():
                if item == k_atp:
                    for k,v in amendments_to_print[k_atp].items():
                        if k=='db_fileds_values':
                            print('got here')
                            print('v :', v)
                            for vi in v:
                                writer.writerow(vi)
                        else:
                            writer.writerow(v)
            writer.writerow([" "])
        clear_variables()
        return response

    return render(request, 'csa_app/dummy_page.html')

def form2_nonNDA_amendment_date_extension_selector(request):
    if request.method == 'POST':
        if request.POST.get("optradio")=="option1":
            return redirect('/redirect-form2_nonNDA_amendment_date_extension_opt1/', permanent=True)
        else:
            return redirect('/redirect-form2_nonNDA_amendment_date_extension_opt2/', permanent=True)
    return render(request, 'csa_app/form2_nonNDA_amendment_date_extension_selector.html')

def form2_nonNDA_amendment_date_extension_opt1(request):
    parent_rec = Form2AmendDateExtensionOption1Form()
    mult_children = formset_factory(Form2AmendDateExtensionOption1Form, min_num=1,extra=14, max_num=15)
    if request.method == 'POST':
        parent_rec = Form2AmendDateExtensionOption1Form(request.POST)
        formset = mult_children(request.POST)
        if parent_rec.is_valid() and formset.is_valid():
            parent_rec.save(commit=True)
            parent_obj = parent_rec.save()
            temp = Form2.objects.get(id=parent_obj.id)
            temp.form2_setup_ref = REC_ID
            temp.form2_child_or_parent = 'parent'
            temp.save()
            for form in formset:
                form.save(commit=True)
                obj = form.save()
                temp = Form2.objects.get(id=obj.id)
                temp.form2_setup_ref = REC_ID
                temp.form2_child_or_parent = 'child'
                temp.form2_parent_field_ref = parent_obj.id
                temp.save()

            parent = Form2.objects.get(form2_setup_ref=int(REC_ID.id), form2_child_or_parent = 'parent', id=int(parent_obj.id))
            children = Form2.objects.filter(form2_setup_ref=int(REC_ID.id), form2_child_or_parent = 'child', form2_parent_field_ref = int(parent_obj.id)).values()
            out = []
            for i in children:
                out.append([i['form2_contr_num'],i['form2_validity_end']])
            amendments_to_print.update(
            {'Date Extension':
                {'header':["Amendment Header Details - Contract Validity Date Extension (parent and children)"],
                'br1':[" "],
                'parent_details':['Parent Contract'],
                'parent_db_headers':['Contr Number', 'Validity End Date'],
                'parent_contr_num_header_and_value':[parent.form2_contr_num, parent.form2_validity_end],
                'br2':[" "],
                'children_details':['Children contracts'],
                'db_fields_headers':['Contr Number','Validity End'],
                'db_fileds_values':out,
                }
              }
            )
            return redirect('/redirect-form2_amendment_selector', permanent=True)
    return render(request, 'csa_app/form2_nonNDA_amendment_date_extension_opt1.html', {'ParentContr':Form2AmendDateExtensionOption1Form(),'mult_children':mult_children})

def form2_nonNDA_amendment_date_extension_opt2(request):
    parent_rec = Form2AmendHeaderDetailsOption2FormParent()
    mult_children = formset_factory(Form2AmendDateExtensionOption1Form, min_num=1,extra=14, max_num=15)
    if request.method == 'POST':
        parent_rec = Form2AmendHeaderDetailsOption2FormParent(request.POST)
        formset = mult_children(request.POST)
        if parent_rec.is_valid() and formset.is_valid():
            parent_rec.save(commit=True)
            parent_obj = parent_rec.save()
            temp = Form2.objects.get(id=parent_obj.id)
            temp.form2_setup_ref = REC_ID
            temp.form2_child_or_parent = 'parent'
            temp.save()
            for form in formset:
                form.save(commit=True)
                obj = form.save()
                temp = Form2.objects.get(id=obj.id)
                temp.form2_setup_ref = REC_ID
                temp.form2_child_or_parent = 'child'
                temp.form2_parent_field_ref = parent_obj.id
                temp.save()

            parent = Form2.objects.get(form2_setup_ref=int(REC_ID.id), form2_child_or_parent = 'parent', id=int(parent_obj.id))
            children = Form2.objects.filter(form2_setup_ref=int(REC_ID.id), form2_child_or_parent = 'child', form2_parent_field_ref = int(parent_obj.id)).values()
            out = []
            for i in children:
                out.append([i['form2_contr_num'],i['form2_validity_end']])
            amendments_to_print.update(
            {'Date Extension':
                {'header':["Amendment Header Details - Contract Validity Date Extension (children only)"],
                'br1':[" "],
                'parent_contr_num_header_and_value':['Parent Contr#', parent.form2_contr_num],
                'br2':[" "],
                'children_details':['Children contracts'],
                'db_fields_headers':['Contr Number','Validity End'],
                'db_fileds_values':out,
                }
              }
            )
            return redirect('/redirect-form2_amendment_selector', permanent=True)
    return render(request, 'csa_app/form2_nonNDA_amendment_date_extension_opt2.html', {'ParentContr':Form2AmendHeaderDetailsOption2FormParent(),'mult_children':mult_children})

def form2_nonNDA_amendment_header_details_selector(request):
    if request.method == 'POST':
        if request.POST.get("optradio")=="option1":
            return redirect('/redirect-form2_nonNDA_amendment_header_details_opt1/', permanent=True)
        else:
            return redirect('/redirect-form2_nonNDA_amendment_header_details_opt2/', permanent=True)
    return render(request, 'csa_app/form2_nonNDA_amendment_date_extension_selector.html')

def form2_nonNDA_amendment_header_details_opt1(request):
    parent_rec = Form2AmendHeaderDetailsOption1FormParent()
    mult_children = formset_factory(Form2AmendHeaderDetailsOption1FormChild, min_num=1,extra=14, max_num=15)
    if request.method == 'POST':
        parent_rec = Form2AmendHeaderDetailsOption1FormParent(request.POST)
        formset = mult_children(request.POST)
        if parent_rec.is_valid() and formset.is_valid():
            parent_rec.save(commit=True)
            parent_obj = parent_rec.save()
            temp = Form2.objects.get(id=parent_obj.id)
            temp.form2_setup_ref = REC_ID
            temp.form2_child_or_parent = 'parent'
            temp.save()
            for form in formset:
                form.save(commit=True)
                obj = form.save()
                temp = Form2.objects.get(id=obj.id)
                temp.form2_setup_ref = REC_ID
                temp.form2_child_or_parent = 'child'
                temp.form2_parent_field_ref = parent_obj.id
                temp.save()

            parent = Form2.objects.get(form2_setup_ref=int(REC_ID.id), form2_child_or_parent = 'parent', id=int(parent_obj.id))
            children = Form2.objects.filter(form2_setup_ref=int(REC_ID.id), form2_child_or_parent = 'child', form2_parent_field_ref = int(parent_obj.id)).values()
            out = []
            for i in children:
                out.append([i['form2_contr_num'],i['form2_contr_name'],i['form2_PGrp'],i['form2_incoterm'],i['form2_owner_email']])
            amendments_to_print.update(
            {'Header Information':
                {'header':["Amendment Header Details"],
                'br1':[" "],
                'parent_details':['Parent Contract'],
                'parent_db_headers':['Contr Number', 'Contr Name', 'PGrp', 'New Contr Owner Email'],
                'parent_contr_num_header_and_value':[parent.form2_contr_num,parent.form2_contr_name,parent.form2_PGrp,parent.form2_owner_email],
                'br2':[" "],
                'children_details':['Children contracts'],
                'db_fields_headers':['Contr Number', 'Contr Name', 'PGrp', 'Inco-Term', 'New Contr Owner Email'],
                'db_fileds_values':out,
                }
              }
            )
            return redirect('/redirect-form2_amendment_selector', permanent=True)
    return render(request, 'csa_app/form2_nonNDA_amendment_header_details_opt1.html', {'ParentContr':Form2AmendHeaderDetailsOption1FormParent(),'mult_children':mult_children})

def form2_nonNDA_amendment_header_details_opt2(request):
    parent_rec = Form2AmendHeaderDetailsOption2FormParent()
    mult_children = formset_factory(Form2AmendHeaderDetailsOption1FormChild, min_num=1,extra=14, max_num=15)
    if request.method == 'POST':
        parent_rec = Form2AmendHeaderDetailsOption2FormParent(request.POST)
        formset = mult_children(request.POST)
        if parent_rec.is_valid() and formset.is_valid():
            parent_rec.save(commit=True)
            parent_obj = parent_rec.save()
            temp = Form2.objects.get(id=parent_obj.id)
            temp.form2_setup_ref = REC_ID
            temp.form2_child_or_parent = 'parent'
            temp.save()
            for form in formset:
                form.save(commit=True)
                obj = form.save()
                temp = Form2.objects.get(id=obj.id)
                temp.form2_setup_ref = REC_ID
                temp.form2_child_or_parent = 'child'
                temp.form2_parent_field_ref = parent_obj.id
                temp.save()

            parent = Form2.objects.get(form2_setup_ref=int(REC_ID.id),form2_child_or_parent='parent',id=int(parent_obj.id))
            children = Form2.objects.filter(form2_setup_ref=int(REC_ID.id),form2_child_or_parent = 'child', form2_parent_field_ref = int(parent_obj.id)).values()
            out = []
            for i in children:
                out.append([i['form2_contr_num'],i['form2_contr_name'],i['form2_PGrp'],i['form2_incoterm'],i['form2_owner_email']])
            amendments_to_print.update(
            {'Header Information':
                {'header':["Amendment Header Details"],
                'br1':[" "],
                'parent_contr_num_header_and_value':['Parent Contr#', parent.form2_contr_num],
                'br2':[" "],
                'children_details':['Children contracts'],
                'db_fields_headers':['Contr Number', 'Contr Name', 'PGrp', 'Inco-Term', 'New Contr Owner Email'],
                'db_fileds_values':out,
                }
              }
            )
            return redirect('/redirect-form2_amendment_selector', permanent=True)
    return render(request, 'csa_app/form2_nonNDA_amendment_header_details_opt2.html', {'ParentContr':Form2AmendHeaderDetailsOption2FormParent(),'mult_children':mult_children})

def form2_nonNDA_amendment_payment_terms_selector(request):
    if request.method == 'POST':
        if request.POST.get("optradio")=="option1":
            return redirect('/redirect-form2_nonNDA_amendment_payment_terms_opt1/', permanent=True)
        else:
            return redirect('/redirect-form2_nonNDA_amendment_payment_terms_opt2/', permanent=True)
    return render(request, 'csa_app/form2_nonNDA_amendment_date_extension_selector.html')

def form2_nonNDA_amendment_payment_terms_opt1(request):
    parent_rec = Form2AmendPaymentTermsFormOpt1()
    mult_children = formset_factory(Form2AmendPaymentTermsFormOpt1, min_num=1,extra=14, max_num=15)
    if request.method == 'POST':
        parent_rec = Form2AmendPaymentTermsFormOpt1(request.POST)
        formset = mult_children(request.POST)
        if parent_rec.is_valid() and formset.is_valid():
            parent_rec.save(commit=True)
            parent_obj = parent_rec.save()
            temp = Form2.objects.get(id=parent_obj.id)
            temp.form2_setup_ref = REC_ID
            temp.form2_child_or_parent = 'parent'
            temp.save()
            for form in formset:
                form.save(commit=True)
                obj = form.save()
                temp = Form2.objects.get(id=obj.id)
                temp.form2_setup_ref = REC_ID
                temp.form2_child_or_parent = 'child'
                temp.form2_parent_field_ref = parent_obj.id
                temp.save()

            parent = Form2.objects.get(form2_setup_ref=int(REC_ID.id), form2_child_or_parent = 'parent', id=int(parent_obj.id))
            children = Form2.objects.filter(form2_setup_ref=int(REC_ID.id), form2_child_or_parent = 'child', form2_parent_field_ref = int(parent_obj.id)).values()
            out = []
            for i in children:
                out.append([i['form2_contr_num'],i['form2_payment_terms']])
            amendments_to_print.update(
            {'Payment terms':
                {'header':["Amendment Header Details"],
                'br1':[" "],
                'parent_details':['Parent Contract'],
                'parent_db_headers':['Contr Number', 'Payment Terms'],
                'parent_contr_num_header_and_value':[parent.form2_contr_num, parent.form2_payment_terms],
                'br2':[" "],
                'children_details':['Children contracts'],
                'db_fields_headers':['Contr Number', 'Payment Terms'],
                'db_fileds_values':out,
                }
              }
            )
            return redirect('/redirect-form2_amendment_selector', permanent=True)
    return render(request, 'csa_app/form2_nonNDA_amendment_payment_terms_opt1.html', {'ParentContr':Form2AmendPaymentTermsFormOpt1(),'mult_children':mult_children})

def form2_nonNDA_amendment_payment_terms_opt2(request):
    parent_rec = Form2AmendHeaderDetailsOption2FormParent()
    mult_children = formset_factory(Form2AmendPaymentTermsFormOpt1, min_num=1,extra=14, max_num=15)
    if request.method == 'POST':
        parent_rec = Form2AmendHeaderDetailsOption2FormParent(request.POST)
        formset = mult_children(request.POST)
        if parent_rec.is_valid() and formset.is_valid():
            parent_rec.save(commit=True)
            parent_obj = parent_rec.save()
            temp = Form2.objects.get(id=parent_obj.id)
            temp.form2_setup_ref = REC_ID
            temp.form2_child_or_parent = 'parent'
            temp.save()
            for form in formset:
                form.save(commit=True)
                obj = form.save()
                temp = Form2.objects.get(id=obj.id)
                temp.form2_setup_ref = REC_ID
                temp.form2_child_or_parent = 'child'
                temp.form2_parent_field_ref = parent_obj.id
                temp.save()

            parent = Form2.objects.get(form2_setup_ref=int(REC_ID.id), form2_child_or_parent = 'parent', id=int(parent_obj.id))
            children = Form2.objects.filter(form2_setup_ref=int(REC_ID.id),form2_child_or_parent = 'child', form2_parent_field_ref = int(parent_obj.id)).values()
            out = []
            for i in children:
                out.append([i['form2_contr_num'],i['form2_payment_terms']])
            amendments_to_print.update(
            {'Payment terms':
                {'header':["Amendment Header Details"],
                'br1':[" "],
                'parent_contr_num_header_and_value':['Parent Contr#', parent.form2_contr_num],
                'br2':[" "],
                'children_details':['Children contracts'],
                'db_fields_headers':['Contr Number', 'Payment Terms'],
                'db_fileds_values':out,
                }
              }
            )
            return redirect('/redirect-form2_amendment_selector', permanent=True)
    return render(request, 'csa_app/form2_nonNDA_amendment_payment_terms_opt2.html', {'ParentContr':Form2AmendHeaderDetailsOption2FormParent(),'mult_children':mult_children})

def lock_unlock(request):
    parent_rec = UnlockForm()
    mult_children = formset_factory(UnlockForm, min_num=1,extra=14, max_num=15)
    if request.method == 'POST':
        parent_rec = UnlockForm(request.POST)
        formset = mult_children(request.POST)
        if parent_rec.is_valid() and formset.is_valid():
            parent_rec.save(commit=True)
            parent_obj = parent_rec.save()
            temp = Form2.objects.get(id=parent_obj.id)
            temp.form2_setup_ref = REC_ID
            temp.form2_child_or_parent = 'parent'
            temp.save()
            for form in formset:
                form.save(commit=True)
                obj = form.save()
                temp = Form2.objects.get(id=obj.id)
                temp.form2_setup_ref = REC_ID
                temp.form2_child_or_parent = 'child'
                temp.save()
            if lock_unlock_NDA:
                return redirect('/redirect-dummy_page2_lock_unlock_NDA', permanent=True)
            else:
                global form_5_for_lock_unlock_non_NDA
                form_5_for_lock_unlock_non_NDA = True
                return redirect('/redirect-form5/', permanent=True)
    return render(request, 'csa_app/lock_unlock.html', {'ParentContr':UnlockForm(),'mult_children':mult_children})

def dummy_page2_lock_unlock_NDA(request):
    if request.method == 'POST':
        setup = Setup.objects.get(id=int(REC_ID.id))
        parent = Form2.objects.get(form2_setup_ref=int(REC_ID.id), form2_child_or_parent='parent')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="CSA request.csv"'

        def write_children():
            children_contr_record = Form2.objects.filter(form2_setup_ref=int(REC_ID.id), form2_child_or_parent='child').values()
            writer.writerow([" "])
            writer.writerow(["Children Contracts"])
            writer.writerow(["Contr # ","Lock/Unlock"])
            for child in children_contr_record:
                writer.writerow([child['form2_contr_num'], child['form2_lock_unlock']])

        writer = csv.writer(response)
        writer.writerow(['User Name', 'Contract Type', 'Request Type', 'Paper Contr. Type', 'Category', 'Sub-category'])
        writer.writerow([setup.user_name, setup.contract_type, setup.request_type, setup.paper_contr_type, setup.category, setup.sub_category])
        writer.writerow([" "])
        if parent.form2_contr_num is not None:
            writer.writerow(["Parent Contract"])
            writer.writerow(["Contr # ","Lock/Unlock"])
            writer.writerow([parent.form2_contr_num, parent.form2_lock_unlock])
            writer.writerow([" "])
            write_children()
        else:
            write_children()

        if form_5_for_lock_unlock_non_NDA and not lock_unlock_NDA:
            form5_record = Form5.objects.filter(
                form5_setup_ref=int(REC_ID.id)).values(
                'form5_1','form5_2','form5_3','form5_4',
                'form5_5','form5_6','form5_7','form5_8',
                'form5_9','form5_10','form5_11','form5_12',
                'form5_13','form5_14','form5_15')[0]
            writer.writerow([" "])
            writer.writerow(["Lease Questionnaire"])
            for k,v in form5_record.items():
                if v:
                    writer.writerow([form5_items_dict[k]])

        return response

    return render(request, 'csa_app/dummy_page.html')
