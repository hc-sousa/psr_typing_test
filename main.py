#!/usr/bin/env python3

import argparse
import random
import string
from time import time, ctime
from readchar import readchar
from pprint import pprint
from collections import namedtuple
from colorama import Fore, Style

def getArgs(args):
    return args['use_time_mode'], args['max_value']

def main():
    ### define and read arguments
    parser = argparse.ArgumentParser(description='Definition of test mode')
    parser.add_argument('-utm', '--use_time_mode',
        action=argparse.BooleanOptionalAction,
        default=False,
        help='Max number of secs for time mode or maximum number of inputs for number of inputs mode.')
    parser.add_argument('-mv', '--max_value',
        type=int, required=True,
        help='Max number of seconds for time mode or maximum number of inputs for number of inputs mode.')

    args = vars(parser.parse_args())
    print(args)
    use_time_mode, max_value = getArgs(args)

    ### data structures
    alphabet = list(string.ascii_lowercase)
    
    Input = namedtuple('Input', ['requested', 'received', "duration"])

    stats = {
        'accuracy': 0.0,
        'inputs': [],
        'number_of_hits': 0,
        'number_of_types': 0,
        'test_duration': 0.0,
        'test_end': '',
        'test_start': '',
        'type_average_duration': 0.0,
        'type_hit_average_duration': 0.0,
        'type_miss_average_duration': 0.0
    }

    print(f"Test running up to {max_value} {'seconds' if use_time_mode else 'inputs'}.")
    ### wait for user confirmation to start test
    print("Press any key to start the test")
    readchar()   # readchar waits for a character to be read, blocking if there are none
    
    start_ts = time()
    stats['test_start'] = ctime(start_ts)

    ### start the test
    while True:
        input_start_ts = time()
        # request letter
        expected = random.choice(alphabet)
        print(f"Type letter '{Fore.BLUE}{expected}{Style.RESET_ALL}'")

        # read input
        received = readchar().lower()
        if received == " ": #stop the game if the user presses the space bar
            break
        print(f"You typed letter {Fore.GREEN if received == expected else Fore.RED}{received}{Style.RESET_ALL}")
            
        stats['inputs'].append(Input(requested = expected, received = received, duration = time() - input_start_ts))

        if use_time_mode:
            if max_value <= time() - start_ts:
                print(f"Current test duration ({time()-start_ts}) exceeds maximum of {max_value}")
                break
        else:
            if len(stats['inputs']) >= max_value:
                print(f"Reached maximum number of inputs ({max_value})")
                break

    print(f"{Fore.BLUE}Test Finished!{Style.RESET_ALL}\n")

    ### calculate final stats
    test_end_ts = time()
    stats['test_duration'] = test_end_ts - start_ts
    stats['test_end'] = ctime(test_end_ts)
    stats['number_of_types'] = len(stats['inputs'])

    total_type_duration = 0
    total_hit_duration = 0
    total_miss_duration = 0

    for value in stats['inputs']:
        total_type_duration += value.duration
        if value.received == value.requested:
            stats['number_of_hits'] += 1
            total_hit_duration += value.duration
        else:
            total_miss_duration += value.duration
            
    stats["type_hit_average_duration"] = total_hit_duration / stats['number_of_hits'] \
        if stats['number_of_hits'] > 0 else 0.0
    stats["type_miss_average_duration"] =  total_miss_duration / (stats['number_of_types'] - stats['number_of_hits']) \
        if (stats['number_of_types'] - stats['number_of_hits']) > 0 else 0.0
    stats['type_average_duration'] = total_type_duration / stats['number_of_types']
    stats['accuracy'] = stats['number_of_hits'] / stats['number_of_types'] * 100

    ### print stats
    pprint(stats)


if __name__ == "__main__":
    main()
