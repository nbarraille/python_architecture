import logging


class Service:
    def __init__(self):
        self.result = None
        self.error = None

    def run(self):
        try:
            self.result = self.execute()
            logging.info(f"{type(self).__name__} successfully executed")
        except Exception as e:
            logging.error(f"Error in {type(self).__name__}", exc_info=e)
            self.error = e
        return self.result

    def execute(self):
        raise NotImplementedError()
