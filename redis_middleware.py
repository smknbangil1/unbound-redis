import redis
import socket

# Konfigurasi Redis
redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

def init(id, cfg):
    print("✅ Redis middleware initialized...")

def deinit(id):
    print("❌ Redis middleware deinitialized...")

def inform_super(id, qstate, superqstate, qdata):
    pass

def cache_dns_response(qname, rdata):
    redis_key = f"dns:{qname}"
    redis_client.set(redis_key, rdata, ex=300)  # Cache selama 5 menit

def query_redis(qname):
    return redis_client.get(f"dns:{qname}")

def process_query(id, qstate, qdata):
    qname = qstate.qinfo.qname_str
    cached_response = query_redis(qname)

    if cached_response:
        print(f"✅ Cache hit: {qname} -> {cached_response.decode('utf-8')}")
        qstate.ext_state[id] = MODULE_FINISHED
        return True
    else:
        print(f"🔍 Resolving {qname}...")
        try:
            resolver = socket.gethostbyname(qname)
            cache_dns_response(qname, resolver)
            print(f"✅ Cached new result: {qname} -> {resolver}")
        except Exception as e:
            print(f"❌ Error resolving {qname}: {e}")
        qstate.ext_state[id] = MODULE_FINISHED
        return True

def operate(id, event, qstate, qdata):
    if event == MODULE_EVENT_NEW:
        return process_query(id, qstate, qdata)
    return True
