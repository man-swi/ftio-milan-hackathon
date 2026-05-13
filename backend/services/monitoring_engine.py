from apscheduler.schedulers.background import (
    BackgroundScheduler
)

from backend.services.trend_monitor import (
    detect_trend_spikes
)

from datetime import datetime

import time


class MonitoringEngine:

    def __init__(self):

        self.scheduler = (
            BackgroundScheduler()
        )

        self.monitoring_active = False

        self.job_registry = []

        self.active_alerts = []

    # ===================================
    # START MONITORING SYSTEM
    # ===================================

    def start_monitoring(self):

        if self.monitoring_active:

            print(
                "Monitoring already active."
            )

            return

        print(
            "STARTING FTIO MONITORING ENGINE"
        )

        # ===================================
        # REGISTER JOBS
        # ===================================

        self.scheduler.add_job(

            self.run_trend_monitoring,

            trigger="interval",

            seconds=15,

            id="trend_monitoring"
        )

        self.scheduler.add_job(

            self.run_inventory_monitoring,

            trigger="interval",

            seconds=15,

            id="inventory_monitoring"
        )

        self.scheduler.add_job(

            self.generate_daily_summary,

            trigger="interval",

            hours=24,

            id="daily_summary"
        )

        self.scheduler.start()

        self.monitoring_active = True

        print(
            "FTIO monitoring system active."
        )

    # ===================================
    # STOP MONITORING
    # ===================================

    def stop_monitoring(self):

        if not self.monitoring_active:

            print(
                "Monitoring already stopped."
            )

            return

        self.scheduler.shutdown()

        self.monitoring_active = False

        print(
            "FTIO monitoring stopped."
        )

    # ===================================
    # TREND MONITORING
    # ===================================

    def run_trend_monitoring(self):

        print(
            f"[{datetime.now()}] "
            "Running trend monitoring..."
        )

        alerts = detect_trend_spikes()

        if alerts:

            print(
                f"Detected "
                f"{len(alerts)} "
                f"trend alerts."
            )

            self.active_alerts.extend(
                alerts
            )

            # Keep only latest alerts
            self.active_alerts = (

                self.active_alerts[-50:]
            )

            for alert in alerts:

                print(
                    f"ALERT: "
                    f"{alert['message']}"
                )

        else:

            print(
                "No trend anomalies detected."
            )

    # ===================================
    # INVENTORY MONITORING
    # ===================================

    def run_inventory_monitoring(self):

        print(
            f"[{datetime.now()}] "
            "Running inventory monitoring..."
        )

        # Placeholder
        # Actual anomaly detection added
        # in Step 15.4

    # ===================================
    # DAILY EXECUTIVE SUMMARY
    # ===================================

    def generate_daily_summary(self):

        print(
            f"[{datetime.now()}] "
            "Generating daily executive summary..."
        )

        # Placeholder
        # Added later in Step 15.5

    # ===================================
    # ALERT ACCESSOR
    # ===================================

    def get_active_alerts(self):

        return self.active_alerts[-20:]

    # ===================================
    # STATUS
    # ===================================

    def get_monitoring_status(self):

        return {

            "monitoring_active":
            self.monitoring_active,

            "active_jobs":

            [
                job.id

                for job in
                self.scheduler.get_jobs()
            ],

            "job_count":

            len(
                self.scheduler.get_jobs()
            ),

            "active_alerts":

            len(
                self.active_alerts
            )
        }


# ===================================
# GLOBAL ENGINE INSTANCE
# ===================================

monitoring_engine = (
    MonitoringEngine()
)