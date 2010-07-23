from datetime import datetime
import uuid
import json

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext,loader
from banquise.web.models import Customer, Host, Package, ServerPackages, Contract, MetaInfo, MetaBug, ChangeLog
from banquise.web.forms import ContractForm, PackageForm, CustomerForm
from django.utils import simplejson
from django.core import serializers
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models.query import QuerySet
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt


supported_client=("0.5")

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

@login_required
def server_package(request,package_id=''):
    package=Package.objects.get(id=package_id)
    link_packages = ServerPackages.objects.filter(package=package).order_by('package__name')
    if request.method == 'POST':
        for host in request.POST.getlist('hosts'): 
            servpack = ServerPackages(host=Host.objects.get(id=host),package=package,
                                  to_install=1,new_install=1)
            servpack.save()
        return HttpResponseRedirect("/web/list/packages/?id=%s" % (package_id))
    
    hosts = Host.objects.all()
    host_list=[]
    host_installed=[]
    for srvpack in link_packages:
        host_installed.append("%s" % (srvpack.host.id))
    for host in hosts:
        if str(host.id) not in host_installed:
            host_list.append(host)
 
    t = loader.get_template('ServerPackage.html')
    scope = _get_default_context({'package':package,
                                  'host_list':host_list,
                                  'tab_package': True,
                                  })
    c = RequestContext(request, scope)
    return HttpResponse(t.render(c))

@login_required
def list_metainfo(request,package_id='',metainfo_id=''):
    """Return a list of :class:`MetaInfo` objects

    :param request: :class:`django.http.HttpRequest` given by the framework
    :type request: :class:`django.http.Request`
    """
    package = get_object_or_404(Package,pk=package_id)
    metainfo = get_object_or_404(MetaInfo,pk=metainfo_id)
    metabugs = MetaBug.objects.filter(metainfo=metainfo).order_by('bugid')
    t = loader.get_template('metainfo.html')
    scope = _get_default_context({'package': package,
                                  'metainfo': metainfo,
                                  'metabugs': metabugs,
                                  'tab_host': True,
                                  })

    c = RequestContext(request, scope)

    return HttpResponse(t.render(c))

@login_required
def list_changelog(request,package_id=''):
    """Return a list of :class:`MetaInfo` objects

    :param request: :class:`django.http.HttpRequest` given by the framework
    :type request: :class:`django.http.Request`
    """
    package = get_object_or_404(Package,pk=package_id)
    changelogs = ChangeLog.objects.filter(package=package).order_by('timestamp')
    t = loader.get_template('changelog.html')
    scope = _get_default_context({'package': package,
                                  'changelogs': changelogs,
                                  'tab_host': True,
                                  })

    c = RequestContext(request, scope)

    return HttpResponse(t.render(c))
    
@login_required
def list_customers(request):
    """Return a list of :class:`Customer` objects

    :param request: :class:`django.http.HttpRequest` given by the framework
    :type request: :class:`django.http.Request`
    """
    customers = Customer.objects.all()
    action=""
    form=""
    ok=0        
    if request.method == 'POST': # If the form has been submitted...
        form = CustomerForm(request.POST) # A form bound to the POST data
        ok=1
        if form.is_valid(): # All validation rules pass
            form.save()
            ok=0
    if (request.GET.get('action') == 'add' and not request.method == 'POST') or ok == 1:
        action='add'
        form = CustomerForm();
    t = loader.get_template('customers.htm')
    scope = _get_default_context({'customers':customers,
                                  'action':action,
                                  'form':form,
                                  'tab_customer': True,
                                  })

    c = RequestContext(request, scope)

    return HttpResponse(t.render(c))

@login_required
def list_hosts(request, contract_id=""):
    """Return a :class:`django.db.models.query.QuerySet` of :class:`Host` objects

    :param request: :class:`django.http.HttpRequest` given by the framework
    :type request: :class:`django.http.Request`
    """
    if contract_id.isdigit():
        hosts = Host.objects.filter(C_h_H=contract_id)
    else:
        hosts = Host.objects.all()
    #contracts = Contract.objects.all()

    t = loader.get_template('hosts.htm')
    c = RequestContext(request, _get_default_context({'hosts':hosts,'tab_host': True}))

    return HttpResponse(t.render(c))

