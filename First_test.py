import re
screen_output = """
vyatta@dut-2:~$ show interfaces
Codes: S - State, L - Link, u - Up, D - Down, A - Admin Down
Interface       IP Address(es)                    S/L  Speed/Duplex  Description
---------       --------------                    ---  ------------  -----------
dp0ce0          -                                 u/D  auto/auto
dp0ce1          -                                 u/D  auto/auto
dp0p7s0         10.156.43.100/24                  u/u  a-1g/a-full   Mgmt Network
dp0xe0          -                                 u/u  10g/full
dp0xe1          -                                 u/u  10g/full
dp0xe11         10.156.21.2/20                    u/u  1g/full
dp0xe12         -                                 A/D  auto/auto     link-to-TimeProvider4100-eth4
dp0xe13         -                                 u/D  auto/auto
lo1             1.1.1.1/32                        u/u  -/-
sw0             -                                 u/u  -/-
sw0.50          10.0.0.2/30                       u/u  -/-
sw0.100         192.168.4.1/24                    u/D  -/-
sw0.1001        100.100.0.1/24                    u/u  -/-
                100:100::1/64
sw0.1002        192.168.1.2/30                    u/u  -/-
                192.168.2.2/30
                cef:0:4:3:2:1:0:4/128
sw0.1026        100.100.8.1/24                    u/u  -/-
                100:100:8::1/64
sw0.4004        4.4.0.1/24                        u/D  -/-
"""

def read_data(screen_output):
    lines=screen_output.split("\n")
    #extract=re.compile(r"././")
    list_of_dicts=[]
    dict={}
    for idx,line in enumerate(lines[5:-1]):
        #print(line[0:8].strip(" "))
        n=list(re.split(r'\s+',line))
        list_of_dicts.append({"Interface":line[0:8].strip(" ")})
        if line[0:8] == '':
            list_of_dicts[idx-1].append({"IP Adress(es)":n[1]})
        try:
            list_of_dicts[idx].update({"IP Adress(es)":n[1]})
        except:
            list_of_dicts[idx].update({"IP Adress(es)":' '}) 
        try:
            list_of_dicts[idx].update({"S/L":n[2]})
        except:
            list_of_dicts[idx].update({"S/L":''})
        try:
            list_of_dicts[idx].update({"Speed/Duplex":n[3]})
        except:
            list_of_dicts[idx].update({"Speed/Duplex":''})
            #v=re.search(r'[ADu]{1}\/[ADu]{1}',line)
            #b=re.match(r'\S*\/*',line)
            #n=re.split(r'\s+',line)
        
    #print(list_of_dicts)
    return list_of_dicts

def list_check(screen_output):
    list_of_dicts=read_data(screen_output)
    c=0
    for d in list_of_dicts:
        if d['Interface']=='':
            c+=1
        else:
            pass
    return c


def test_function():
    assert len(read_data(screen_output)) == 20

def test_function_2():
    c = list_check(screen_output)
    assert c == 4