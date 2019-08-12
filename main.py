import logging
from logger import Logger
from systemStatus import SystemStatus
import threading
from queue import Queue
from time import sleep, time


def system_state_callback(logger, q_cpu, q_ap, q_gcs):
    logger.info("[SYS_STATE]: Function system_state_callback called")
    system_status = SystemStatus(logger, q_cpu, q_ap, q_gcs)
    while True:
        system_status.update()


def gcs_callback(logger, q_sys_status):
    logger.info("[GCS]: Function gcs_callback called")
    msg_count = 0
    while True:
        msg_count += 1
        if msg_count is 256:
            msg_count = 0
        if msg_count < 10:  
            q_sys_status.put(msg_count)
            logger.debug("[GCS]: put msg_count = %d", msg_count)
        sleep(1)


def ap_callback(logger, q_sys_status):
    logger.info("[AP]: Function ap_callback called")
    msg_count = 0
    while True:
        msg_count += 1
        if msg_count is 256:
            msg_count = 0
        if msg_count < 10:  
            q_sys_status.put(msg_count)
            logger.debug("[AP]: put msg_count = %d", msg_count)
        sleep(1)


if __name__ == "__main__":
    # Create logger
    logger = Logger(logger_name=__name__, file_name='state.log',
        file_level=logging.DEBUG, console_level=logging.DEBUG)
    
    # Create queue:
    queue_cpu = Queue()
    queue_ap = Queue()
    queue_gcs = Queue()
  
    # Create threads:
    thread_system_state = threading.Thread(target=system_state_callback, 
        args=(logger, queue_cpu, queue_ap, queue_gcs,), daemon=True)
    thread_gcs = threading.Thread(target=gcs_callback, args=(logger, queue_gcs,), daemon=True)
    thread_ap = threading.Thread(target=ap_callback, args=(logger, queue_ap,), daemon=True)

    # Start threads
    thread_system_state.start()
    thread_gcs.start()
    thread_ap.start()

    while True:
        sleep(10)
