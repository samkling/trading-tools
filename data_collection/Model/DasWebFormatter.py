from datetime import datetime

class DasWebFormatter:
    def __init__(self, data):
        self.data = data.split('\n')
        self.file_name = ""
        self.format_data()
        self.create_file_name()
        self.create_file()

    def create_file(self):
        self.write_to_tradervue_file("Date,Time,Symbol,Quantity,Price,Side")
        today_date = datetime.today().strftime('%Y-%m-%d') #or manually set date
        for row in self.data:
            data_string = ','.join([today_date, row[1], row[2], row[5], row[4], row[3]])
            self.write_to_tradervue_file(data_string)


    def write_to_tradervue_file(self, data_string):
        with open(self.file_name, "a") as file:
            file.write(f"{data_string}\n")
        print(f"{data_string}")

    def create_file_name(self):
        today_date = datetime.today().strftime('%Y-%m-%d')
        self.file_name = f"TraderVueImport/{today_date}.csv"

    def format_data(self):
        data = []
        for row in self.data:
            if len(row) > 0:
                data.append(row.split('\t'))
        self.data = data

    def print_data(self):
        for row in self.data:
            print(row)
