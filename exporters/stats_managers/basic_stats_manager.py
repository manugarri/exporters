from exporters.stats_managers.base_stats_manager import BaseStatsManager


class BasicStatsManager(BaseStatsManager):

    def populate(self):
        self.logger.debug(repr(self.stats))
