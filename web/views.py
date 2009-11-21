from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext,loader
from banquise.web.models import Customer, Host, Package, Contract


def index(request):
    return render_to_response('index.html')


def list_customers(request):
    """Return a list of customers

    :param request: request given by the framework
    :type request: :class:`django.http.Request`
    """
    c = Customer.objects.all()

    t = loader.get_template('customers.htm')
    c = RequestContext(request, {'c':c})

    return HttpResponse(t.render(c))
