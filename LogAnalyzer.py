#!/usr/bin/python3.6

import re
import requests
import time
import datetime


hosts_dict=dict()
return_dict =dict()
time_scale = dict()
hour_byte = dict()
hour_request = dict()
get_distribution = dict ()

def get_file_from_url(url):
    """
    This method gets the file and opens in a file_pointer
    :param url: url of the file to be downloaded
    :return: None
    """
    ret = requests.get(url)
    status = ret.status_code
    if status >=200 and status <300:
        file_content = ret.text
        return file_content


def clean_lines(lines):
    """
    This method removes intial and end double quotes
    :param lines: List of lines
    :return: cleaned_lines
    """
    cleaned_lines = []
    for line in lines:
        if line[0] == '"':
            cleaned_lines.append(line[1:-1])
        else:
            cleaned_lines.append(line)
    return cleaned_lines


def extract_contents_from_line(line):
    pattern = r"^(?P<IP>\d{1,3}.\d{1,3}.\d{1,3}..\d{1,3}) (?P<Second>-|\S) (?P<user>-|\S+) \[(?P<time>\S+) \S+\] [\"]" \
              r"(?P<reqest>\S+) (?P<endpath>\S+) (?P<proto>\S+)[\"] (?P<status>\d+) (?P<size>\d+) [\"](?P<host>\S+)" \
              r"[\"] [\"](?P<browser>.*?)[\"]"
    match = re.search(pattern, line)
    try:
        matching_dict = match.groupdict()
        if len(matching_dict):
            return matching_dict
        else:
            print(line)
            exit()
    except Exception as e:
        #print(line)
        return False


def process_status_kind(line_dict):
    """
    This method shall process statuses kind
    :param line_dict:
    :return:
    """
    return_code = line_dict['status']
    if return_code in return_dict.keys():
        return_dict[return_code]+=1
        return
    else:
        return_dict[return_code]=1
        return


def update_time_scale(time_in_sec):
    """
    This method shall split the log time to 60 min slots and assigns a lable
    :param time_in_sec:
    :return label: lable for the time slot
    """
    if time_scale.keys():
        for time_slot in sorted(time_scale.keys()):
            if time_in_sec >= time_scale[time_slot]['start'] and time_in_sec < time_scale[time_slot]['end']:
                return time_slot
        time_scale[time_slot+1] ={}
        time_scale[time_slot+1]['start'] = time_in_sec
        time_scale[time_slot+1]['end'] = time_in_sec + 3600
        return time_slot+1

    else:
        time_scale[1]={}
        time_scale[1]['start'] =time_in_sec
        time_scale[1]['end']=time_in_sec+3600


def get_epoch_time(timeString):
    """
    This method returns the epoch time for the given time string.
    :param timeString: time string extracted from the log
    :return epoch_time:
    """
    epoch_time = time.mktime(datetime.datetime.strptime(timeString, "%d/%b/%Y:%H:%M:%S").timetuple())
    return epoch_time


def epoch_to_normal(epoch):
    '''
    This method converts epoch time to readable time format
    :param epoch:
    :return:
    '''
    return datetime.datetime.fromtimestamp( epoch )


def process_hosts(line_dict):
    """
    This method shall process hosts
    :param line_dict:
    :return:
    """
    host_name = line_dict['IP']
    if host_name in hosts_dict.keys():
        hosts_dict[host_name]+=1
        return
    else:
        hosts_dict[host_name]=1
        return


def process_time(line_dict):
    time_in_sec = get_epoch_time(line_dict['time'])
    time_hour_lable = update_time_scale(time_in_sec)

    bytes_served = int(line_dict['size'])
    if time_hour_lable in hour_byte.keys():
        hour_byte[time_hour_lable]+=bytes_served
    else:
        hour_byte[time_hour_lable]=bytes_served
    if time_hour_lable in hour_request.keys():
        hour_request[time_hour_lable]+=1
    else:
        hour_request[time_hour_lable]=1
    if time_hour_lable in get_distribution.keys():
        get_distribution[time_hour_lable]+=1
    else:
        get_distribution[time_hour_lable]=1


def sort_dictionary(dictionary):
    """
    This method shall sort dictionary of depth-1 based on value
    :param dictionary: dictionary to be sorted
    :return final: sorted in reverse dictionary
    """
    final = dict(reversed(sorted(dictionary.items(), key=lambda item: item[1])))
    return final


def process_contents_of_line(line_dict):
    """
    This method shall process contents of line to achieve specified results
    :param line_dict: dictionary content
    :return:
    """
    process_hosts(line_dict)


def get_tuples_for_dict(dictionary, number):
    """
    This method returns tuples for the specified dictionary
    :param dictionary:
    :return:
    """
    list_of_tup=[]

    for key in dictionary.keys():
        entry = (key, dictionary[key])
        list_of_tup.append(entry)
        number -=1
        if number==0:
            break
    return list_of_tup


def get_first_element_value(dictionary):
    """
    This method returns the first element from the dictionary
    :param dictionary:
    :return:
    """
    return list(dictionary.keys())[0], dictionary[list(dictionary.keys())[0]]

def get_timeframe_from_timescale(slot):
    start = epoch_to_normal(time_scale[slot]['start'])

    stop = epoch_to_normal(time_scale[slot]['end'])
    return start, stop


read_file = open("C:\\Users\\santop\\PycharmProjects\\PythonAssinment\\AssignmentScripts\\TestFolder\\search_log.log")
#file_content = get_file_from_url("https://raw.githubusercontent.com/ocatak/apache-http-logs/master/w3af.txt")
file_content = read_file.read()
lines = file_content.split('\n')
cleaned_lines = clean_lines(lines)
for line in cleaned_lines:
    content_dict = extract_contents_from_line(line)
    if content_dict:
        process_hosts(content_dict)
        process_status_kind(content_dict)
        process_time(content_dict)

print (" ------ Top 10 Frequent hosts ------- ")
print(get_tuples_for_dict(sort_dictionary(hosts_dict), 10))
print (" ---- Top 10 HTTP Status Codes ------ ")
print(get_tuples_for_dict(sort_dictionary(return_dict), 10))
print(" ---- Hour with highest requests ----- ")
time, reqs = get_first_element_value(sort_dictionary(hour_request))
start_time, end_time = get_timeframe_from_timescale(time)
print( str(reqs)+ ' requests were made between ',  str(start_time), 'and' , str(end_time))
print(" ---- Hour with highest byte served ----- ")
time, bytes = get_first_element_value(sort_dictionary(hour_byte))
start_time, end_time = get_timeframe_from_timescale(time)
print( str(reqs)+ ' bytes were served between ',  str(start_time), 'and' , str(end_time))
#print(sort_dictionary(hour_request))
sorted_distribution = sort_dictionary(get_distribution)
print(" ---- Mean of the Get distributiuon ----- ")
total_requests = sum(get_distribution.values())
total_hours = len(get_distribution)
print(round(total_requests/total_hours))
print(" ----- Mode of distribution ----- ")
time, mode = list(sorted_distribution.keys())[0], get_distribution[list(sorted_distribution.keys())[0]]
start_time, end_time = get_timeframe_from_timescale(time)
print( str(mode)+ ' is the mode of Get distribution observed between ',  str(start_time), 'and' , str(end_time))

#
#print(len(file_content))
