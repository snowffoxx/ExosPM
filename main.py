import datetime
import pprint

from collect import get_hosts_file, exos_task, data_parsing, create_worksheet, report


def main(excel_file, site, role):
    now = datetime.datetime.now()
    print('>>>>>>>>>>>>>>>>>>>>>>>>')
    print(f'Begin proactive maintenamce...Current time: {now}')

    commands = [
        'show switch', 'show fan', 'show temp', 'show power', 'show cpu',
        'show memory', 'show config | inc sysName'
    ]
    hosts = get_hosts_file(excel_file)
    result = exos_task(hosts, commands=commands, vendors='extreme', site=site, role=role)
    # pprint.pprint(result)
    chk_list = data_parsing(result)
    # pprint.pprint(chk_list)
    create_worksheet(excel_file)
    report(chk_list, excel_file)

    print('<<<<<<<<<<<<<<<<<<<<<<<<<')
    now = datetime.datetime.now()
    print(f'End proactive maintenance... Current time: {now}')


if __name__ == '__main__':
    excel_file = input('Type excel file: [exos_pm.xlsx] ')
    if not excel_file:
        excel_file = 'exos_pm.xlsx'
    site = input('Type site: [ALL] ')
    if site.upper() == 'ALL':
        site = ''
    role = input('type role: [ALL] ')
    if role.upper() == 'ALL':
        role = ''

    main(excel_file, site, role)

