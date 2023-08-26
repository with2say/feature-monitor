# monitor/core/metrics.py

class Metric:
    METRICS = {
        'uptime': {'command': 'uptime', 'parser': 'uptime_parser'},
        'free': {'command': 'free -m', 'parser': 'free_parser'},
    }

    @classmethod
    def get_metric(cls, name):
        metric_info = cls.METRICS[name]
        return metric_info['command'], getattr(cls, metric_info['parser'])

    @staticmethod
    def uptime_parser(result):
        # 파싱 로직
        return parsed_result

    @staticmethod
    def free_parser(result):
        # 파싱 로직
        return parsed_result
