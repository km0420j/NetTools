import dns.resolver
import socket
import pdb

def namequery(name):
    try:
        answers = dns.resolver.query(name, 'A')
        for a in answers:
            a.address
    except dns.resolver.NXDOMAIN:
        return("No record of %s" % name)
    except dns.resolver.Timeout:
        return("Timed out while resolving %s" % name)
    except dns.exception.DNSException:
        return("Unhandled exception")

def namequery2(name):
    try:
        return socket.gethostbyname(name)
    except:
        return None
if __name__ == '__main__':
    name = input("Enter computer name: ")
    print(namequery2(name))

