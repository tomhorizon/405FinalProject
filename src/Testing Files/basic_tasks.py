"""!
@file basic_tasks.py
    This program runs 2 tasks that communicate with an accelerometer using I2C
    communication. Task 1 reads, scales, and places the acceleromters X-axis data
    into a qeue, and Task 2 prints it. The accelerometer information is read every
    1/2 second. This file is a modified version of Dr. JR Ridgely's provided example code

@author JR Ridgely
@author Dylan Weiglein
@author Tom Taylor
@author Jonathan Fraser 
@date   2021-Dec-15 JRR Created from the remains of previous example
@date   2023-Feb-17 Dylan, Tom, Jonathan updated to run I2C w/ accelerometer
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share
import time
import mma845x
from pyb import I2C

def task1(shares):
    """!
    Task which puts things into a share and a queue.
    @param shares A list holding the share and queue used by this task
    """
    # Get references to the share and queue which have been passed to this task
    # Initialize accelerometer object (I2C)
    accel_q = shares
    accel1 = mma845x.MMA845x(pyb.I2C(1, pyb.I2C.MASTER, baudrate = 100000), 29)
    accel1.standby()
    # read accel
    while True:
        accel1.active()
        read_accel = accel1.get_ax()
        accel1.standby()
        accel_q.put(read_accel)
        yield 0


def task2(shares):
    """!
    Task which takes things out of a queue and share and displays them.
    @param shares A tuple of a share and queue from which this task gets data
    """
    # Get references to the share and queue which have been passed to this task
    accel_display = shares
    

    while True:
        # Show everything currently in the queue and the value in the share
        print(accel_display.get())
        
        yield 0


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    
    acQ = task_share.Queue('f', 1000, thread_protect=False, overwrite=True, name='x_accel')
    task_1 = cotask.Task(task1, name = 'get accel',
                         priority = 2, period = 500, profile = True, trace=False, shares=(acQ))
    task_2 = cotask.Task(task2, name = 'print accel',
                         priority = 1, period = 500, profile = True, trace=False, shares=(acQ))
    cotask.task_list.append (task_1)
    cotask.task_list.append (task_2)
    
    while True:
        cotask.task_list.pri_sched()

