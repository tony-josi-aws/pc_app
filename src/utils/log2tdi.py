#
# FreeRTOS-tdlogger
# Copyright (C) 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# https://www.FreeRTOS.org
# https://github.com/FreeRTOS
#

import argparse

last_timestamp = None
tdi_timestamp = 0
occ_id = {}
task_id = {}
irq_id = {}
kernel_object_id = {}
global_id = 1
in_isr = False
events = []

def parse_arguments():
    parser = argparse.ArgumentParser(description='Raw Logs to TDI format converter.')
    parser.add_argument('-l', '--log-file', required=True, help='Raw log file.')
    parser.add_argument('-t', '--tdi-file', required=False, help='Output TDI file.')
    return parser.parse_args()


def parse_time(bytes):
    global last_timestamp
    global tdi_timestamp
    global global_id

    timestamp = int.from_bytes(bytes, 'big')
    if last_timestamp is None:
        last_timestamp = timestamp

    if timestamp >= last_timestamp:
        tdi_timestamp += ( timestamp - last_timestamp )
    else:
        if 0 not in occ_id:
            occ_id[0] = global_id
            global_id += 1
            events.append(f'NAM 7 {occ_id[0]} TimeWrap')
        events.append(f'OCC 7 {occ_id[0]} {tdi_timestamp}')
        tdi_timestamp = 0xffffffff - last_timestamp + timestamp
    last_timestamp = timestamp


def parse_cmd_type_id(bytes):
    cmd_type_id = int.from_bytes(bytes, 'big')
    cmd = (cmd_type_id & 0xff000000) >> 24
    type = (cmd_type_id & 0x00ff0000) >> 16
    id = (cmd_type_id & 0x0000ffff)
    return cmd, type, id


def parse_task_event(cmd, type, id, event_bytes):
    global global_id

    task_name = event_bytes.decode('utf-8')
    if id not in task_id:
        task_id[id] = global_id
        global_id += 1
        events.append(f'NAM 0 {task_id[id]} {task_name}')

    if cmd == 0x01: # start
        events.append(f'STA {type} {task_id[id]} {tdi_timestamp}')
    if cmd == 0x00: # stop
        events.append(f'STO {type} {task_id[id]} {tdi_timestamp}')
    if cmd == 0x03: # create
        pass
    if cmd == 0x04: # delete
        pass


def parse_isr_event(cmd, type, id, event_bytes):
    global global_id

    irq_name = event_bytes.decode('utf-8')
    if id not in irq_id:
        irq_id[id] = global_id
        global_id += 1
        events.append(f'NAM 1 {irq_id[id]} {irq_name}')

    if cmd == 0x01: # start
        events.append(f'STA {type} {irq_id[id]} {tdi_timestamp}')
        if in_isr == True:
            events.append('DSC 3 0 0')
        else:
            in_isr = True
    if cmd == 0x00: # stop
        events.append(f'STO {type} {irq_id[id]} {tdi_timestamp}')
        in_isr = False


def parse_kernel_object_event(cmd, type, id):
    global global_id

    if id not in kernel_object_id:
        kernel_object_id[id] = global_id
        global_id += 1

    if cmd == 0x01: # Acquire or send
        events.append(f'STA {type} {kernel_object_id[id]} {tdi_timestamp}')
    if cmd == 0x00: # # Release or receive
        events.append(f'STO {type} {kernel_object_id[id]} {tdi_timestamp}')


def parse_raw_logs(log_file):
    with open(log_file, 'br') as f:
        while True:
            # Timestamp.
            data = f.read(4)
            if not data:
                break
            parse_time(data)
            # Command, type and id.
            data = f.read(4)
            cmd, type, id = parse_cmd_type_id(data)
            event_bytes = f.read(4)
            if type == 0: # task
                parse_task_event(cmd, type, id, event_bytes)
            elif type == 1: # isr
                parse_isr_event(cmd, type, id, event_bytes)
            elif type >= 2 and type <= 4: # semaphore, msg queue, event
                parse_kernel_object_event(cmd, type, id)


def generate_tdi_file(tdi_file):
    with open(tdi_file, 'w') as f:
        print('CPU trace', file=f)
        print('SPEED 68000000', file=f)
        print('MEMSPEED 120000000', file=f)
        print('TIME 68000000', file=f)

        for event in events:
            print(event, file=f)

        print('END', file=f)


def convert_raw_logs_to_tdi(raw_log_file, output_tdi_file):
    parse_raw_logs(raw_log_file)
    generate_tdi_file(output_tdi_file)


def main():
    args = parse_arguments()
    log_file = args.log_file
    if args.tdi_file is None:
        tdi_file = log_file + '.tdi'
    else:
        tdi_file = args.tdi_file
    convert_raw_logs_to_tdi(log_file, tdi_file)


if __name__ == '__main__':
    main()