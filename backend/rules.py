"""
US healthcare benefits rulebook — IRS Rev. Proc. 2025-19 (2026 plan year).
Used to validate contributions and display plan compliance info.
"""

PLAN_YEAR = "2026"

# --- HSA (Health Savings Account) — IRS 2026 limits ---
HSA = {
    "annual_limit_self_only": 4400.00,
    "annual_limit_family": 8750.00,
    "catch_up_age": 55,
    "catch_up_amount": 1000.00,
    "hdhp_min_deductible_self": 1700.00,
    "hdhp_min_deductible_family": 3400.00,
    "hdhp_max_oop_self": 8500.00,
    "hdhp_max_oop_family": 17000.00,
}

# --- FSA (Flexible Spending Account) — IRS 2026 indexed limit ---
FSA = {
    "annual_limit_healthcare": 3400.00,
    "grace_period_days": 75,  # or carryover up to $680 (15% of limit) — plan-dependent
    "use_it_or_lose_it": True,  # unless employer offers grace/carryover
}

# --- Employer plan rules (Optum-style organizational policy) ---
EMPLOYER_PLAN = {
    "employer_name": "Optum / UnitedHealth Group",
    "minimum_employee_hsa_monthly": 50.00,
    "employer_hsa_seed_monthly": 75.00,
    "employer_match_max_monthly": 100.00,
    "employer_match_requires_min_employee": True,
    "fsa_enrollment_window": "Annual open enrollment (Nov 1–15)",
    "eligible_expenses_url": "https://www.irs.gov/publications/p502",
}


def hsa_annual_limit(coverage_type: str, age: int) -> float:
    base = HSA["annual_limit_family"] if coverage_type == "family" else HSA["annual_limit_self_only"]
    if age >= HSA["catch_up_age"]:
        base += HSA["catch_up_amount"]
    return base


def hsa_remaining_allowance(coverage_type: str, age: int, contributed_ytd: float) -> float:
    return max(0.0, round(hsa_annual_limit(coverage_type, age) - contributed_ytd, 2))


def fsa_remaining_allowance(contributed_ytd: float) -> float:
    return max(0.0, round(FSA["annual_limit_healthcare"] - contributed_ytd, 2))


def validate_hsa_contribution(amount: float, coverage_type: str, age: int, contributed_ytd: float) -> str | None:
    if amount < EMPLOYER_PLAN["minimum_employee_hsa_monthly"]:
        return (
            f"Minimum employee HSA contribution is "
            f"${EMPLOYER_PLAN['minimum_employee_hsa_monthly']:.2f}/month per plan policy"
        )
    remaining = hsa_remaining_allowance(coverage_type, age, contributed_ytd)
    if amount > remaining:
        return f"Exceeds 2026 IRS HSA annual limit. Remaining allowance: ${remaining:.2f}"
    return None


def get_rulebook() -> dict:
    return {
        "plan_year": PLAN_YEAR,
        "source": "IRS Rev. Proc. 2025-19; Optum employer plan policy",
        "hsa": {
            **HSA,
            "notes": [
                "Must be enrolled in a qualified HDHP to contribute.",
                "Employer + employee contributions combined cannot exceed annual limit.",
                f"Catch-up contribution (${HSA['catch_up_amount']:.0f}) available at age {HSA['catch_up_age']}+.",
            ],
        },
        "fsa": {
            **FSA,
            "notes": [
                "Healthcare FSA is use-it-or-lose-it unless employer offers grace period or carryover.",
                "Cannot have both HSA and general healthcare FSA (limited-purpose FSA allowed with HSA).",
            ],
        },
        "employer_plan": EMPLOYER_PLAN,
    }
