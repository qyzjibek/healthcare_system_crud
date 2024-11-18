from django.shortcuts import render, get_object_or_404, redirect
from .models import Country, Users, Discover, Disease, Record, PublicServant

def home(request):
    return render(request, 'home.html')

def country_list(request):
    countries = Country.objects.all()
    return render(request, 'countries/country_list.html', {'countries': countries})

def country_create(request):
    if request.method == 'POST':
        cname = request.POST['cname']
        population = request.POST['population']
        Country.objects.create(cname=cname, population=population)
        return redirect('country_list')
    return render(request, 'countries/country_form.html')

def country_update(request, cname):
    country = get_object_or_404(Country, cname=cname)
    if request.method == 'POST':
        country.population = request.POST['population']
        country.save()
        return redirect('country_list')
    return render(request, 'countries/country_form.html', {'country': country})

def country_delete(request, cname):
    country = get_object_or_404(Country, cname=cname)
    country.delete()
    return redirect('country_list')


def user_list(request):
    users = Users.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

def user_form(request, user_id=None):
    if user_id:
        user = get_object_or_404(Users, email=user_id)  # Query by email (primary key)
    else:
        user = None

    countries = Country.objects.all()  # All countries for the dropdown

    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        surname = request.POST['surname']
        salary = request.POST['salary']
        phone = request.POST['phone']
        country_name = request.POST['cname']  # The country selected in the form

        try:
            country = Country.objects.get(cname=country_name)
        except Country.DoesNotExist:
            country = None
            # Handle the case where the country does not exist (e.g., show an error)

        if user:
            # Update existing user
            user.email = email
            user.name = name
            user.surname = surname
            user.salary = salary
            user.phone = phone
            user.cname_id = country
            user.save()
        else:
            # Create new user
            Users.objects.create(
                email=email,
                name=name,
                surname=surname,
                salary=salary,
                phone=phone,
                cname_id=country
            )

        return redirect('user_list')  # Redirect to user_list after form submission

    return render(request, 'users/user_form.html', {'user': user, 'countries': countries})


def user_delete(request, user_id):
    user = get_object_or_404(Users, email=user_id)  # Query by email (primary key)
    user.delete()
    return redirect('user_list')  # Redirect to user list after deletion

def discover_list(request):
    discoveries = Discover.objects.select_related('cname', 'disease_code').all()
    return render(request, 'discover_list.html', {'discoveries': discoveries})

def discover_delete(request, cname, disease_code):
    discover = get_object_or_404(Discover, cname__cname=cname, disease_code__disease_code=disease_code)
    discover.delete()
    return redirect('discover_list')

def discover_form(request, cname=None, disease_code=None):
    discover = None
    if cname and disease_code:
        discover = get_object_or_404(Discover, cname__cname=cname, disease_code__disease_code=disease_code)

    countries = Country.objects.all()
    diseases = Disease.objects.all()

    if request.method == 'POST':
        cname = Country.objects.get(cname=request.POST['cname'])
        disease_code = Disease.objects.get(disease_code=request.POST['disease_code'])
        first_enc_date = request.POST['first_enc_date']

        if discover:
            discover.cname = cname
            discover.disease_code = disease_code
            discover.first_enc_date = first_enc_date
            discover.save()
        else:
            Discover.objects.create(
                cname=cname,
                disease_code=disease_code,
                first_enc_date=first_enc_date
            )
        return redirect('discover_list')

    return render(request, 'discover_form.html', {
        'discover': discover,
        'countries': countries,
        'diseases': diseases
    })

# List of records
def records_list(request):
    records = Record.objects.all()
    return render(request, 'records/records_list.html', {'records': records})

# Create a new record
def record_create(request):
    countries = Country.objects.all()  # All countries for the dropdown
    diseases = Disease.objects.all()  # All diseases for the dropdown
    if request.method == 'POST':
        email = request.POST['email']
        cname = request.POST['cname']
        disease_code = request.POST['disease_code']
        total_deaths = request.POST['total_deaths']
        total_patients = request.POST['total_patients']

        # Assuming you already have PublicServant, Country, and Disease objects with the given ids
        public_servant = get_object_or_404(PublicServant, email=email)
        country = get_object_or_404(Country, cname=cname)
        disease = get_object_or_404(Disease, disease_code=disease_code)

        # Create the new record
        Record.objects.create(
            email=public_servant,
            cname=country,
            disease_code=disease,
            total_deaths=total_deaths,
            total_patients=total_patients
        )
        return redirect('records_list')
    
    return render(request, 'records/records_form.html', {'countries': countries, 'diseases': diseases})

# Update an existing record
def record_update(request, record_pkey):
    record = get_object_or_404(Record, record_pkey=record_pkey)
    countries = Country.objects.all()
    diseases = Disease.objects.all()
    
    if request.method == 'POST':
        record.email = get_object_or_404(PublicServant, email=request.POST['email'])
        record.cname = get_object_or_404(Country, cname=request.POST['cname'])
        record.disease_code = get_object_or_404(Disease, disease_code=request.POST['disease_code'])
        record.total_deaths = request.POST['total_deaths']
        record.total_patients = request.POST['total_patients']
        record.save()
        return redirect('records_list')
    
    return render(request, 'records/records_form.html', {'record': record, 'countries': countries, 'diseases': diseases})

# Delete an existing record
def record_delete(request, record_pkey):
    record = get_object_or_404(Record, record_pkey=record_pkey)
    
    if request.method == 'POST':
        record.delete()
        return redirect('records_list')
    
    return render(request, 'records/record_confirm_delete.html', {'record': record})
