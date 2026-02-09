from __future__ import annotations
import os

NOISE_TOKENS = {
    "moon", "ape", "wagmi", "gm", "pump", "fomo", "ngmi", "wen",
    "100x", "1000x", "gem", "banger", "send", "degen", "chad",
    "alpha", "based", "rugged", "cooked", "ser", "fud", "bullish",
}

SIGNAL_TOKENS = {
    "utility", "community", "locked", "audit", "doxxed", "roadmap",
    "building", "partnership", "organic", "staking", "governance",
    "protocol", "integration", "liquidity", "vesting", "multisig",
}

CRASH_TOKENS = {
    "rug", "scam", "honeypot", "drain", "exit", "fake", "dump",
    "bot", "shill", "honeypot", "migrating", "abandoned",
}


def _heuristic_clarity(narratives: list[str]) -> float:
    if not narratives:
        return 50.0
    tokens = " ".join(narratives).lower().split()
    total = len(tokens) or 1

    noise = sum(1 for t in tokens if t in NOISE_TOKENS)
    signal = sum(1 for t in tokens if t in SIGNAL_TOKENS)
    crash = sum(1 for t in tokens if t in CRASH_TOKENS)

    noise_ratio = noise / total
    signal_boost = min(signal * 6, 30)
    crash_penalty = crash * 15

    score = 58.0 - noise_ratio * 180 + signal_boost - crash_penalty
    return max(0.0, min(100.0, score))


class SignalAgent:
    def __init__(self) -> None:
        self._api_key = os.environ.get("ANTHROPIC_API_KEY", "")

    def score(self, narratives: list[str]) -> float:
        if self._api_key:
            try:
                return self._claude_score(narratives)
            except Exception:
                pass
        return _heuristic_clarity(narratives)

    def _claude_score(self, narratives: list[str]) -> float:
        import anthropic
        client = anthropic.Anthropic(api_key=self._api_key)
        text = "\n".join(narratives[:5])
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=64,
            messages=[{
                "role": "user",
                "content": (
                    "Analyze the signal quality of this Solana meme coin narrative. "
                    "High signal means clear utility, genuine community, and transparent team. "
                    "Low signal means pure hype, noise, or rug indicators. "
                    "Reply with only a number from 0 to 100.\n\n"
                    f"Narrative:\n{text}"
                ),
            }],
        )
        raw = msg.content[0].text.strip()
        return max(0.0, min(100.0, float("".join(c for c in raw if c.isdigit() or c == "."))))
