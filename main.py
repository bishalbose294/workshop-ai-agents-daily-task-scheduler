from agent import DailyPlannerAgent

if __name__ == "__main__":
    agent = DailyPlannerAgent()
    result = agent.run(
        "Plan my day for 2026-07-09. Fit in my pending tasks around my meetings, "
        "and account for the weather."
    )
    print("\n=========== FINAL DAILY PLAN ===========")
    print(result)