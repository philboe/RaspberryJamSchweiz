"""@package docstring
sbb module

The sbb module interfaces to http://transport.opendata.ch/ and provides
convenient functions to search the transport database.
"""

import json
import requests
import dateutil.parser
import urllib
class Sbb(object):
    """
    class to interface transport.opendata.ch

    """
    __url = 'http://transport.opendata.ch'
    __APIVersion = 'v1'
    def connections(self,**kwargs):
        """
        straight forward request to ~/connections
        @param self object pointer
        @param **kwargs required are the keys from and to. All arguments are forward as query to ~/connections?query. The description of the parameters can be found here: https://transport.opendata.ch/examples/connections.php
        @return json dictionary
        """
        if not 'from' in kwargs or not 'to' in kwargs:
            raise KeyError("you have to state \'from\' and \'to\' in your request")
        url = "{0}/{1}/connections?{2}".format(self.__url, self.__APIVersion, urllib.urlencode(kwargs))
        resp = requests.get(url)
        data = json.loads(resp.text)
        return data
def nextConnection(von,bis):
    """
    Convenience function. Returns the time of the next connection as a string  
    @param von departure station
    @param bis arrival station
    @return string in the form hh:mm signifying the time of the next train leaving the "von" station in direction "bis".

    """
    sbb = Sbb()
    kwargs = {'from':von, 'to':bis}
    data = sbb.connections(**kwargs)
    #data = json.loads(resp.text)
    mydate= dateutil.parser.parse(data['connections'][0]['from']['departure'])
    return '{0:02d}:{1:02d}'.format(mydate.hour,mydate.minute)