@login_required
def list_packages(request, host_id=""):
    """Return a :class:`django.db.models.query.QuerySet` of :class:`Package` objects

    :param request: :class:`django.http.HttpRequest` given by the framework
    :type request: :class:`django.http.Request`
    """

    #this doesn't work yet
    host = get_object_or_404(Host,pk=host_id)
    packages = ServerPackages.objects.filter(host=host,date_installed__isnull=True,package_installed=0,package_skipped=0).order_by('package__name')
    packages_installed = ServerPackages.objects.filter(host=host,package_installed=True).order_by('package__name')

    if request.method=='POST':
        to_install = request.POST.getlist('to_install')
        pack_in_page= request.POST.getlist('pack_in_page')
        # remove the a package to be installed if it's not more
        # present in the request and not yet installed on the server
        if request.POST.get('update_all'):
            for pack in packages:
                pack.to_install = True
                pack.save()
        elif request.POST.get('skip'):
            for pack in packages:
                pack.package_skipped = True
                pack.to_install = False
                pack.date_installed=datetime.today()
                pack.save()
        else:
            for pack in packages:
                if str(pack.id) not in to_install and str(pack.id) in pack_in_page:
                    if pack.to_install and not pack.date_installed:
                        pack.to_install = False
                        pack.save()
            for id in to_install:
                p = ServerPackages.objects.get(id=id)
                p.to_install = True
                p.save()
        packages = ServerPackages.objects.filter(host=host,date_installed__isnull=True,package_installed=0,package_skipped=0).order_by('package__name')
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
    c = RequestContext(request, _get_default_context({'host':host,'packages':packages_list,'packages_installed':packages_installed_list,
                       'tab_host': True,}))

    return HttpResponse(t.render(c))


@login_required
def details_customer(request, customer_id):
    """Return a :class:`django.db.models.query.QuerySet` of :class:`Customer` objects

    :param request: :class:`django.http.HttpRequest` given by the framework
    :type request: :class:`django.http.Request`
    """
    customer = get_object_or_404(Customer,pk=customer_id)
    contracts = customer.contract_set.all()
    # find the numbers of hosts for this customer
    s = set()
    action=""
    form=""
    for cont in contracts:
        for host in cont.hosts.all():
            s.add(host)
    ok=0        
    if request.method == 'POST': # If the form has been submitted...
        form = ContractForm(request.POST) # A form bound to the POST data
        ok=1
           
        if form.is_valid(): # All validation rules pass
            contract=form.save(commit=False)
            contract.license="%s-%s-%s" % (str(uuid.uuid4())[0:3],str(uuid.uuid4())[0:4],str(uuid.uuid4())[0:3])
            contract.customer=customer
            contract.save()
            ok=0
    if (request.GET.get('action') == 'add' and not request.method == 'POST') or ok == 1:
        action='add'
        form = ContractForm();
    elif (request.GET.get('action') == 'delete'):
        contract = get_object_or_404(Contract,pk=request.GET.get('cont'))    
        contract.delete()
    valid_contracts = contracts.filter(start_date__lte=datetime.today(),end_date__gte=datetime.today())
    old_contracts = contracts.filter(end_date__lt=datetime.today())
    future_contracts = contracts.filter(start_date__gt=datetime.today())


    t = loader.get_template('customerDetails.html')
    scope = _get_default_context({'customer':customer,'tot_hosts':len(s),
                                  'action':action,
                                  'form':form,
                                  'valid_contracts':valid_contracts,
                                  'future_contracts':future_contracts,
                                  'tab_customer': True,
                                  'old_contracts':old_contracts,})
    c = RequestContext(request, scope)

    return HttpResponse(t.render(c))

@login_required
def form_packages(request):
    """Return a :class:`django.db.models.query.QuerySet` of :class:`Package` objects

    :param request: :class:`django.http.HttpRequest` given by the framework
    :type request: :class:`django.http.Request`
    """
    packages=[]
    link_packages=[]
    form = PackageForm();
    pack_id=""
    ok=0
    if request.POST.get("to_install"):
        serv_package=ServerPackages.objects.get(id=request.POST.get("to_install"))
        serv_package.to_install=1
        serv_package.save()
        ok=1
    if request.method == 'POST' and ok == 0: # If the form has been submitted...
        form = PackageForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            s_name = form.cleaned_data['name']
            s_arch = form.cleaned_data['arch']
            s_version = form.cleaned_data['version']
            s_release = form.cleaned_data['release']
            s_repo = form.cleaned_data['repo']
            packages=Package.objects.filter(name__contains=s_name,arch__contains=s_arch,version__contains=s_version,release__contains=s_release,repo__contains=s_repo).order_by('name','arch','version','release')
            
    elif request.GET.get('id'):
        pack_id = request.GET.get('id')
        packages=Package.objects.filter(id=pack_id)
        link_packages = ServerPackages.objects.filter(package=packages).order_by('package__name')
        
    t = loader.get_template('packageForm.html')
    scope = _get_default_context({'tab_package': True,'pack_detail':pack_id,'form':form,'packages':packages,'link_packages':link_packages})
    c = RequestContext(request, scope)

    return HttpResponse(t.render(c))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def check_version(version):
    if version in supported_client:
        return True
    else:
        return False


