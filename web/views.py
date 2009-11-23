import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext,loader
from banquise.web.models import Customer, Host, Package, Contract

def _get_default_context(dict_in):
    """Returns a :class:`dict` containing all the needed variables for the context

    :param dict_in: input to be added to the default variables
    :type dict_in: :class:`dict`
    :rtype: :class:`dict`
    """

    contracts = Contract.objects.all().order_by('end_date')
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
    c_list = list()
    for c in customers:
        c_list.append({
            'name':c.name,
            'end_date': c.contract_set.latest().end_date,
            'days_left': (c.contract_set.latest().end_date - datetime.date.today()).days,
            'id': c.pk
            })

    t = loader.get_template('customers.htm')
    scope = _get_default_context({'customers':c_list,})

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

    t = loader.get_template('customerDetails.html')
    scope = _get_default_context({'customer':customer,})
    c = RequestContext(request, scope)

    return HttpResponse(t.render(c))