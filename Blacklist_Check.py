import requests,os, argparse, sys
import subprocess
import shlex
import os.path

# Blacklists to check
CONF_BLACKLISTS= ['0spam-killlist.fusionzero.com'
        ,'0spam.fusionzero.com'
        ,'access.redhawk.org'
        ,'all.rbl.jp'
        ,'all.spam-rbl.fr'
        ,'all.spamrats.com'
        ,'aspews.ext.sorbs.net'
        ,'b.barracudacentral.org'
        ,'backscatter.spameatingmonkey.net'
        ,'badnets.spameatingmonkey.net'
        ,'bb.barracudacentral.org'
        ,'bl.drmx.org'
        ,'bl.konstant.no'
        ,'bl.nszones.com'
        ,'bl.spamcannibal.org'
        ,'bl.spameatingmonkey.net'
        ,'bl.spamstinks.com'
        ,'black.junkemailfilter.com'
        ,'blackholes.five-ten-sg.com'
        ,'blacklist.sci.kun.nl'
        ,'blacklist.woody.ch'
        ,'bogons.cymru.com'
        ,'bsb.empty.us'
        ,'bsb.spamlookup.net'
        ,'cart00ney.surriel.com'
        ,'cbl.abuseat.org'
        ,'cbl.anti-spam.org.cn'
        ,'cblless.anti-spam.org.cn'
        ,'cblplus.anti-spam.org.cn'
        ,'cdl.anti-spam.org.cn'
        ,'cidr.bl.mcafee.com'
        ,'combined.rbl.msrbl.net'
        ,'db.wpbl.info'
        ,'dev.null.dk'
        ,'dialups.visi.com'
        ,'dnsbl-0.uceprotect.net'
        ,'dnsbl-1.uceprotect.net'
        ,'dnsbl-2.uceprotect.net'
        ,'dnsbl-3.uceprotect.net'
        ,'dnsbl.anticaptcha.net'
        ,'dnsbl.aspnet.hu'
        ,'dnsbl.inps.de'
        ,'dnsbl.justspam.org'
        ,'dnsbl.kempt.net'
        ,'dnsbl.madavi.de'
        ,'dnsbl.rizon.net'
        ,'dnsbl.rv-soft.info'
        ,'dnsbl.rymsho.ru'
        ,'dnsbl.sorbs.net'
        ,'dnsbl.zapbl.net'
        ,'dnsrbl.swinog.ch'
        ,'dul.pacifier.net'
        ,'dyn.nszones.com'
        ,'dyna.spamrats.com'
        ,'fnrbl.fast.net'
        ,'fresh.spameatingmonkey.net'
        ,'hostkarma.junkemailfilter.com'
        ,'images.rbl.msrbl.net'
        ,'ips.backscatterer.org'
        ,'ix.dnsbl.manitu.net'
        ,'korea.services.net'
        ,'l2.bbfh.ext.sorbs.net'
        ,'l3.bbfh.ext.sorbs.net'
        ,'l4.bbfh.ext.sorbs.net'
        ,'list.bbfh.org'
        ,'list.blogspambl.com'
        ,'mail-abuse.blacklist.jippg.org'
        ,'netbl.spameatingmonkey.net'
        ,'netscan.rbl.blockedservers.com'
        ,'no-more-funn.moensted.dk'
        ,'noptr.spamrats.com'
        ,'orvedb.aupads.org'
        ,'pbl.spamhaus.org'
        ,'phishing.rbl.msrbl.net'
        ,'pofon.foobar.hu'
        ,'psbl.surriel.com'
        ,'rbl.abuse.ro'
        ,'rbl.blockedservers.com'
        ,'rbl.dns-servicios.com'
        ,'rbl.efnet.org'
        ,'rbl.efnetrbl.org'
        ,'rbl.iprange.net'
        ,'rbl.schulte.org'
        ,'rbl.talkactive.net'
        ,'rbl2.triumf.ca'
        ,'rsbl.aupads.org'
        ,'sbl-xbl.spamhaus.org'
        ,'sbl.nszones.com'
        ,'sbl.spamhaus.org'
        ,'short.rbl.jp'
        ,'spam.dnsbl.anonmails.de'
        ,'spam.pedantic.org'
        ,'spam.rbl.blockedservers.com'
        ,'spam.rbl.msrbl.net'
        ,'spam.spamrats.com'
        ,'spamrbl.imp.ch'
        ,'spamsources.fabel.dk'
        ,'st.technovision.dk'
        ,'tor.dan.me.uk'
        ,'tor.dnsbl.sectoor.de'
        ,'tor.efnet.org'
        ,'torexit.dan.me.uk'
        ,'truncate.gbudb.net'
        ,'ubl.unsubscore.com'
        ,'uribl.spameatingmonkey.net'
        ,'urired.spameatingmonkey.net'
        ,'virbl.dnsbl.bit.nl'
        ,'virus.rbl.jp'
        ,'virus.rbl.msrbl.net'
        ,'vote.drbl.caravan.ru'
        ,'vote.drbl.gremlin.ru'
        ,'web.rbl.msrbl.net'
        ,'work.drbl.caravan.ru'
        ,'work.drbl.gremlin.ru'
        ,'wormrbl.imp.ch'
        ,'xbl.spamhaus.org'
        ,'zen.spamhaus.org']

def digip(ip,revip,outf):
    m=0
    for i in range(len(CONF_BLACKLISTS)):
        if m<CONF_BLACKLISTS[i]:
            newip = revip + '.' + CONF_BLACKLISTS[i]
            cmd='dig +short ' + newip
            proc=subprocess.Popen(shlex.split(cmd),stdout=subprocess.PIPE)
            out,err=proc.communicate()
            if '127.0.0' in out:
                bl = ip + ' Blacklisted on' + CONF_BLACKLISTS[i]
                print bl
                write_file(bl,outf)

def read_file(infile,outfile):
    bol = os.path.isfile(outfile)

    if bol == 'True':
        os.remove(outfile)
        file = open(infile, 'r')
        while 1:
            line = file.readline()
            line = line.strip()
            if not line: break
            reverse(line,outfile)
        file.close()
    else:
        file = open(infile, 'r')
        while 1:
            line = file.readline()
            line = line.strip()
            if not line: break
            reverse(line,outfile)
        file.close()

def write_file(result,destf):
    f = open(destf,'ab')
    f.write(result + '\n')
    f.close()

def reverse(oip, outpf):
    if len(oip) <= 1:
        return oip
    else:
        l = oip.split('.')
        invip = '.'.join(l[::-1])
        digip(oip,invip, outpf)

def main():
    opt=argparse.ArgumentParser(description="Checking for blacklisted IPs from various sites")
    opt.add_argument("input",help="Get IPs from file")
    opt.add_argument("output", help="Output results to (filename.txt)")
    
    if len(sys.argv)<=2:
        opt.print_help()
        sys.exit(1)
    
    options= opt.parse_args()
    read_file(options.input, options.output)
    
#print CONF_BLACKLISTS[2]

if __name__ == '__main__':
    main()