# REST methods
@csrf_exempt
def call_test(request):
    uuid = request.POST[u'uuid']
    version = request.POST[u'version']
    try:
        host = Host.objects.get(hash=uuid)
        contract_list = Contract.objects.filter(hosts=host,end_date__gte=datetime.today())
        if contract_list:
            #this is ok, the host exists and has a valid contract
            if check_version(version):
                return HttpResponse("OK")
            else:
                return HttpResponse("VERSION")
                
        else:
            #this host has no valid contract linked to it
            return HttpResponse("ERROR2")
    except:
            #no host found
            return HttpResponse("ERROR3")
                  
@csrf_exempt
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

@csrf_exempt
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

@csrf_exempt
def call_send_list(request):
    uuid = request.POST[u'uuid']
    packages = request.POST[u'packages']      
    login = request.POST[u'login']
    passwd = request.POST[u'passwd'] 
    user = authenticate(username=login, password=passwd)
    if user is not None:
        if not user.is_active:
            return HttpResponse("Your account has been disabled!")
    else:
        return HttpResponse("Your username and password were incorrect.")
    if not user.is_staff:
        return HttpResponse("You are not allowed to use this command.")
    
#    parseMeta(metainfo,metabug)           
    for package in json.loads(packages):
        tab = package.split(",")
        try:
            pack = Package.objects.get(name=tab[0],arch=tab[1],version=tab[2],release=tab[3])
        except (Package.DoesNotExist):
            pack = Package(name=tab[0],arch=tab[1],version=tab[2],release=tab[3],repo=tab[4])
            if len(tab) > 5:
                pack.type=tab[5]
                if tab[6] != "none":
                    my_metainfo=MetaInfo.objects.get(updateid=str(tab[6]))
                    pack.metainfo=my_metainfo
            else:
                pack.type="na"
            pack.save()

    return HttpResponse("Ok")
        
@csrf_exempt
def call_send_install(request):
    uuid = request.POST[u'uuid']
    host = Host.objects.get(hash=uuid)
    packages_install_list = [] 
    packages = ServerPackages.objects.filter(host=host,to_install=1,package_installed=0,new_install=1)
    for package in packages:
        packages_install_list.append("%s,%s,%s,%s" % (package.package.name,package.package.arch,package.package.version,package.package.release))
    json_value = json.dumps(packages_install_list)
    return HttpResponse(json_value, mimetype="application/javascript") 

@csrf_exempt
def call_send_ask_update(request):
    uuid = request.POST[u'uuid']
    host = Host.objects.get(hash=uuid)
    packages_install_list = [] 
    packages = ServerPackages.objects.filter(host=host,to_install=1,package_installed=0,new_install=0)
    for package in packages:
        packages_install_list.append("%s,%s,%s,%s" % (package.package.name,package.package.arch,package.package.version,package.package.release))
    json_value = json.dumps(packages_install_list)
    return HttpResponse(json_value, mimetype="application/javascript") 

@csrf_exempt
def call_send_changelog(request):
    pack_id = request.POST[u'pack_id']
    changelog = request.POST[u'changelog']
    package = Package.objects.get(pk=pack_id)
    changelogs = eval(json.dumps(changelog))
    for children in eval(changelogs):
        try:
            change = ChangeLog.objects.get(timestamp=children[0],authorversion=children[1],description=children[2])
        except:    
            change = ChangeLog(timestamp=children[0],authorversion=children[1],description=children[2])
            change.package = package
            change.save()
    return HttpResponse("changelog added")            

@csrf_exempt
def call_send_update(request):
    uuid = request.POST[u'uuid']
    host = Host.objects.get(hash=uuid)
    packages = request.POST[u'packages']      
    package = json.loads(packages)
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
        pack = Package(name=tab[0],arch=tab[1],version=tab[2],release=tab[3],repo=tab[4])
        if len(tab) > 5:
            pack.type=tab[5]
            updateid=tab[6]
            if updateid != 'none':
                my_metainfo=MetaInfo.objects.get(updateid=str(tab[6]))
                pack.metainfo=my_metainfo
        else:
            pack.type="na"
        pack.save()
        # create a link with the server
        servpack = ServerPackages(host=host,package=pack,date_available=datetime.today())
        servpack.save()
        # check if we have to update the package
        #if servpack.to_install:
        #    print "needs to be installed : " + str(pack)     
        #    packages_install_list.append(package)
            #packages_install_list.append("|")
    return HttpResponse(pack.pk) 

