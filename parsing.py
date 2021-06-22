import re


class ExosParse:
    def __init__(self, data):
        self.data = data.split('\n')

    def hostname(self):
        p = re.compile('sysName')
        for i in self.data:
            m = p.search(i)
            if m:
                tmp = i.split(' ')
                hostname = tmp[-1].replace('\"', '')
                return hostname
        hostname = 'unknown'
        return hostname

    def dev_model(self):
        p = re.compile('System Type:')
        for i in self.data:
            m = p.search(i)
            if m:
                i = ' '.join(i.split())
                tmp = i.split(':')
                dev_model = tmp[-1].strip()
                if dev_model:
                    return dev_model
        dev_model = 'unknown'
        return dev_model

    def os_ver(self):
        p = re.compile('ExtremeXOS version')
        for i in self.data:
            m = p.search(i)
            if m:
                i = ' '.join(i.split())
                tmp = i.split(' ')
                if tmp:
                    version = tmp[-1].strip()
                    return version
        version = 'unknown'
        return version

    def uptime(self):
        p = re.compile('System UpTime:')
        for i in self.data:
            m = p.search(i)
            if m:
                i = ' '.join(i.split())
                tmp = i.split(':')
                uptime = tmp[-1].strip()
                return uptime
        uptime = 'unknown'
        return uptime

    def cpu_usage(self):
        p = re.compile('System\s+([0-9]+[.][0-9]+\s)+')
        for i in self.data:
            m = p.search(i)
            if m:
                i = ' '.join(i.split())
                tmp = i.split(' ')
                idle = int(100 - float(tmp[7]))
                cpu_idle = str(idle) + ' %'
                return cpu_idle
        cpu_idle = 'unknown'
        return cpu_idle

    def mem_usage(self):
        meminfo = list()
        p = re.compile('KB')
        for i in self.data:
            m = p.search(i)
            if m:
                tmp = i.split(':')
                if len(tmp) == 2:
                    meminfo.append(tmp[1].strip())
        if meminfo:
            # print(meminfo)
            mem_free = int(int(meminfo[3]) / int(meminfo[0]) * 100)
            return str(mem_free) + ' %'
        else:
            mem_free = 'unknown'
            return mem_free

    def fan(self):
        """
        Slot-1 FanTray-1 information:
         State:                  Operational
         NumFan:                 2
         PartInfo:               1451N-42780 450300-00-03
         Revision:               3.0
         Fan-1:                  Operational at 3120 RPM
         Fan-2:                  Operational at 6960 RPM

        Slot-1 FanTray-2 information:
         State:                  Operational
         NumFan:                 2
         PartInfo:               1451N-42779 450300-00-03
         Revision:               3.0
         Fan-1:                  Operational at 3240 RPM
         Fan-2:                  Operational at 7020 RPM

        Slot-1 FanTray-3 information:
         State:                  Operational
         NumFan:                 2
         PartInfo:               1451N-42776 450300-00-03
         Revision:               3.0
         Fan-1:                  Operational at 3180 RPM
         Fan-2:                  Operational at 6420 RPM

                :return:
        """
        p = re.compile('Fan-[0-9]+:')
        num_fan = 0
        ok = True
        fan_state = str()

        for i in self.data:
            m = p.search(i)
            if m:
                i = ' '.join(i.split())
                tmp1 = i.split(':')
                tmp2 = tmp1[-1].strip().split(' ')
                if tmp2[0].strip() != 'Operational':
                    ok = False
                    fan_state = f'{tmp1[0], tmp2[0]}'
                    return fan_state
                num_fan += 1
        if ok and num_fan:
            fan_state = f'ALL({num_fan}) is Operational'
            return fan_state
        else:
            return 'unknown'

    def temperature(self):
        """
        Field Replaceable Units               Temp (C)   Status   Min  Normal   Max
        ---------------------------------------------------------------------------
        Switch         : X440-24p               22.50    Normal   -10    0-48  55


        Field Replaceable Units               Temp (C)   Status   Min  Normal   Max
        ---------------------------------------------------------------------------
        Slot-1         : G24Xc                  26.50    Normal   -10    0-50  60
        Slot-2         : G24Xc                  25.50    Normal   -10    0-50  60
        Slot-3         :
        Slot-4         :
        Slot-5         : 10G8Xc                 29.50    Normal   -10    0-50  60
        Slot-6         : G48Tc                  27.50    Normal   -10    0-50  60
        MSM-A          : MSM-48c                37.50    Normal   -10    0-50  60
        MSM-B          : MSM-48c                37.50    Normal   -10    0-50  60
        PSUCTRL-1      :                        33.25    Normal   -10    0-50  60
        PSUCTRL-1      :
        PSUCTRL-2      :                        34.55    Normal   -10    0-50  60
        PSUCTRL-2      :
        """
        # only check slot-1 ...
        p = re.compile('^Switch\s+[:]{1}|^Slot-1\s+[:]{1}')
        for i in self.data:
            m = p.search(i)
            if m:
                i = ' '.join(i.split())
                tmp = i.split(' ')
                temperature = tmp[3]
                status = tmp[4]
                return f'{temperature} ℃, {status}'
        return 'unknown'

    def power_supply(self):
        """# show power
                             PSU-1 or  PSU-2 or
                             Internal  External  External  External  Power
        Slots  Type          PSU       PSU       PSU       PSU       Usage
        -------------------------------------------------------------------
        Slot-1 X440-24p        P         -         -         -         N/A
        Slot-2 X440-24p        P         -         -         -         N/A
        Slot-3
        Slot-4
        Slot-5
        Slot-6
        Slot-7
        Slot-8


        Flags : (P) Power available, (F) Failed or no power,
                (O) 48V powered off when 2 or 3 external PSUs are powered on,
                (-) Empty


        # show power

        PowerSupply 1 information:
         State             : Powered On
         PartInfo          : Internal PSU-1 1452W-80410 800462-00-06
         Output 1          : 12.06 V,  0.00 A   (12V/550W Max)

        PowerSupply 2 information:
         State             : Powered On
         PartInfo          : Internal PSU-2 1741W-80773 800462-00-07
         Output 1          : 11.98 V,  2.25 A   (12V/550W Max)
         Power Usage       : 41.46 W

        System Power Usage : 41.46 W
         Poll Interval     : 60 s
         Change Threshold  : N/A
         Change Action     : N/A

        """
        status = str()
        num_ps = 0
        p1 = re.compile('State\s+:')
        p2 = re.compile('^Slot-[0-9]+\s{1}[A-Z0-9]+[PFO-]{1}')

        # use stand alone.
        for i in self.data:
            m1 = p1.search(i)
            if m1:
                i = ' '.join(i.split())
                tmp = i.split(':')
                status = tmp[1].strip()
                if status == 'Powered On':
                    num_ps += 1
                    pwr = status
                else:
                    if status == 'Empty':
                        pass
                    else:
                        pwr = status
                        return pwr

        if num_ps and status:
            return f'ALL({num_ps}) is {pwr}'

        # use stack config.
        for i in self.data:
            m2 = p2.search(i)
            if m2:
                i = ' '.join(i.split())
                tmp = i.split(' ')
                status = tmp[2].strip()
                if status != 'P':
                    return status
                else:
                    num_ps += 1

        if num_ps and status:
            return f'ALL({num_ps}) is {status}'

        return 'unknown'


