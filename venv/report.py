import config
import datetime

class Report():
    def __init__(self, error_path, response_path):
        self.log_errors = {}
        self.log_response = {}

    def add_error(self, function, error_text):
        key = datetime.datetime.now().strftime("%H:%M:%S.%f")
        if key in self.log_errors.keys():
            key = key + "0"
            while key in self.log_errors.keys():
                elem = int(key[-1])
                elem += 1
                key[-1] = str(elem)
        self.log_errors[key] = function + ": " + error_text
        self.print_error_while_working(key, function + ": " + error_text)

    def print_errors(self):
        with open (config.report_errors_path, 'w') as file_writer:
            for key, val in self.log_errors.items():
                file_writer.write('{0} - {1}\n'.format(key, val))

    def add_log(self, function, log_text):
        var_text = self.parse_log(function, log_text)
        if var_text:
            log_text = str(var_text)
            log_text = log_text.replace('"', '')
        key = datetime.datetime.now().strftime("%H:%M:%S.%f")
        if str(key) in str(self.log_response.keys()):
            key = key + "0"
            while key in self.log_response.keys():
                elem = int(key[-1])
                elem += 1
                key = key[:-1] +  str(elem)
        self.log_response[key] = function + ": " + log_text
        self.print_log_while_working(key, function + ": " + log_text)

    def print_logs(self):
        with open (config.report_logs_path, 'w') as file_writer:
            for key, val in self.log_response.items():
                file_writer.write('{0} - {1}\n'.format(key, val))

    def print_log_while_working(self, key, val):
        with open (config.report_logs_path, 'a') as file_writer:
            file_writer.write('{0} - {1}\n'.format(key, val))

    def print_error_while_working(self, key, val):
        with open (config.report_errors_path, 'a') as file_writer:
            file_writer.write('{0} - {1}\n'.format(key, val))

    def parse_log(self, function, response):
        if str(function) == "Registration":
            if "[{" in response:
                response = response.split(',')
                first_response = response[0]
                first_response = first_response[3:]
                return (first_response, response[1], response[10])
            else:
                return False