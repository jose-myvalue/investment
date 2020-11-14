class Utils:
    @staticmethod
    def get_previous_quarter(quarter, year):
        if quarter in range(2, 5):
            return quarter - 1, year
        elif quarter == 1:
            return 4, year - 1

    @staticmethod
    def get_next_quarter(quarter, year):
        if quarter in range(1, 4):
            return quarter + 1, year
        elif quarter == 4:
            return 1, year + 1
