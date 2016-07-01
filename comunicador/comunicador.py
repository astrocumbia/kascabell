### comunicador.py
###
### @author Jose Figueroa Martinez <jfigueroa@mixteco.utm.mx>
### @date 20160306
### @lecture Computo Ubicuo
###
### La idea del comunicador es que se inicializa la principio.
### Luego, cada servicio lo busca en el puerto 9100 para que se le asigne un
### puerto y para que se le proporcionen los datos de sus provedores y
### consumidores.
###
### El comunicador no sabe de dependencias, con lo cual se va a basar en lo que
### le digan los modulos en sus comunicaciones.
###
### La idea es que le comuniquen cuando una dependencia esta caida para que la
### quite de los activos, y que cuando se vaya una dependencia le pueda avisar
### al comunicador y el comunicador le avise a los demas.
###
### Digamos que es un manejador de dependencias para que nadie tenga que
### escanear la red mas de una ves.
###
### TODO documentar mejor :-)

import paste    # pip install paste # web server
from bottle import route, run, request, response, post, get  # framework web
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import json
import requests #http requests
import copy

##################################################
### VARS ###

config = {}
ss_modules = []         # shared-state de modulos registrados.
ss_changes = Queue(0)   # shared-state changes a aplicar en los ss_modules.
ss_ports   = Queue(1)   # shared-state ports. Para generar un puerto a la vez.
ss_nots    = Queue(0)   # shared-state notificaciones a consumidores.

ss_state            = {}         # shared-state for the state of modules. Keys are module-names.
ss_state_changes    = Queue(0)   # shared-state for state changes

##################################################
### UTILS ###

# Acronimo de get_file_contents
def gfc(fi):
    with open(fi) as f:
        co = f.read()

    return co

def buscamod(modules, typ, nam):
    for m in modules:
        if (m['type'] ==  typ) and (m['name'] == nam):
            return m

    return None

def get_providers(modules, mod):
    r = []
    for m in modules:
        if m['type'] in mod['providers']:
            for l in m['locations']:
                if l in mod['locations']:
                    r.append({"type": m["type"], "name": m["name"],
                              "version": m["version"], "ip": m["ip"], "port": m['port']})
                    break
    
    return r

def get_consumers(modules, typ, locs):
    r   = []
    for m in modules:
        if typ in m['providers']:
            for loc in locs:
                if loc in m['locations']:
                    r.append({"type": m["type"], "name": m["name"],
                        "version": m["version"], "ip": m["ip"], "port": m['port']})
                    break

    return r

################################################
### RUTAS ###
def jrender(r, data):
    r.set_header('Content-Type', 'application/json')
    return json.dumps(data, sort_keys=True, indent=4)

@route('/')
def index():
    return jrender(response, config)
   
@route('/domotic')
def domotic():
    return jrender(response, True)

# Debe devolver el mismo puerto para el mismo dispositivo si ya lo habia
# pedido antes.
#
# Variables post: providers (json array en una string),
#                 locations (json array en una string)
#
# Nota: El cliente DEBE incluir el parametro "providers" en su post codificada
#       como variable de formulario y si no tiene providers debe mandar un
#       arreglo json en texto "[]". El contenido de "providers" es una cadena
#       de texto json con los providers. Ej: "[\"monitor\", \"voceador\"]"
@post('/register/<typ>/<nam>/<ver>')
def register(typ, nam, ver):
    ip    = request.environ.get('REMOTE_ADDR')
    provs = json.loads(request.forms.providers)
    locs  = json.loads(request.forms.locations)
    return jrender(response, get_port(typ, nam, ver, provs, locs, ip))

@route('/modules')
def route_modules():
    return jrender(response, ss_modules)

# Proporciona los datos de todos los modulos que estan mandando su state.
@route('/monitor')
def route_monitor():
    nmodules = []
    for m in ss_modules:
        nm = copy.copy(m)
        if nm["name"] in ss_state:
            nm["state"] = ss_state[ nm["name"] ]

        nmodules.append(nm)

    return jrender(response, nmodules)

# Actualiza los datos de state de cualquier modulo. Los datos vienen en la
# variable con nombre 'state'
#
# Variables post: state (objeto json en string)
#
@post('/monitor/<typ>/<nam>')
def route_monitor_component(typ, nam):
    mod = buscamod(ss_modules, typ, nam)
    if (None != mod):
        try:
            state = json.loads(request.forms.state)
            ss_state_changes.put({"name": nam, "state": copy.copy(state)})
            r = state
        except Error as err:
            r = None
    else:
        r = None
    
    return jrender(response, r)


