import pytest
from kona.models import TokenProcess


@pytest.fixture
def basic_token():
    return TokenProcess(contract_address="So11111111111111111111111111111111111111112")


@pytest.fixture
def healthy_token():
    return TokenProcess(
        contract_address="KonaTest111111111111111111111111111111111111",
        narratives=[
            "community-driven solana token with locked liquidity governance staking roadmap",
            "organic growth building utility doxxed team multisig timelock vesting",
        ],
        price_series=[0.001, 0.0012, 0.0014, 0.0015, 0.0016],
        holder_series=[200, 350, 500, 720, 950],
        lp_locked_pct=95.0,
        mint_disabled=True,
        audit_passed=True,
        top10_pct=18.0,
        token_age_days=21,
        mention_series=[100.0, 180.0, 260.0, 340.0, 450.0],
    )


@pytest.fixture
def crashed_token():
    return TokenProcess(
        contract_address="RugTest1111111111111111111111111111111111111",
        narratives=["ape moon 100x pump fomo send rug scam drain exit dump"],
        price_series=[0.01, 0.008, 0.005, 0.002, 0.0001],
        holder_series=[5000, 3000, 1500, 800, 200],
        lp_locked_pct=0.0,
        mint_disabled=False,
        audit_passed=False,
        top10_pct=92.0,
        token_age_days=1,
        mention_series=[10000.0, 5000.0, 1000.0, 200.0, 50.0],
    )
