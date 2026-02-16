from __future__ import annotations
import statistics


class RoutingAnalyzer:
    def analyze(self, mention_series: list[float], holder_series: list[int]) -> float:
        mention_score = self._mention_velocity(mention_series)
        holder_score = self._holder_growth(holder_series)
        return max(0.0, min(100.0, mention_score * 0.55 + holder_score * 0.45))

    def _mention_velocity(self, series: list[float]) -> float:
        if len(series) < 2:
            return 50.0
        first = series[0] or 1.0
        latest = series[-1]
        growth = (latest - first) / first * 100
        growth_score = min(max(growth, 0.0), 100.0)
        if len(series) >= 3:
            diffs = [series[i] - series[i - 1] for i in range(1, len(series))]
            acceleration = diffs[-1] - diffs[0]
            accel_bonus = min(max(acceleration / (first or 1) * 20, -15), 15)
        else:
            accel_bonus = 0.0
        return max(0.0, min(100.0, growth_score * 0.7 + 50 * 0.3 + accel_bonus))

    def _holder_growth(self, series: list[int]) -> float:
        if len(series) < 2:
            return 50.0
        first = series[0] or 1
        latest = series[-1]
        growth = (latest - first) / first * 100
        return max(0.0, min(100.0, growth * 0.8))
