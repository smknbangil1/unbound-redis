# unbound aja, blm integrasi ke redis
## ini konfig unbound untuk DNS Netral tanpa filtering, forward ke public dns DoT (DNS Over TLS)
```bash
server:
    chroot: ""
    interface: 0.0.0.0
    port: 53

    # Kontrol akses
    access-control: 127.0.0.1 allow
    access-control: 10.0.0.0/8 allow
    access-control: 172.16.0.0/12 allow
    access-control: 192.168.0.0/16 allow
    access-control: 0.0.0.0/0 refuse

    # Keamanan
    hide-identity: yes
    hide-version: yes
    identity: ""
    version: ""
    use-caps-for-id: yes
    do-not-query-localhost: yes
    harden-dnssec-stripped: yes
    harden-below-nxdomain: yes
    harden-referral-path: yes
    harden-large-queries: yes
    harden-short-bufsize: yes
    harden-algo-downgrade: yes
    minimal-responses: yes

    # Optimasi caching
    serve-expired: yes
    serve-expired-ttl: 86400
    serve-expired-client-timeout: 1800
    prefetch: yes
    prefetch-key: yes
    rrset-cache-size: 256m
    msg-cache-size: 256m
    neg-cache-size: 64m
    key-cache-size: 32m
    cache-min-ttl: 300
    cache-max-ttl: 86400

    # Optimasi performa
    num-threads: 4
    outgoing-range: 2048
    num-queries-per-thread: 1024
    so-rcvbuf: 4m
    so-sndbuf: 4m
    max-udp-size: 1232
    edns-buffer-size: 1232

    # Protokol & resolusi
    do-ip4: yes
    do-ip6: no
    do-udp: yes
    do-tcp: yes
    module-config: "validator iterator"
    tls-cert-bundle: "/etc/ssl/certs/ca-certificates.crt"

    # Logging
    verbosity: 1
    log-queries: yes
    log-replies: yes
    logfile: ""
    # logfile: "/var/log/unbound.log"

forward-zone:
    name: "."
    forward-tls-upstream: yes
    forward-first: yes  
    forward-addr: 9.9.9.9@853
    forward-addr: 9.9.9.10@853
    forward-addr: 1.1.1.1@853

remote-control:
    control-enable: yes
    control-interface: 127.0.0.1
```
