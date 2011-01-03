from dajax.core.Dajax import Dajax
from dajaxice.core import dajaxice_functions
from datetime import date
from datetime import datetime
from datetime import timedelta
from banquise.web.models import Customer, Host, Package, ServerPackages, Contract, MetaInfo, MetaBug, ChangeLog
from banquise.web.forms import ContractForm, PackageForm, CustomerForm, HistoryForm

def display_valid_contracts(request,host_id):
        dajax = Dajax()
        valid_contracts = Contract.objects.filter(start_date__lte=datetime.today(),
                                          end_date__gte=datetime.today())
        msg = "<strong>Valid contracts :</strong><table>"
        print str(valid_contracts)
        for contract in valid_contracts:
            msg += "<tr class='hosts_expand'><td>%s</td><td>" % contract
            msg += "<span onclick=\"Dajaxice.banquise.web.add_host_to_contract('Dajax.process',{'host_id':%s,'contract_id':%s});\">" % (host_id, contract.id)
            msg += "<img src='/media/images/icons/ok.png' height='16' border='0'></span></td></tr>" 
        msg += "</table>"
        div_id="#host_%s" % host_id
        dajax.assign(div_id,'innerHTML',msg)
        return dajax.json()
    
dajaxice_functions.register(display_valid_contracts)

def add_host_to_contract(request,host_id,contract_id):
        dajax = Dajax()
        host = Host.objects.get(id=host_id)
        contract = Contract.objects.get(id=contract_id)
        contract.hosts.add(host)
        contract.save()
        msg = ""
        div_id="#img_host_%s" % host_id
        dajax.assign(div_id,'innerHTML',msg)
        div_id="#host_%s" % host_id
        dajax.assign(div_id,'innerHTML',msg)
        return dajax.json()

dajaxice_functions.register(add_host_to_contract)