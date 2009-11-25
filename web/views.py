import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext,loader
from banquise.web.models import Customer, Host, Package, Contract
from django.utils import simplejson
from django.core import serializers


def _get_default_context(dict_in):
    """Returns a :class:`dict` containing all the needed variables for the context

    :param dict_in: input to be added to the default variables
    :type dict_in: :class:`dict`
    :rtype: :class:`dict`
    """

    contracts = Contract.objects.filter(end_date__gte=datetime.date.today()).order_by('end_date')
    d = {'contracts':contracts}
 
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

def call_setup(request):
   print request.POST 
   # search it there is a contract on which we can attach the host
   license_tosearch = request.POST[u'license'] 
   contract = Contract.objects.get(license=license_tosearch) 
   host = Host(name=request.POST[u'hostname'])
   host.save()
   contract.hosts.add(host)   
   contract.save()
   json_value = serializers.serialize('json',contract)
   return HttpResponse(json_value, mimetype="application/javascript") 