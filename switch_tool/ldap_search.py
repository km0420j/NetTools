import base64
from ldap3 import Server, Connection, ALL
from credentials import ldapusername, ldappassword

def computer_by_user(username):
    # search AD, return list of computers with username in description
    server = '172.20.1.185'
    try:
        conn = Connection(server, base64.b64decode(ldapusername), 
                                  base64.b64decode(ldappassword))

        conn.bind()
        search_filter = '(&(objectclass=computer)(description=*{}*))'.format(username)
        conn.search('ou=ZGF Root,dc=zgf,dc=local',search_filter, attributes=['cn'])
        return [x.cn.value for x in conn.entries]

    except:
        return ['An Error Occured']



    
