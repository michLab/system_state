import logging
from logger import Logger
from systemStatus import SystemStatus
import threading
from multiprocessing import Queue
from time import sleep, time


class SystemStatus1:
    def __init__(self, logger, q_cpu, q_ap, q_gcs):
        self.logger = logger
        self.queue_cpu = q_cpu
        self.queue_ap = q_ap
        self.queue_gcs = q_gcs

        self.last_gcs_message_time = 0
        self.gcs_message_timeout = 1.5
        self.gcs_timeout_exceeded = False

        self.last_ap_message_time = 0
        self.ap_message_timeout = 1.5
        self.ap_timeout_exceeded = False
        
        logger.info("[SYS_STATE]: logger.id = %d", id(self.logger))
        logger.info("[SYS_STATE]: queue_ap.id = %d", id(self.queue_ap))
        logger.info("[SYS_STATE]: queue_gcs.id = %d", id(self.queue_gcs))


    def update(self):
        self.update_gcs()
        self.update_ap()
        self.logger.info("[SYS_STATE]: gcs_mps = %d, ap_mps = %d",
            self.gcs_msg_count, self.ap_msg_count)
        sleep(0.5)

    def update_gcs(self):
        try:
            self.gcs_msg_count = queue_gcs.get_nowait()
            self.logger.debug("[SYS_STATE]: get gcs_msg_count = %d", self.gcs_msg_count)
            self.last_gcs_message_time = self.get_time()
            self.gcs_timeout_exceeded = False

        except:
            self.logger.debug("[SYS_STATE]: No data in queue_gcs")
            if (self.get_time() - self.last_gcs_message_time) > self.gcs_message_timeout:
                self.logger.warning("[SYS_STATE]: Last gcs data is older than %f [s]",
                    self.gcs_message_timeout)
                self.gcs_timeout_exceeded = True
                self.gcs_msg_count = 0

    
    def update_ap(self):
        try:
            while True:  # Get only the last message, drop others
                self.ap_msg_count = queue_ap.get_nowait()
                self.logger.debug("[SYS_STATE]: get ap_msg_count = %d", self.ap_msg_count)
                self.last_ap_message_time = self.get_time()
                self.ap_timeout_exceeded = False

        except:
            self.logger.debug("[SYS_STATE]: No data in queue_ap")
            if (self.get_time() - self.last_ap_message_time) > self.ap_message_timeout:
                self.logger.warning("[SYS_STATE]: Last ap data is older than %f [s]",
                    self.ap_message_timeout)
                self.ap_timeout_exceeded = True
                self.ap_msg_count = 0

        
    def get_time(self):
        return time()


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

    logger.info("[MAIN]: logger.id = %d", id(logger))
    logger.info("[MAIN]: queue_ap.id = %d", id(queue_ap))
    logger.info("[MAIN]: queue_gcs.id = %d", id(queue_gcs))

    
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
