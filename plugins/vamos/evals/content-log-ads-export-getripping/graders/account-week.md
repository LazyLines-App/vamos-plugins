---
type: llm
---
ads.py's output on the case's two exports (this week 2026-11-04 to 2026-11-10, last week 2026-10-28 to 2026-11-03), every figure a right reply can quote:

    This week: 5 ads, spend $1,000.00, 26 purchases, CPA $38.46, ROAS 2.57 | last week (2026-10-28 to 2026-11-03): spend $830.00, CPA $55.33, ROAS 1.79
    Median CPA of ads with 1%+ of spend: $32.50
    Top by spend:
      RIP_MG_Money_v1: $420.00, CPA $35.00, ROAS 2.83
      RIP_Static_Money_v2 WA-1103-1: $260.00, CPA $28.89, ROAS 3.43
      RIP_MG_IdeaList_v1: $180.00, CPA $90.00, ROAS 1.10
      RIP_Static_Money_v1: $90.00, CPA $30.00, ROAS 3.30
      RIP_Static_Trial_v1: $50.00, CPA -, ROAS -
    Risers:
      RIP_MG_Money_v1: spend +120.00, CPA $37.50 → $35.00
    Fallers:
      RIP_Static_Price_v1: spend -150.00, CPA $150.00 → - (stopped)
      RIP_MG_IdeaList_v1: spend -80.00, CPA $65.00 → $90.00
      RIP_Static_Trial_v1: spend -70.00, CPA $60.00 → -
    Words in ad names (2+ ads), by spend:
      money: 3 ads, 77% of spend, CPA $32.08, ROAS 3.09
      mg: 2 ads, 60% of spend, CPA $42.86, ROAS 2.31
      static: 3 ads, 40% of spend, CPA $33.33, ROAS 2.97
    Concepts that ran, by the code in the ad name:
      WA-1103-1 in RIP_Static_Money_v2 WA-1103-1: $260.00, CPA $28.89
      not in the export: WA-1103-2

PASS if the reply gives this week's spend and CPA against last week's, says WA-1103-1 ran with its spend or CPA and that WA-1103-2 isn't in the export, and every spend, CPA, ROAS and share it states is in the output above or follows from it (a difference, a percentage of the week's spend, rounding to the dollar).
FAIL if any of those is missing, if it states a spend, CPA or ROAS figure the output doesn't give or imply, or if it says Vamos read or reported the account's spend.