@get('/monitor/<typ>/<nam>')
def route_monitor_component_get(typ, nam):
    mod     = buscamod(ss_modules,typ, nam)
    nmod    = copy.copy(mod)
    state  = {}

    if (None != mod):
        if nam in ss_state:
            state = ss_state[nam]
            nmod["state"] = state

    return jrender(response, nmod)



#################################################
### FUNCIONES PRINCIPALES

def get_port(typ, nam, ver, provs, locs, ip):
    omod = buscamod(ss_modules, typ, nam)
    
    mod = {"type": typ, "name": nam, "version": ver, "ip": ip,
           "providers": provs, "locations": locs}

    if omod != None:
        print("Modulo ya estaba previamente")
        print(omod)
        port            = omod['port']
        mod['port']     = port
        nmod            = copy.copy(omod)
        nmod['changes'] = 'remove' # Quitar de ss_modules para reemplazar
        ss_changes.put(nmod)
    else:
        port        = ss_ports.get()
        mod['port'] = port
        ss_ports.task_done()

    mod['changes'] = 'add'
    ss_changes.put(copy.copy(mod)) # Agregar a ss_modules

    providers = get_providers(ss_modules, mod)

    r = {"port": port,
         "providers": providers}

    ss_nots.put(copy.copy(mod))    # Notificar a consumidores

    return r

#################################################
### SERVICIOS PERMANENTES SOBRE QUEUES

def port_provider(fport =  9101):
    while True:
        ss_ports.put(fport)
        fport = fport + 1
    
# Aplicador de cambios.
#
# Un solo thread sacando de la queue de cambios asegura que no va a haber
# acceso concurrente inapropiado.
#
# Estructura ejemplo de un cambio:
# {"change": "add | remove",
#  "type": "monitor, "name": "m1", "port": 9101, "version": "0.0.1",
#  "providers": ["monitor"], "ip": "127.0.0.1"}
def change_applier():
    while True:
        mod = ss_changes.get()
        op  = mod["changes"]
        del  mod["changes"]
    
        if op == "add":
            print("Agregando " )
            print(mod)
            ss_modules.append(mod)
        else:
            print("Quitando ")
            print(mod)
            ss_modules.remove(mod)

        ss_changes.task_done()
    return mod

def state_change_applier():
    while True:
        ch      = ss_state_changes.get()
        nam     = ch["name"]
        state   = ch["state"]
        
        ss_state[nam] = state

        ss_state_changes.task_done()

    return True

def notify_changes():
    while True:
        mod = ss_nots.get()
        ss_nots.task_done()

        print("Notificando cambios para modulo")
        print(mod)
        op  = mod['changes']
        del mod['changes']
        cons = get_consumers(ss_modules, mod['type'], mod['locations'])

        for c in cons:
            try:
                if op == "add":
                    url = 'http://' + c['ip'] + ':' + str(c['port']) + \
                    '/provider'
                    print("Notificando alta de " + mod['type'] + "/" + \
                            mod['name'] + " a " + c['type'] + "/" + c['name'] + " en " + url)
                    r = requests.post(url,  data = mod)
                else:
                    url = 'http://' + c['ip'] + ':' + str(c['port']) + \
                    '/provider/'+ mod['type'] + '/' + mod['name']
                    print("Notificando baja de " + mod['type'] + "/" + \
                            mod['name'] + " a " + url)
                    r = requests.delete(url)
            except requests.exceptions.RequestException:
                pass    # Por ahora, no importa si no responden.

def run_server():
    run(server='paste', host="0.0.0.0", port=config["port"])
    return True

###########
### CALLBACKS DE TERMINO de FUTURES

def nots_stopped():
    print("Dejo de notificar")

def changes_stopped():
    print("Dejo de aplicar cambios")

def ports_stopped():
    print("Dejo de dar puertos")

def state_changes_stopped():
    print("Dejo de aplicar cambios en state")

#####################################
if __name__ == '__main__':

    conf_file = "config.json"   # puede cambiarse por parametros
    config = json.loads (gfc(conf_file)) # leer el contenido del archivo

    ## SERVICIOS PERMANENTES EN FUTURES
    ex        = ThreadPoolExecutor(max_workers=200)

    port_prov = ex.submit(port_provider)
    change_ap = ex.submit(change_applier)
    schang_ap = ex.submit(state_change_applier)
    notifc    = ex.submit(notify_changes)
    server    = ex.submit(run_server)

    # ALTA DE CALLBACKS DE FINALIZACION
    port_prov.add_done_callback(ports_stopped)
    change_ap.add_done_callback(changes_stopped)
    notifc.add_done_callback(nots_stopped)
    schang_ap.add_done_callback(state_changes_stopped)