@csrf_exempt
def call_send_sync(request):
    uuid = request.POST[u'uuid']
    host = Host.objects.get(hash=uuid)
    packages = request.POST[u'packages']      
    list_of_packages=[]
    tot_added=0
    tot_updated=0
    tot_synced=0
    tot_deleted=0
    
    packages_installed = ServerPackages.objects.filter(host=host,date_installed__isnull=False).order_by('package__name')
    for package in json.loads(packages):
        tab = package.split(",")
        list_of_packages.append(tab[0])
        # find the package
        
        try:
            pack = Package.objects.get(name=tab[0],arch=tab[1],version=tab[2],release=tab[3])
            # is there a link between the package and the server ?    
            try:
                servpack = ServerPackages.objects.get(host=host,package=pack)
                if not servpack.date_installed:
                    servpack.date_synced=datetime.today()
                    servpack.date_installed=datetime.today()
                    servpack.package_installed=1
                    servpack.save()
                    tot_synced=tot_synced+1
                   
            except (ServerPackages.DoesNotExist):
                servpack = ServerPackages(host=host,package=pack,date_available=datetime.today(),date_synced=datetime.today())
                servpack.save()
                tot_updated=tot_updated+1
        except (Package.DoesNotExist):
            pack = Package(name=tab[0],arch=tab[1],version=tab[2],release=tab[3],repo=tab[4])
            pack.type="na"
            pack.updateid="n/a"
            
            pack.save()
            tot_added=tot_added+1
            # create a link with the server
            servpack = ServerPackages(host=host,package=pack,date_available=datetime.today(),date_synced=datetime.today())
            servpack.package_installed=1
            servpack.save()
    for package in packages_installed: 
        if str(package.package.name) not in list_of_packages:
            if package.to_install:
                tot_deleted=tot_deleted+1
                package.removed=1
                package.package_installed=0
                package.to_install=0
                package.date_synced=datetime.today()
                package.save()
    return HttpResponse("synced : %s updated, %s added, %s synced, %s deleted" % (tot_updated,tot_added,tot_synced,tot_deleted))
        
@csrf_exempt
def call_setup(request):
    # search it there is a contract on which we can attach the host
    license_tosearch = request.POST[u'license'] 
    pub_ip=request.META["REMOTE_ADDR"]
    priv_ip=request.POST[u'priv_ip']
    try:
        contract = Contract.objects.get(license=license_tosearch) 
    except:
        return HttpResponse("ERROR0") 
        
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

@csrf_exempt
def call_send_metainfo(request):
    if request.POST[u'metainfo']:
        parseMetaInfo(request.POST[u'metainfo'])
    return HttpResponse("metainfo saved") 

@csrf_exempt
def call_send_metabug(request): 
    if request.POST[u'metabug']:
        parseMetaBug(request.POST[u'metabug'],True)
    return HttpResponse("metabug saved") 
    
@csrf_exempt
def parseMetaInfo(metainfo):
    metadata=json.loads(metainfo)
    if not isinstance(metadata,list):
        metadata_list=[]
        metadata_list.append(metadata)
        metadata=metadata_list
    for data in metadata:
        for meta in data.iteritems():
            # insert the metainfo if needed
            try: 
                my_metainfo = MetaInfo.objects.get(updateid=str(meta[0]))
            except (MetaInfo.DoesNotExist):
                my_metainfo = MetaInfo()
                my_metainfo.updateid=meta[0]
                if meta[1]:
                    if meta[1][0]:
                        my_metainfo.type=meta[1][0]
                    if meta[1][1]:
                        my_metainfo.status=meta[1][1]
                    if meta[1][2]:
                        my_metainfo.description=meta[1][2]
                my_metainfo.save()
    return True
                
@csrf_exempt
def parseMetaBug(metabug,onerecord=False):
    # save the bug info            
    if onerecord:
        metadata=[]
        metadata.append(json.loads(metabug))
    else:
        metadata=json.loads(metabug)
    if metadata: 
        for data in metadata:
            if data: 
                #find the metainfo
                if data[1]:
                    my_metainfo = MetaInfo.objects.get(updateid=str(data[0]))
                    # insert the metainfo if needed
                    for ref in data[1]:
                        try: 
                            my_metabug = MetaBug.objects.get(metainfo=my_metainfo,bugid=ref['id'])
                        except (MetaBug.DoesNotExist):
                            my_metabug = MetaBug()
                            my_metabug.metainfo=my_metainfo
                            if ref['href']:
                                my_metabug.href=ref['href']
                            if ref['id']:
                                my_metabug.bugid=ref['id']
                            if ref['type']:
                                my_metabug.type=ref['type']    
                            if ref['title']:
                                my_metabug.title=ref['title']    
                            my_metabug.save()
    return True
