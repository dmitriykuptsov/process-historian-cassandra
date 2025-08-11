FILTER_NONE = 0
FILTER_MAX = 1
FILTER_MIN = 2

ALLOWED_FILTERS = [FILTER_MAX, FILTER_MIN]

class Filter():
    @staticmethod
    def check_filter(type, value, threshold):
        if type == FILTER_MAX:
            if value > threshold:
                return True
        if type == FILTER_MIN:
            if value < threshold:
                return True
        return False
    
    @staticmethod
    def filter_to_human_readable(type):
        if type == FILTER_MAX:
            return "MAXIMUM VALUE"
        if type == FILTER_MIN:
            return "MINIMUM VALUE"