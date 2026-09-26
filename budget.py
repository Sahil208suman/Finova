from pathlib import Path
import pandas as pd


class BudgetService:

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def set_budget(self, amount):
        budget_data = pd.DataFrame([
            {
                "Monthly_Budget": amount
            }
        ])

        budget_data.to_csv(self.file_path, index=False)

    def get_budget(self):
        if not self.file_path.exists():
            return 0.0

        try:
            budget_data = pd.read_csv(self.file_path)

            if budget_data.empty:
                return 0.0

            return float(budget_data.iloc[0]["Monthly_Budget"])

        except Exception:
            return 0.0
        