#create by 2014.05
#author junbao.kjb
#
#DNS parser
#

import re, struct, types


'''
define the DNS packet struct, 
'''
class DNSPacket:
    def __init__(self, data, dns_type):
        ''' parse DNS packet '''
        self.decode(data, dns_type)


    def get_len(self):
        return self.DATA_LEN

    def get_id(self):
        return self.id

    def get_qr(self):
        return self.qr

    def get_opcode(self):
        return self.opcode

    def get_aa(self):
        return self.aa

    def get_tc(self):
        return self.tc

    def get_rd(self):
        return self.rd

    def get_ra(self):
        return self.ra

    def get_z(self):
        return self.z

    def get_rcode(self):
        return self.rcode

    def get_qdcount(self):
        return self.qdcount

    def get_ancount(self):
        return self.ancount

    def get_nscount(self):
        return self.nscount

    def get_arcount(self):
        return self.arcount

    def get_qd(self):
        return self.qd

    def get_qd_name(self):
        tmp = []
        for item in self.qd:
            tmp.append(item['qd_name'])
        return tmp

    def get_qd_type(self):
        tmp = []
        for item in self.qd:
            tmp.append(item['qd_type'])
        return tmp

    def get_qd_class(self):
        tmp = []
        for item in self.qd:
            tmp.append(item['qd_class'])
        return tmp

    def get_an(self):
        return self.an

    def get_an_type(self):
        tmp = []
        for item in self.an:
            tmp.append(item['an_type'])
        return tmp

    def get_an_class(self):
        tmp = []
        for item in self.an:
            tmp.append(item['an_class'])
        return tmp

    def get_an_ttl(self):
        tmp = []
        for item in self.an:
            tmp.append(item['an_ttl'])
        return tmp

    def get_an_len(self):
        tmp = []
        for item in self.an:
            tmp.append(item['an_len'])
        return tmp

    def get_an_rdata(self):
        tmp = []
        for item in self.an:
            tmp.append(item['an_rdata'])
        return tmp

    def get_an_name(self):
        tmp = []
        for item in self.an:
            tmp.append(item['an_name'])
        return tmp

    def get_ns(self):
        return self.ns

    def get_ns_type(self):
        tmp = []
        for item in self.ns:
            tmp.append(item['ns_type'])
        return tmp

    def get_ns_class(self):
        tmp = []
        for item in self.ns:
            tmp.append(item['ns_class'])
        return tmp

    def get_ns_ttl(self):
        tmp = []
        for item in self.ns:
            tmp.append(item['ns_ttl'])
        return tmp

    def get_ns_len(self):
        tmp = []
        for item in self.ns:
            tmp.append(item['ns_len'])
        return tmp

    def get_ns_rdata(self):
        tmp = []
        for item in self.ns:
            if item.has_key('ns_rdata'):
                tmp.append(item['ns_rdata'])
        return tmp

    def get_ns_name(self):
        tmp = []
        for item in self.ns:
            tmp.append(item['ns_name'])

    def get_ns_cache(self):
        tmp=[]
        for item in self.ns:
            if item.has_key('ns_cache'):
                tmp.append(item['ns_cache'])
        return tmp

    def get_ns_prins(self):
        tmp=[]
        for item in self.ns:
            if item.has_key('ns_prins'):
                tmp.append(item['ns_prins'])
        return tmp

    def get_ns_respmail(self):
        tmp=[]
        for item in self.ns:
            if item.has_key('ns_respmail'):
                tmp.append(item['ns_respmail'])
        return tmp

    def get_ns_sn(sn):
        tmp=[]
        for item in self.ns:
            if item.has_key('ns_sn'):
                tmp.append(item['ns_sn'])
        return tmp

    def get_ns_refint(self):
        tmp=[]
        for item in self.ns:
            if item.has_key('ns_refint'):
                tmp.append(item['ns_refint'])
        return tmp
    def get_ns_retint(self):
        tmp=[]
        for item in self.ns:
            if item.has_key('ns_retint'):
                tmp.append(item['ns_retint'])
        return tmp

    def get_ns_exlim(self):
        tmp=[]
        for item in self.ns:
            if item.has_key('ns_exlim'):
                tmp.append(item['ns_exlim'])
        return tmp

    def get_ns_mimttl(self):
        tmp=[]
        for item in self.ns:
            if item.has_key('ns_mimttl'):
                tmp.append(item['ns_mimttl'])
        return tmp

    def decode(self, data, dns_type):
        iter=0
        self.DATA_LEN=len(data)
        if dns_type == 'TCP':
            high=struct.unpack('B', data[iter])[0]
            low= struct.unpack('B', data[iter+1])[0]
            length =high*256 + low 
            if length+2 != len(data):
                raise
            iter += 2

        self.id=struct.unpack('>H', data[iter:iter+2])[0]
        iter += 2

        high=struct.unpack('B', data[2])[0]
        low= struct.unpack('B', data[3])[0]
        self.qr    = (high >> 7)
        self.opcode= (high >> 3) & 0x0F
        self.aa    = (high >> 2) & 0x01
        self.tc    = (high >> 1) & 0x01
        self.rd    =  high       & 0x01
        self.ra    = (low >> 7)  & 0x01
        self.z     = (low >> 4)  & 0x07
        self.rcode = low         & 0x0F
        iter += 2
    
        self.qdcount=struct.unpack('>H', data[iter:iter+2])[0]
        self.ancount=struct.unpack('>H', data[iter+2:iter+4])[0]
        self.nscount=struct.unpack('>H', data[iter+4:iter+6])[0]
        self.arcount=struct.unpack('>H', data[iter+6:iter+8])[0]
        iter += 8

        self.qd=[]; tmp_name=''
        for i in range(0, self.qdcount):
            (tmp_name, iter)=self.get_name(data, iter)
            iter +=1
            qdtype = struct.unpack('>H', data[iter:iter+2])[0]
            iter += 2
            qdclass = struct.unpack('>H', data[iter:iter+2])[0]
            iter += 2
            qd_item = {'qd_name': tmp_name, 'qd_type': qdtype, 'qd_class': qdclass}
            self.qd.append(qd_item)
         
        self.an=[]; tmp_name=''
        for i in range(0, self.ancount):
            (tmp_name, iter)=self.get_name(data, iter)
            iter +=1
            antype = struct.unpack('>H', data[iter:iter+2])[0]
            iter += 2
            # A type
            if antype == 1:
                anclass = struct.unpack('>H', data[iter:iter+2])[0]
                iter += 2
                anttl =  struct.unpack('>I', data[iter:iter+4])[0]
                iter += 4
                anlen = struct.unpack('>H', data[iter:iter+2])[0]
                iter += 2
                add1 =struct.unpack('B', data[iter])[0]
                add2 =struct.unpack('B', data[iter+1])[0]
                add3 =struct.unpack('B', data[iter+2])[0]
                add4 =struct.unpack('B', data[iter+3])[0]
                iter += 4
                rdata = str(add1) + '.' + str(add2) + '.' + str(add3) + '.' + str(add4)
                an_item = {'an_name': tmp_name, 'an_type': antype, 'an_class': anclass, 'an_ttl': anttl, 'an_len': anlen, 'an_rdata': rdata}
                self.an.append(an_item)
                
            # NS & CNAME type
            elif antype == 2 or antype == 5:
                
                anclass = struct.unpack('>H', data[iter:iter+2])[0]
                iter += 2
                anttl =  struct.unpack('>I', data[iter:iter+4])[0]
                iter += 4
                anlen = struct.unpack('>H', data[iter:iter+2])[0]
                iter += 2
                (rdata, iter)=self.get_name(data, iter)
                an_item = {'an_name': tmp_name, 'an_type': antype, 'an_class': anclass, 'an_ttl': anttl, 'an_len': anlen, 'an_rdata': rdata}
                self.an.append(an_item)
                iter+=1
                
            # SOA type
            elif antype == 6:
                anclass = struct.unpack('>H', data[iter:iter+2])[0]
                anclass &= 0x7fff
                ancache &= 0x8000
                iter += 2
                anttl = struct.unpack('>I', data[iter:iter+4])[0]
                iter += 4
                anlen = struct.unpack('>H', data[iter:iter+2])[0]
                iter += 2
                (anpns, iter)=self.get_name(data, iter)
                (anram, iter)=self.get_name(data, iter)
                ansn =  struct.unpack('>I', data[iter:iter+4])[0]
                iter += 4
                anri = struct.unpack('>I', data[iter:iter+4])[0]
                iter += 4
                anrin = struct.unpack('>I', data[iter:iter+4])[0]
                iter += 4
                anel = struct.unpack('>I', data[iter:iter+4])[0]
                iter += 4
                anml = struct.unpack('>I', data[iter:iter+4])[0]
                iter += 4
                an_item = {'an_name':tmp_name, 'an_type': antype, 'an_class': anclass, 'an_cache': ancache, 'an_ttl': anttl, 'an_len': anlen, 'an_prins': anpns, 'an_respmail': anram, 'an_sn': ansn, 'an_refint': anri, 'an_retint': anrin, 'an_exlim': anel, 'an_mimttl':anml}
                self.an.append(an_item)


        self.ns=[]; tmp_name=''
        for i in range(0, self.nscount):
            (tmp_name, iter)=self.get_name(data, iter)

            nstype = struct.unpack('>H', data[iter:iter+2])[0]
            iter += 2
            if nstype == 1:
                nsclass = struct.unpack('>H', data[iter:iter+2])[0]
                iter += 2
                nsttl =  struct.unpack('>I', data[iter:iter+4])[0]
                iter += 4
                nslen = struct.unpack('>H', data[iter:iter+2])[0]
                iter += 2
                add1 =struct.unpack('B', data[iter])[0]
                add2 =struct.unpack('B', data[iter+1])[0]
                add3 =struct.unpack('B', data[iter+2])[0]
                add4 =struct.unpack('B', data[iter+3])[0]
                iter += 4
                rdata = str(add1) + '.' + str(add2) + '.' + str(add3) + '.' + str(add4)
                ns_item = {'ns_name': tmp_name, 'ns_type': nstype, 'ns_class': nsclass, 'ns_ttl': nsttl, 'ns_len': nslen, 'ns_rdata': rdata}
                self.ns.append(ns_item)
            elif nstype == 2:
                nsclass = struct.unpack('>H', data[iter:iter+2])[0]
                iter += 2
                nsttl =  struct.unpack('>I', data[iter:iter+4])[0]
                iter += 4
                nslen = struct.unpack('>H', data[iter:iter+2])[0]
                iter += 2
                (rdata, iter)=self.get_name(data, iter)
                ns_item = {'ns_name': tmp_name, 'ns_type': nstype, 'ns_class': nsclass, 'ns_ttl': nsttl, 'ns_len': nslen, 'ns_rdata': rdata}
                self.ns.append(ns_item)
            elif nstype == 6:
                nsclass = struct.unpack('>H', data[iter:iter+2])[0]
                nsclass &= 0x7fff
                nscache &= 0x8000
                iter += 2
                nsttl = struct.unpack('>I', data[iter:iter+4])[0]
                iter += 4
                nslen = struct.unpack('>H', data[iter:iter+2])[0]
                iter += 2
                (nspns, iter)=self.get_name(data, iter)
                (nsram, iter)=self.get_name(data, iter)
                nssn =  struct.unpack('>I', data[iter:iter+4])[0]
                iter += 4
                nsri = struct.unpack('>I', data[iter:iter+4])[0]
                iter += 4
                nsrin = struct.unpack('>I', data[iter:iter+4])[0]
                iter += 4
                nsel = struct.unpack('>I', data[iter:iter+4])[0]
                iter += 4
                nsml = struct.unpack('>I', data[iter:iter+4])[0]
                iter += 4
                ns_item = {'ns_name':tmp_name, 'ns_type': nstype, 'ns_class': nsclass, 'ns_cache': nscache, 'ns_ttl': nsttl, 'ns_len': anlen, 'ns_prins': nspns, 'ns_respmail': nsram, 'ns_sn': nssn, 'ns_refint': nsri, 'ns_retint': nsrin, 'ns_exlim': nsel, 'ns_mimttl':nsml}
                self.ns.append(ns_item)



    ''' parse query name in DNS format'''
    #
    def get_name(self, data, iter):
        tmp_name=''; added=0
        seglen=struct.unpack('>B', data[iter])[0]
        while seglen != 0:
            if seglen == 192:
                iter += 1
                pos=struct.unpack('>B', data[iter])[0]
                (tmp, num) = self.get_name(data, pos)
                iter += 1
                tmp_name += tmp
                tmp_name += tmp_name[-1]
                seglen=struct.unpack('>B', data[iter])[0]
                iter -= 1
            else:
                tmp_name += data[iter+1:iter+seglen+1] + '.'
                iter=iter+seglen+1
                added += seglen+1
                seglen=struct.unpack('>B', data[iter])[0]

        tmp_name=tmp_name[0:-1]
        return (tmp_name, iter)



