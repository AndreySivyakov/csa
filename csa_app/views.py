from django.shortcuts import render, redirect
from .forms import *
from .models import *
from datetime import date as today_date
from django.forms.formsets import formset_factory
import csv
from django.http import HttpResponse
from django.contrib import messages



# Create your views here.
def home_page(request):
    if request.method == 'POST':
        if request.POST.get('submission_check') == 'yes':

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

            if request.POST.get('type_of_request') == "First Create (Parent and/or Child)" or \
            (request.POST.get('type_of_request') == "First Create (Parent and/or Child)" or \
            (request.POST.get('type_of_request') == "Lock/Unlock Contract" and \
            request.POST.get('contract_type') == "Non-Disclosure Agreement")):

                response = redirect('/redirect-form1/', permanent=True)
                return response

            elif request.POST.get('contract_type') == "Non-Disclosure Agreement":
                if request.POST.get('type_of_request') == "First Release (Parent and/or Child)":
                    return redirect('/redirect-form2-first-release/', permanent=True)
                elif request.POST.get('type_of_request') == "Amendment":
                    return redirect('/redirect-form2-amendment/', permanent=True)

            elif request.POST.get('type_of_request') == "First Release (Parent and/or Child)":
                #response = redirect('/redirect-forms_2_5/', permanent=True)
                #return response
                return render(request, 'csa_app/coming_soon.html')

            else:
                return render(request, 'csa_app/coming_soon.html')

    return render(request, 'csa_app/home_page.html')



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
        #return render(request, 'csa_app/dummy_page.html')
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
            #return render(request, 'csa_app/dummy_page.html')
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
            #return render(request, 'csa_app/dummy_page.html')
    return render(request, 'csa_app/form1_add_children.html',
        {'ParentContrNumberForm':ParentContrNumberForm(), 'mult_children':mult_children})

def dummy_page(request):

    if request.method == 'POST':
        setup = Setup.objects.get(id=int(REC_ID.id))
        parent = ParentContract.objects.get(parent_contract_setup_ref=int(REC_ID.id))
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        writer = csv.writer(response)
        writer.writerow(['User Name', 'Contract Type', 'Request Type', 'Paper Contr. Type', 'Category', 'Sub-category'])
        writer.writerow([setup.user_name, setup.contract_type, setup.request_type, setup.paper_contr_type, setup.category, setup.sub_category])
        writer.writerow([" "])
        writer.writerow([form1_activity])
        if form1_activity == "Create only parent contract":
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

def forms_2_5(request):
    #form2()
    #form5()
    return render(request, 'csa_app/coming_soon.html')

def forms_1_5(request):
    #form2()
    #form5()
    return render(request, 'csa_app/coming_soon.html')

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

def form2_first_release(request):
    parent_contr_record = Form2FormParent()
    if request.method == 'POST':
        parent_contr_record = Form2FormParent(request.POST)
        print(parent_contr_record.is_valid())
        if parent_contr_record.is_valid():
            print('got here')
            parent_contr_record.save(commit=True)
            parent_contr_record_obj = parent_contr_record.save()
            temp = Form2.objects.get(id=parent_contr_record_obj.id)
            temp.form2_target_value = 0.22
            temp.form2_child_or_parent = "parent"
            temp.form2_setup_ref = REC_ID
            temp.save()
            return redirect('/redirect-dummy_page2_first_release/', permanent=True)
    return render(request, 'csa_app/form_2_first_release.html', {'Form2FormParent':Form2FormParent()})

def dummy_page2_first_release(request):
    if request.method == 'POST':
        setup = Setup.objects.get(id=int(REC_ID.id))
        parentf2 = Form2.objects.get(form2_setup_ref=int(REC_ID.id))
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        writer = csv.writer(response)
        writer.writerow(['User Name', 'Contract Type', 'Request Type', 'Paper Contr. Type', 'Category', 'Sub-category'])
        writer.writerow([setup.user_name, setup.contract_type, setup.request_type, setup.paper_contr_type, setup.category, setup.sub_category])
        writer.writerow([" "])
        writer.writerow(["Non-Disclosure Agreement - First Release"])
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
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

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
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

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
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        writer = csv.writer(response)
        writer.writerow(['User Name', 'Contract Type', 'Request Type', 'Paper Contr. Type', 'Category', 'Sub-category'])
        writer.writerow([setup.user_name, setup.contract_type, setup.request_type, setup.paper_contr_type, setup.category, setup.sub_category])
        writer.writerow([" "])
        writer.writerow(["Contr # ","Contr. Name","Contr. Validity End Date","PGrp","New Contr. Owner Email"])
        writer.writerow([amend_items.form2_contr_num, amend_items.form2_contr_name, amend_items.form2_validity_end, amend_items.form2_PGrp, amend_items.form2_owner_email])

        return response

    return render(request, 'csa_app/dummy_page.html')
