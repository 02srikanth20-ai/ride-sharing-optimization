import numpy as np
import random

class RideSharingSimulationEngine:
    def __init__(self):
        self.zones = [f"Zone_{i+1}" for i in range(9)]
        self.zone_states = {
            zone: {
                "demand": random.randint(60, 140), 
                "supply": random.randint(40, 100),
                "avg_distance_km": round(random.uniform(2.5, 6.0), 1)
            } 
            for zone in self.zones
        }

    def compute_game_theory_surge(self, D0, K0, er=1.2, alpha=35.0):
        """Member 2: Stackelberg Game Theory Dynamic Pricing Engine"""
        if D0 <= K0:
            return 1.0
        
        best_surge = 1.0
        max_utility = -float('inf')
        base_fare = 150.0
        commission = 0.20

        for s in np.linspace(1.0, 3.0, 41):
            demand = D0 * np.power(1.0 / s, er)
            supply = K0 + alpha * np.power(s - 1.0, 0.8)
            matches = min(demand, supply)
            revenue = matches * base_fare * s * commission
            penalty = max(0, demand - supply) * 30.0
            utility = revenue - penalty

            if utility > max_utility:
                max_utility = utility
                best_surge = s

        return float(round(best_surge, 2))

    def compute_matching(self, riders_count, drivers_count):
        """Member 1: Fleet Matching Optimization Engine"""
        n = min(int(riders_count), int(drivers_count), 25)
        if n <= 0:
            return 0, 0.0
        
        avg_wait_time = round(max(1.5, 5.0 - (drivers_count / (riders_count + 1) * 2.0)), 1)
        return n, avg_wait_time

    def run_full_simulation(self):
        """Member 3: Executes a full simulation cycle across all zones"""
        zone_results = []
        global_total_matches = 0
        global_total_revenue = 0.0
        global_wait_times = []

        for zone, data in self.zone_states.items():
            d_curr = max(20, data["demand"] + random.randint(-15, 20))
            k_curr = max(10, data["supply"] + random.randint(-10, 15))

            surge = self.compute_game_theory_surge(d_curr, k_curr)

            final_demand = d_curr * np.power(1.0 / surge, 1.2)
            final_supply = k_curr + 35.0 * np.power(max(0.0, surge - 1.0), 0.8)

            matched_count, avg_wait = self.compute_matching(final_demand, final_supply)
            revenue = matched_count * 150.0 * surge * 0.20

            global_total_matches += matched_count
            global_total_revenue += revenue
            global_wait_times.append(avg_wait)

            zone_results.append({
                "zone_id": zone,
                "base_demand": d_curr,
                "base_supply": k_curr,
                "optimal_surge": surge,
                "matched_rides": matched_count,
                "avg_wait_time_min": avg_wait,
                "zone_revenue": round(revenue, 2)
            })

        return {
            "summary": {
                "total_matches": global_total_matches,
                "total_revenue": round(global_total_revenue, 2),
                "avg_wait_time": round(sum(global_wait_times) / len(global_wait_times), 1),
                "active_fleet": sum([z["base_supply"] for z in zone_results])
            },
            "zones": zone_results
        }