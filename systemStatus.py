from time import time, sleep


class SystemStatus:
    def __init__(self, logger, q_cpu, q_ap, q_gcs):
        self.logger = logger
        self.queue_cpu = q_cpu
        self.queue_ap = q_ap
        self.queue_gcs = q_gcs

        logger.info("[SYS_STATE]: logger.id = %d", id(self.logger))
        logger.info("[SYS_STATE]: queue_ap.id = %d", id(self.queue_ap))
        logger.info("[SYS_STATE]: queue_gcs.id = %d", id(self.queue_gcs))

        self.last_gcs_message_time = 0
        self.gcs_message_timeout = 1.5
        self.gcs_timeout_exceeded = False

        self.last_ap_message_time = 0
        self.ap_message_timeout = 1.5
        self.ap_timeout_exceeded = False
        

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