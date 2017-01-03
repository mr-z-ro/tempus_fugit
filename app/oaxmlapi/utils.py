#########################################################################################################################################
# format date value into a sensible value
from datetime import datetime


def date_percent_difference(start_date, end_date):
    """
    :param start_date:
    :param end_date:
    :return: dictionary of the form {'percent_days' : percent_days, 'days_consumed' : res_list['days_consumed'],
    'days_remaining' : res_list['days_remaining'], 'days_diff' : res_list['days_diff']}
    """
    res_list = {}

    curr_date = datetime.today()

    if start_date != 'None':
        day, mnth, yr = start_date[:10].split('/')
        starting_date = datetime(year=int(yr), month=int(mnth), day=int(day))

    if end_date != 'None':
        day, mnth, yr = end_date[:10].split('/')
        ending_date = datetime(year=int(yr), month=int(mnth), day=int(day))

    # verify that arguments passed have non-Nones
    if start_date == 'None' and end_date == 'None':
        res_list['days_consumed'] = 0
        res_list['days_diff'] = 0
        res_list['days_remaining'] = 0
    elif start_date == 'None' and end_date != 'None':
        res_list['days_consumed'] = 0
        res_list['days_diff'] = 0
        res_list['days_remaining'] = (ending_date - curr_date).days
    elif start_date != 'None' and end_date == 'None':
        res_list['days_consumed'] = (curr_date - starting_date).days
        res_list['days_diff'] = 0
        res_list['days_remaining'] = 0
    else:
        # compute total days from start to end date
        res_list['days_diff'] = (ending_date - starting_date).days
        res_list['days_consumed'] = (curr_date - starting_date).days
        res_list['days_remaining'] = (ending_date - curr_date).days

    if res_list['days_remaining'] > 0:
        percent_days = res_list['days_consumed'] * 100 / float(res_list['days_diff'])
    else:
        percent_days = 100.00

    return {'percent_days': percent_days, 'days_consumed': res_list['days_consumed'],
            'days_remaining': res_list['days_remaining'], 'days_diff': res_list['days_diff']}