from datetime import datetime
import uuid
import json

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext,loader
from banquise.web.models import Customer, Host, Package, ServerPackages, Contract
from django.utils import simplejson
from django.core import serializers
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models.query import QuerySet

def _get_default_context(dict_in):
    """Returns a :class:`dict` containing all the needed variables for the context

    :param dict_in: input to be added to the default variables
    :type dict_in: :class:`dict`
    :rtype: :class:`dict`
    """

    contracts = Contract.objects.filter(end_date__gte=datetime.today()).order_by('end_date')
    d = {'contracts':contracts,}

    if dict_in:
        d.update(dict_in)
    return d

def index(request):

    t = loader.get_template('index.html')
    c = RequestContext(request, _get_default_context(None))

    return HttpResponse(t.render(c))

def list_customers(request):
    """Return a list of :class:`Customer` objects

    :param request: :class:`django.http.HttpRequest` given by the framework
    :type request: :class:`django.http.Request`
    """
    customers = Customer.objects.all()

    t = loader.get_template('customers.htm')
    scope = _get_default_context({'customers':customers,})

    c = RequestContext(request, scope)

    return HttpResponse(t.render(c))

def list_hosts(request, contract_id=""):
    """Return a :class:`django.db.models.query.QuerySet` of :class:`Host` objects

    :param request: :class:`django.http.HttpRequest` given by the framework
    :type request: :class:`django.http.Request`
    """

    if contract_id.isdigit():
        hosts = Host.objects.filter(C_h_H=contract_id)
    else:
        hosts = Host.objects.all()
    contracts = Contract.objects.all()

    t = loader.get_template('hosts.htm')
    c = RequestContext(request, _get_default_context({'hosts':hosts,}))

    return HttpResponse(t.render(c))

def list_packages(request, host_id=""):
    """Return a :class:`django.db.models.query.QuerySet` of :class:`Package` objects

    :param request: :class:`django.http.HttpRequest` given by the framework
    :type request: :class:`django.http.Request`
    """

    #this doesn't work yet
    host = get_object_or_404(Host,pk=host_id)
    packages = ServerPackages.objects.filter(host=host,date_installed__isnull=True,package_skipped=0).order_by('package__name')
    packages_installed = ServerPackages.objects.filter(host=host,date_installed__isnull=False).order_by('package__name')

    if request.method=='POST':
        to_install = request.POST.getlist('to_install')
        # remove the a package to be installed if it's not more
        # present in the request and not yet installed on the server
        for pack in packages:
            if str(pack.id) not in to_install:
                if pack.to_install and not pack.date_installed:
                    pack.to_install = False
                    pack.save()
        for id in to_install:
            p = ServerPackages.objects.get(id=id)
            p.to_install = True
            p.save()
        packages = ServerPackages.objects.filter(host=host,date_installed__isnull=True,package_skipped=0).order_by('package__name')
    paginator = Paginator(packages, 25)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        packages_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        packages_list = paginator.page(paginator.num_pages)
        
    paginator_history = Paginator(packages_installed, 25)
    try:
        page_hist = int(request.GET.get('page_hist', '1'))
    except ValueError:
        page_hist = 1
    try:
        packages_installed_list = paginator_history.page(page_hist)
    except (EmptyPage, InvalidPage):
        packages_installed_list = paginator_history.page(paginator_history.num_pages)

    t = loader.get_template('packages.html')
    c = RequestContext(request, _get_default_context({'packages':packages_list,'packages_installed':packages_installed_list}))

    return HttpResponse(t.render(c))


def details_customer(request, customer_id):
    """Return a :class:`django.db.models.query.QuerySet` of :class:`Customer` objects

    :param request: :class:`django.http.HttpRequest` given by the framework
    :type request: :class:`django.http.Request`
    """
    customer = get_object_or_404(Customer,pk=customer_id)
    contracts = customer.contract_set.all()
    # find the numbers of hosts for this customer
    s = set()
    for cont in contracts:
        for host in cont.hosts.all():
            s.add(host)

    valid_contracts = contracts.filter(end_date__gte=datetime.today())
    old_contracts = contracts.filter(end_date__lt=datetime.today())


    t = loader.get_template('customerDetails.html')
    scope = _get_default_context({'customer':customer,'tot_hosts':len(s),
                                  'valid_contracts':valid_contracts,
                                  'old_contracts':old_contracts,})
    c = RequestContext(request, scope)

    return HttpResponse(t.render(c))

# REST methods
def call_test(request):
   uuid = request.POST[u'uuid']
   try:
	   host = Host.objects.get(hash=uuid)
	   contract_list = Contract.objects.filter(hosts=host,end_date__gte=datetime.today())
	   if contract_list:
		   #this is ok, the host exists and has a valid contract
		   return HttpResponse("OK") 
	   else:
		   #this host has no valid contract linked to it
		   return HttpResponse("ERROR2")
   except:
		   #no host found
		   return HttpResponse("ERROR3")
                  
