class Response():
    def __init__(self, command, message, logger=None):
        self.__logger = logger
        self.__command = command
        self.__message = message

    def send(self):
        if self.__logger is not None:
            self.__logger.info('CLI[{}] {}'.format(self.__command, self.__message))

        print('[{}] {}'.format(self.__command, self.__message))
