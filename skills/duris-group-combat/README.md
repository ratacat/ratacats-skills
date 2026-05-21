# Duris Group Combat

This skill helps an agent reason about Duris combat when several characters, roles, targets, and risks are moving at once.

Use it when the question is not "what is Duris?" but "what should the group do now?" It focuses on tanks, assists, caster readiness, adds, bash risk, command pacing, and survival-first decision making.

This keeps the agent from spamming commands or choosing a clever action when a boring survival action matters more. Group combat rewards timing, shared targets, and clear role bindings. This skill makes those priorities explicit.

Good fits:

- Designing group combat behavior
- Parsing a fight log
- Choosing assist or rescue logic
- Handling adds and target swaps
- Preventing duplicate casts or panic spam

Use it with `duris-game-knowledge`. The game-knowledge skill explains the world; this skill handles the group fight. When combat state is unclear, observe, parse, and update state before acting.
