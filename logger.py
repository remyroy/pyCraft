import getpass
import sys
import Utils
from networking import PacketSenderManager, NetworkManager
from optparse import OptionParser

from datetime import timedelta, datetime



if __name__ == "__main__":
        
    parser = OptionParser()
    
    parser.add_option("-c", "--connection", dest="connection",
        help="connection string CONNECTION")

    parser.add_option("-u", "--username", dest="username", default="",
                  help="username to log in with (only with no gui mode)")
    
    parser.add_option("-p", "--password", dest="password", default="",
                  help="password to log in with (only with no gui mode)")
    
    parser.add_option("-s", "--server", dest="server", default="",
                  help="server to connect to (only with no gui mode)")
    
    parser.add_option("-d", "--dump-packets", 
                  action="store_true", dest="dumpPackets", default=False,
                  help="run with this argument to dump packets")
    
    parser.add_option("-o", "--out-file", dest="filename", default="dump.txt",
                  help="file to dump packets to")
    
    (options, args) = parser.parse_args()

    assert options.connection
    assert options.username
    assert options.password
    assert options.server
            
    user = options.username
    passwd = options.password

    loginThread = Utils.MinecraftLoginThread(user, passwd)
    loginThread.start()
    loginThread.join()

    derp = loginThread.getResponse()

    if(derp['Response'] != "Good to go!"):
        print derp['Response']
        sys.exit()

    sessionid = derp['SessionID']

    print "Logged in as " + derp['Username'] + "! Your session id is: " + sessionid

    stuff = options.server
    
    if ':' in stuff:
        StuffEnteredIntoBox = stuff.split(":")
        host = StuffEnteredIntoBox[0]
        port = int(StuffEnteredIntoBox[1])
    else:
        host = stuff
        port = 25565

    connection = NetworkManager.ServerConnection(None, derp['Username'], passwd, sessionid, host, port, options)
    connection.start()

    start = datetime.utcnow()

    delay = timedelta(seconds=5)

    try:
        while datetime.utcnow() - start < delay:
            pass
    except KeyboardInterrupt, e:
        pass
    connection.disconnect()
    sys.exit(1)
