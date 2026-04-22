from __future__ import annotations

TECHNICAL_TERMS = {
    "tokenomics", "whitepaper", "vesting", "multisig", "timelock",
    "dao", "governance", "staking", "yield", "apy", "tvl", "dex",
    "amm", "liquidity", "slippage", "impermanent", "oracle",
}

MEME_QUALITY = {
    "original", "unique", "culture", "community", "viral", "trend",
    "narrative", "story", "identity", "brand", "niche", "focused",
}


class ClarityAnalyzer:
    def analyze(self, narratives: list[str]) -> float:
        if not narratives:
            return 50.0
        tokens = " ".join(narratives).lower().split()
        total = len(tokens) or 1

        tech_count = sum(1 for t in tokens if t in TECHNICAL_TERMS)
        meme_count = sum(1 for t in tokens if t in MEME_QUALITY)
        word_diversity = len(set(tokens)) / total

        tech_boost = min(tech_count * 5, 20)
        meme_boost = min(meme_count * 4, 15)
        diversity_score = word_diversity * 40

        return max(0.0, min(100.0, 30.0 + tech_boost + meme_boost + diversity_score))
