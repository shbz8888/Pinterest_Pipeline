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
    list_of_dicts=[]
    dict={}
    for idx,line in enumerate(lines[5:-1]):
        n=list(re.split(r'\s+',line))
        list_of_dicts.append({"Interface":line[0:8].strip(" ")})
        if line[0:8] == '        ' and list_of_dicts[idx-1]["Interface"] != '' : 
            list_of_dicts[idx-1]["IP Adress(es)"]+= ', '+n[1]   #Appends interface value to previous dictionary
        elif line[0:8] == '        ' and list_of_dicts[idx-1]["Interface"] == '':
            list_of_dicts[idx-2]["IP Adress(es)"]+= ', '+n[1]   #Appends interface value to dictionary two places behind
        try:
            list_of_dicts[idx].update({"IP Adress(es)":n[1]})   #Trys to add a value to the dictionary
        except:
            list_of_dicts[idx].update({"IP Adress(es)":' '})    #If it doesn't exist a blank space is added
        try:
            list_of_dicts[idx].update({"S/L":n[2]})
        except:
            list_of_dicts[idx].update({"S/L":''})
        try:
            list_of_dicts[idx].update({"Speed/Duplex":n[3]})
        except:
            list_of_dicts[idx].update({"Speed/Duplex":''})
    Final_list = [x for x in list_of_dicts if not ('' == x.get('Interface'))]    
    return list_of_dicts,Final_list



def list_check(screen_output):  #Will be used in tests below
    Initial_list, Final_list=read_data(screen_output)
    for d in Final_list:
        if d['Interface']=='':
            return True
    return False  


def test_regex():    #Checks that the regex statement has cut the lines correctly
    list_of_dicts, Final_list=read_data(screen_output)
    assert len(list_of_dicts) == 20

def test_list():  #Checks if the final list contains any dictionaries with empty values
    assert list_check(screen_output) == False
    assert any(d['Interface'] not in [''] for d in list_of_dicts) == True

def test_dictionary_formation():    #Checks the dictionaries formed properly
    list_of_dicts, Final_list=read_data(screen_output)
    assert any(d['S/L'] in ['u/D', 'u/u', 'A/D'] for d in list_of_dicts) == True

list_of_dicts, Final_list=read_data(screen_output)
print(Final_list)


    
