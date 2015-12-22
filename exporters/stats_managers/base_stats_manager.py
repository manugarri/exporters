from exporters.logger.base_logger import StatsManagerLogger
from exporters.pipeline.base_pipeline_item import BasePipelineItem


class BaseStatsManager(BasePipelineItem):
    def __init__(self, options):
        super(BaseStatsManager, self).__init__(options)
        self.logger = StatsManagerLogger({'log_level': options.get('log_level'),
                                          'logger_name': options.get('logger_name')})

    def iteration_times(self, times):
        raise NotImplementedError

    def populate(self):
        raise NotImplementedError

    def update_module_stats(self, module, mod_stats):
        self.stats.setdefault(module, {}).update(mod_stats)
