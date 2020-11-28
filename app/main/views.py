from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json, requests
from psycopg2.extras import Json
from functools import reduce
from django.http import JsonResponse, HttpResponseRedirect
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from django.core.mail import EmailMessage



hashsalt = 'ecmqeslt'


def checksum(st):
    return reduce(lambda x,y:x+y, map(ord, st))


def template(tmpl, add):
    result = str(tmpl)
    dt = add.get('date', datetime.now().date())
    version = add.get('version', 'v001')
    if not (isinstance(dt, date) or isinstance(dt, datetime)):
        dt = datetime.strptime(dt, "%Y-%m-%d").date()
    result = result.replace('{day}', dt.strftime('%d')). \
        replace('{month}', dt.strftime('%m')). \
        replace('{year}', dt.strftime('%Y')). \
        replace('YYYYMM', dt.strftime('%Y%m')). \
        replace('YYYY-MM-DD', dt.strftime('%Y-%m-%d')). \
        replace('YYYY-MM', dt.strftime('%Y-%m')). \
        replace('MMYYYY', dt.strftime('%m%Y')). \
        replace('MM-YYYY', dt.strftime('%m-%Y')). \
        replace('{curr_date}', datetime.now().strftime('%m%Y')). \
        replace('{CURR_DATE}', datetime.now().strftime('%m%Y')). \
        replace('{date}', dt.strftime('%Y-%m-%d')). \
        replace('{DATE}', dt.strftime('%Y_%m_%d')). \
        replace('{datetime}', datetime.now().isoformat()). \
        replace('{dateFrom}', dt.isoformat()). \
        replace('{prevMonth}', (dt-relativedelta(months=1)).strftime('%Y-%m-01')). \
        replace('{nextMonth}', (dt+relativedelta(months=1)).strftime('%Y-%m-01')). \
        replace('{prevDay}', (dt-timedelta(days=1)).strftime('%Y-%m-%d')). \
        replace('{nextDay}', (dt+timedelta(days=1)).strftime('%Y-%m-%d')). \
        replace('{VERSION}', version). \
        replace('{version}', version)
    if isinstance(add, dict):
        for k,v in add.items():
            ktxt = '{%s}' % k
            if v is None:
                val = ''
            elif isinstance(v, date):
                val = v.strftime('%Y-%m-%d')
            elif isinstance(v, datetime):
                val = v.isoformat()
            else:
                val = str(v)
            result = result.replace(ktxt, val)
            if ktxt.lower() in result and k.lower() not in add.keys():
                result = result.replace(ktxt.lower(), v)
            if ktxt.upper() in result and k.upper() not in add.keys():
                result = result.replace(ktxt.upper(), v)
    return result


@csrf_exempt
def setdata(request):
    hash = request.GET.get('hash', '')
    results = {'u': request.user.pk, 'h': hash}
    if 'sa' in hash:
        if request.method == 'POST':
            params = json.loads(request.body.decode('utf-8'))
        else:
            params = request.GET
        params = {k:v for k,v in params.items() if k != 'hash'}
        parvalues = '%s%s' % (''.join([str(x) for x in list(params.values())]), hashsalt)
        if request.user.pk or int(hash[2:]) == checksum(parvalues):
            c = connection.cursor()
            try:
                c.execute("BEGIN")
                c.callproc("fset_" + request.path.split('/')[2], [hash, Json(params), request.user.pk])
                dbresults = c.fetchone()[0]
                c.execute("COMMIT")
            except Exception as e:
                dbresults = {"error": str(e)}
            finally:
                c.close()
            try:
                results = dbresults
                if dbresults.get('django_eval'):
                    res = globals()[dbresults['django_eval']](dbresults)
                    results = {'res': res, 'results': results, 'eval': res.get('eval') or dbresults.get('eval') if type(res) is dict else dbresults.get('eval')}
                if dbresults.get('django_redirect'):
                    return HttpResponseRedirect(results['django_redirect'])
            except Exception as e:
                results = {"error_eval": str(e), "results": dbresults, "eval": "vRes.innerText='Error: %s';" % str(e)}
        else:
            results = {"sm": checksum(parvalues), 'hs': int(hash[2:])}
    else:
        results = {'no': 'hash'}
    return JsonResponse(results, safe=False)

# Create your views here.
