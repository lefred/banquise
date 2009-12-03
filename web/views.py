import datetime
import uuid
import json

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext,loader
from banquise.web.models import Customer, Host, Package, ServerPackages, Contract
from django.utils import simplejson
from django.core import serializers


def _get_default_context(dict_in):
    """Returns a :class:`dict` containing all the needed variables for the context

    :param dict_in: input to be added to the default variables
    :type dict_in: :class:`dict`
    :rtype: :class:`dict`
    """

    contracts = Contract.objects.filter(end_date__gte=datetime.date.today()).order_by('end_date')
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

def list_hosts(request):
    """Return a :class:`django.db.models.query.QuerySet` of :class:`Host` objects

    :param request: :class:`django.http.HttpRequest` given by the framework
    :type request: :class:`django.http.Request`
    """

    hosts = Host.objects.all()
    contracts = Contract.objects.all()

    t = loader.get_template('hosts.htm')
    c = RequestContext(request, _get_default_context({'hosts':hosts,}))

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

    valid_contracts = contracts.filter(end_date__gte=datetime.date.today())
    old_contracts = contracts.filter(end_date__lt=datetime.date.today())


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
       contract_list = Contract.objects.filter(hosts=host,end_date__gte=datetime.date.today())
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
    for package in json.loads(packages):
        tab = package.split(",")
        # find the package
        try:
            pack = Package.objects.get(name=tab[0],arch=tab[1],version=tab[2],release=tab[3])
            # is there a link between the package and the server ?    
            try:
                servpack = ServerPackages.objects.get(host=host,package=pack)
                servpack.date_installed=datetime.date.now()
                servpack.package_installed=1
                servpack.save()
            except (ServerPackages.DoesNotExist):
                servpack = ServerPackages(host=host,package=pack,
                                          package_installed=1,
                                          date_available=datetime.date.now(),
                                          date_installed=datetime.date.now())
                servpack.save()
        except (Package.DoesNotExist):
            pack = Package(name=tab[0],arch=tab[1],version=tab[2],release=tab[3])
            pack.save()
            # create a link with the server
            servpack = ServerPackages(host=host,package=pack,date_available=datetime.date.now(),
                                      package_installed=1,date_installed=datetime.date.now())
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
                servpack = ServerPackages(host=host,package=pack,date_available=datetime.date.now())
                servpack.save()
        except (Package.DoesNotExist):
            pack = Package(name=tab[0],arch=tab[1],version=tab[2],release=tab[3])
            pack.save()
            # create a link with the server
            servpack = ServerPackages(host=host,package=pack,date_available=datetime.date.now())
            servpack.save()
        # check if we have to update the package
        if servpack.to_install:
            print "needs to be installed : " + str(pack)     
            packages_install_list.append(package)
            #packages_install_list.append("|")
    json_value = json.dumps(packages_install_list)
    return HttpResponse(json_value, mimetype="application/javascript") 
        
def call_setup(request):
   # search it there is a contract on which we can attach the host
   license_tosearch = request.POST[u'license'] 
   contract = Contract.objects.get(license=license_tosearch) 
   customer = Customer.objects.filter(contract=contract)
   try: 
       # search if the host exists alreay 
       host = Host.objects.get(name=request.POST[u'hostname'])
       # is it link to a valid contract already ?
       contract_list = Contract.objects.filter(customer=customer,hosts=host,end_date__gte=datetime.date.today())
       if contract_list:
           print "This host is already linked to a valid contract" 
           return HttpResponse("ERROR1") 
       
   except:     
       host = Host(name=request.POST[u'hostname'])
   # generate a hash to identify the host
   host.hash = str(uuid.uuid4())[0:8]
   host.release = request.POST[u'release']
   host.save()
   contract.hosts.add(host)   
   contract.save()
   #json_value = serializers.serialize('json',contract)
   #return HttpResponse(json_value, mimetype="application/javascript") 
   return HttpResponse(host.hash)
