"""
=========================================================
BatteryMind Recommendation Engine
=========================================================

Converts

SOH
+
Health
+
Risk
+
SHAP Explanation

into actionable battery maintenance recommendations.

Author:
BatteryMind
"""

class BatteryRecommendation:

    def __init__(self):

        print("=" * 60)
        print("BatteryMind Recommendation Engine Ready")
        print("=" * 60)

    ##########################################################
    # General Recommendation
    ##########################################################

    def general_recommendation(self, health):

        if health == "Excellent":

            return [
                "Battery is operating optimally.",
                "Continue normal charging practices.",
                "Perform routine monitoring."
            ]

        elif health == "Healthy":

            return [
                "Battery health is good.",
                "Avoid unnecessary fast charging.",
                "Monitor temperature periodically."
            ]

        elif health == "Moderate":

            return [
                "Battery degradation has started.",
                "Reduce deep discharge cycles.",
                "Avoid continuous high-current loads."
            ]

        elif health == "Degraded":

            return [
                "Battery performance has significantly decreased.",
                "Reduce operating temperature.",
                "Schedule battery maintenance."
            ]

        else:

            return [
                "Battery is critically degraded.",
                "Replacement is recommended.",
                "Avoid high-current operation."
            ]

    ##########################################################
    # SHAP Recommendation
    ##########################################################

    def shap_recommendation(self, shap_features):

        recommendations = []

        for feature in shap_features:

            name = feature["feature"]

            if "Temperature" in name:

                recommendations.append(
                    "Improve thermal management to reduce temperature stress."
                )

            elif "Voltage" in name:

                recommendations.append(
                    "Maintain stable charging voltage and avoid over-discharge."
                )

            elif "Current" in name:

                recommendations.append(
                    "Reduce high-current discharge whenever possible."
                )

            elif "Energy" in name:

                recommendations.append(
                    "Optimize energy usage to reduce battery wear."
                )

            elif "Time" in name:

                recommendations.append(
                    "Avoid unnecessarily long operating cycles."
                )

        recommendations = list(dict.fromkeys(recommendations))

        return recommendations

    ##########################################################
    # Risk Message
    ##########################################################

    def risk_message(self, risk):

        messages = {

            "Low":
            "Battery risk is minimal.",

            "Medium":
            "Moderate degradation detected. Continue monitoring.",

            "High":
            "High degradation detected. Maintenance is recommended.",

            "Critical":
            "Critical battery condition. Immediate replacement advised."

        }

        return messages.get(risk, "")

    ##########################################################
    # Complete Recommendation
    ##########################################################

    def generate(

        self,

        soh,

        health,

        risk,

        shap_features

    ):

        return {

            "soh": round(soh * 100, 2),

            "health": health,

            "risk": risk,

            "risk_message": self.risk_message(risk),

            "general_recommendations":

                self.general_recommendation(health),

            "shap_recommendations":

                self.shap_recommendation(shap_features)

        }


############################################################
# Testing
############################################################

if __name__ == "__main__":

    engine = BatteryRecommendation()

    sample_shap = [

        {

            "feature": "Temperature_std",

            "impact": -0.05,

            "direction": "Decrease SOH"

        },

        {

            "feature": "Current_rms",

            "impact": -0.03,

            "direction": "Decrease SOH"

        },

        {

            "feature": "Voltage_min",

            "impact": 0.02,

            "direction": "Increase SOH"

        }

    ]

    result = engine.generate(

        soh=0.84,

        health="Healthy",

        risk="Low",

        shap_features=sample_shap

    )

    from pprint import pprint

    pprint(result)