# PM Market Analysis

This skill is for market-aware analysis of one prediction-market event.

Use it after the agent has enough world context and needs to connect that context to exact instruments, current market structure, liquidity, resolution risk, platform risk, and possible forecast or proposal outputs.

This is disciplined trading context. It keeps the agent from waving at a headline and calling it analysis. A good pass identifies the exact market, the exact side, the exact resolution path, and the practical forces around price and execution.

Good fits:

- Analyzing one PM event with many child markets
- Matching Polymarket or Kalshi instrument identity
- Checking liquidity and spread concerns
- Writing a forecast, brief, proposal, or no-publish result
- Separating market mechanics from world facts

Expected output: exact instrument identity, rule summary, world thesis, market context, key risks, and a forecast, proposal, brief, or no-publish result. Use `pm-deep-analysis` first when the world model is thin. Use this skill when market facts matter.