if __name__ == '__main__':
    data = """
SysName:          Cheonsong_3F_L1
SysLocation:      
SysContact:       support@extremenetworks.com, +1 888 257 3000
System MAC:       02:04:96:7D:FB:4A
System Type:      X440-24p (Stack)

SysHealth check:  Enabled (Normal)
Recovery Mode:    All
System Watchdog:  Enabled

Current Time:     Mon Jun 14 11:32:11 2021
Timezone:         [Auto DST Disabled] GMT Offset: 540 minutes, name is KST.
Boot Time:        Sun Feb 21 17:38:39 2021
Boot Count:       9
Next Reboot:      None scheduled
System UpTime:    112 days 17 hours 53 minutes 32 seconds 

Slot:             Slot-1 *                     Slot-2                  
                  ------------------------     ------------------------
Current State:    MASTER                       BACKUP (In Sync)        

Image Selected:   primary                      secondary               
Image Booted:     primary                      secondary               
Primary ver:      16.2.5.4                     16.2.5.4                
                  patch1-7
Secondary ver:    16.2.5.4                     16.2.5.4                
                                               patch1-7

Config Selected:  primary.cfg                                          
Config Booted:    primary.cfg                                          

primary.cfg       Created by ExtremeXOS version 16.2.5.4
                  278217 bytes saved on Thu Apr  8 16:45:22 2021    
    
                     PSU-1 or  PSU-2 or
                     Internal  External  External  External  Power
Slots  Type          PSU       PSU       PSU       PSU       Usage
-------------------------------------------------------------------
Slot-1 X440-24p        P         -         -         -         N/A
Slot-2 X440-24p        P         -         -         -         N/A
Slot-3 
Slot-4 
Slot-5 
Slot-6 
Slot-7 
Slot-8 


Flags : (P) Power available, (F) Failed or no power,
        (O) 48V powered off when 2 or 3 external PSUs are powered on,
        (-) Empty


FanTray-1 information:
 State:                  Operational
 NumFan:                 4
 Fan-1:                  Operational at 11000 RPM
 Fan-2:                  Operational at 11000 RPM
 Fan-3:                  Operational at 11000 RPM
 Fan-4:                  Operational at 11000 RPM

FanTray-2 information:
 State:                  Operational
 NumFan:                 4
 Fan-1:                  Operational at 11000 RPM
 Fan-2:                  Operational at 11000 RPM
 Fan-3:                  Operational at 11000 RPM
 Fan-4:                  Operational at 11000 RPM

FanTray-3 information:
 State:                  Empty

FanTray-4 information:
 State:                  Empty

FanTray-5 information:
 State:                  Empty

FanTray-6 information:
 State:                  Empty

FanTray-7 information:
 State:                  Empty

FanTray-8 information:
 State:                  Empty

Field Replaceable Units               Temp (C)   Status   Min  Normal   Max
---------------------------------------------------------------------------
Slot-1         : X440-24p               38.50    Normal   -10    0-48  55
Slot-2         : X440-24p               40.00    Normal   -10    0-48  55
Slot-3         : 
Slot-4         : 
Slot-5         : 
Slot-6         : 
Slot-7         : 
Slot-8         : 


System Memory Information
-------------------------
 Slot-1    Total DRAM (KB): 524288
 Slot-1    System     (KB): 19076
 Slot-1    User       (KB): 213024
 Slot-1    Free       (KB): 292188
 Slot-2    Total DRAM (KB): 524288
 Slot-2    System     (KB): 19076
 Slot-2    User       (KB): 203912
 Slot-2    Free       (KB): 301300

Memory Utilization Statistics
-----------------------------

 Card Slot Process Name     Memory (KB)
---------------------------------------
 Slot-1 1   aaa              2009            
 Slot-1 1   acl              1309            
 Slot-1 1   bfd              645             
 Slot-1 1   bgp              0               
 Slot-1 1   brm              0               
 Slot-1 1   ces              0               
 Slot-1 1   cfgmgr           1531            


SysName:          Baekwoon_3F_1
SysLocation:      
SysContact:       support@extremenetworks.com, +1 888 257 3000
System MAC:       02:04:96:6D:5A:9A
System Type:      X440-24p (Stack)

SysHealth check:  Enabled (Normal)
Recovery Mode:    All
System Watchdog:  Enabled

Current Time:     Fri Jun 11 17:52:17 2021
Timezone:         [Auto DST Disabled] GMT Offset: 540 minutes, name is KST.
Boot Time:        Sun Feb 21 17:39:29 2021
Boot Count:       67
Next Reboot:      None scheduled
System UpTime:    110 days 12 minutes 47 seconds 

Slot:             Slot-1 *                     Slot-2                  
                  ------------------------     ------------------------
Current State:    MASTER                       BACKUP (In Sync)        

Image Selected:   secondary                    primary                 
Image Booted:     secondary                    primary                 
Primary ver:      16.2.5.4                     16.2.5.4                
                                               patch1-7
Secondary ver:    16.2.5.4                     16.2.2.4                
                  patch1-7

Config Selected:  primary.cfg                                          
Config Booted:    primary.cfg                                          

primary.cfg       Created by ExtremeXOS version 16.2.5.4
                  278279 bytes saved on Thu Apr  8 16:40:26 2021


      CPU Utilization Statistics - Monitored every 5 seconds
-------------------------------------------------------------------------------

Card   Process      5    10   30   1    5    30   1    Max           Total
                    secs secs secs min  mins mins hour            User/System
                    util util util util util util util util       CPU Usage
                    (%)  (%)  (%)  (%)   (%)  (%)  (%)  (%)         (secs)
-------------------------------------------------------------------------------

Slot-1 System        4.4  3.8  4.4  4.2  4.6  4.1  4.0 53.3  1269.94   771656.76
Slot-2 System        5.2  4.6  4.2  4.5  4.6  4.3  4.3 99.9     0.00       0.00 
Slot-1 aaa           0.0  0.0  0.1  0.2  0.2  0.1  0.1  7.7 13255.93   29100.39 
Slot-1 acl           0.0  0.0  0.0  0.1  0.1  0.1  0.1  5.0  7404.23   15810.16 
Slot-1 bfd           0.0  0.1  0.0  0.1  0.1  0.1  0.1  1.8  4144.55    5450.54 
Slot-1 bgp           0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0     0.00       0.00 
Slot-1 brm           0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0     0.00       0.00 
Slot-1 ces           0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0     0.00       0.00 
Slot-1 cfgmgr        0.0  0.0  0.1  0.0  0.1  0.0  0.0  4.5   509.47     218.12 
Slot-1 cli           0.7  0.3  1.3  0.6 10.5  3.7  1.8 46.4   656.60     178.68 
Slot-1 devmgr        0.0  0.0  0.0  0.0  0.0  0.0  0.0 46.4   502.05     120.57 
Slot-1 dirser        0.0  0.0  0.0  0.1  0.0  0.0  0.0  4.2     1.04       2.58 
Slot-1 dosprotect    0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.6     0.45       0.18 
Slot-1 dot1ag        0.0  0.0  0.0  0.0  0.0  0.0  0.0  2.4    27.42      55.57 


"""
    test = ExosParse(data)
    print(test.power_supply())