def call_set_release(request):
   uuid = request.POST[u'uuid']
   try:
       host = Host.objects.get(hash=uuid)
       host.release = request.POST[u'release']
       host.save()
       return HttpResponse("OK") 
   except:     
       # can set the release
       return HttpResponse("ERROR4") 

def call_packs_done(request):
    uuid = request.POST[u'uuid']
    host = Host.objects.get(hash=uuid)
    packages = request.POST[u'packages'] 
    packages_skipped = request.POST[u'packages_skipped']
    
    # mark skipped all packages not more found on the repo
    for skip_package in json.loads(packages_skipped):
        skip_tab = skip_package.split(",")
        # find the package
        skip_pack = Package.objects.get(name=skip_tab[0],arch=skip_tab[1],version=skip_tab[2],release=skip_tab[3])
        # is there a link between the package and the server ?    
        skip_servpack = ServerPackages.objects.get(host=host,package=skip_pack)
        skip_servpack.date_installed=datetime.today()
        skip_servpack.package_skipped=1
        skip_servpack.to_install=0
        skip_servpack.save()
    
    for package in json.loads(packages):
        tab = package.split(",")
        # find the package
        try:
            pack = Package.objects.get(name=tab[0],arch=tab[1],version=tab[2],release=tab[3])
            # is there a link between the package and the server ?    
            try:
                servpack = ServerPackages.objects.get(host=host,package=pack)
                servpack.date_installed=datetime.today()
                servpack.package_installed=1
                servpack.save()
            except (ServerPackages.DoesNotExist):
                servpack = ServerPackages(host=host,package=pack,
                                          package_installed=1,
                                          date_available=datetime.today(),
                                          date_installed=datetime.today())
                servpack.save()
        except (Package.DoesNotExist):
            pack = Package(name=tab[0],arch=tab[1],version=tab[2],release=tab[3])
            pack.save()
            # create a link with the server
            servpack = ServerPackages(host=host,package=pack,date_available=datetime.today(),
                                      package_installed=1,date_installed=datetime.today())
            servpack.save()
    return HttpResponse("Packages updated")
        
def call_send_update(request):
    uuid = request.POST[u'uuid']
    host = Host.objects.get(hash=uuid)
    packages = request.POST[u'packages']      
    packages_install_list = [] 
    for package in json.loads(packages):
        tab = package.split(",")
        # find the package
        try:
            pack = Package.objects.get(name=tab[0],arch=tab[1],version=tab[2],release=tab[3])
            # is there a link between the package and the server ?    
            try:
                servpack = ServerPackages.objects.get(host=host,package=pack)
            except (ServerPackages.DoesNotExist):
                servpack = ServerPackages(host=host,package=pack,date_available=datetime.today())
                servpack.save()
        except (Package.DoesNotExist):
            pack = Package(name=tab[0],arch=tab[1],version=tab[2],release=tab[3])
            pack.save()
            # create a link with the server
            servpack = ServerPackages(host=host,package=pack,date_available=datetime.today())
            servpack.save()
        # check if we have to update the package
        #if servpack.to_install:
        #    print "needs to be installed : " + str(pack)     
        #    packages_install_list.append(package)
            #packages_install_list.append("|")
    packages = ServerPackages.objects.filter(host=host,to_install=1,package_installed=0)
    for package in packages:
        #print "needs to be installed : %s,%s,%s,%s" % (package.package.name,package.package.arch,package.package.version,package.package.release)  
        packages_install_list.append("%s,%s,%s,%s" % (package.package.name,package.package.arch,package.package.version,package.package.release))
    json_value = json.dumps(packages_install_list)
    return HttpResponse(json_value, mimetype="application/javascript") 
        
def call_setup(request):
   # search it there is a contract on which we can attach the host
   license_tosearch = request.POST[u'license'] 
   pub_ip=request.META["REMOTE_ADDR"]
   priv_ip=request.POST[u'priv_ip']
   contract = Contract.objects.get(license=license_tosearch) 
   customer = Customer.objects.filter(contract=contract)
   try: 
       # search if the host exists alreay 
       host = Host.objects.get(name=request.POST[u'hostname'])
       # is it link to a valid contract already ?
       contract_list = Contract.objects.filter(customer=customer,hosts=host,end_date__gte=datetime.today())
       if contract_list:
           print "This host is already linked to a valid contract" 
           return HttpResponse("ERROR1") 
       
   except:     
       host = Host(name=request.POST[u'hostname'])
   # generate a hash to identify the host
   host.hash = str(uuid.uuid4())[0:8]
   host.release = request.POST[u'release']
   host.ip = priv_ip
   host.public_ip=pub_ip
   host.save()
   contract.hosts.add(host)   
   contract.save()
   #json_value = serializers.serialize('json',contract)
   #return HttpResponse(json_value, mimetype="application/javascript") 
   return HttpResponse(host.hash)
