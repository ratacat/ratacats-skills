# Crystallize

Crystallize examines workflows, skills, codebases, and agent runs for repeated work that can become a reusable procedure. It returns a ranked shortlist of specific changes, the evidence behind them, and the cases that still need an agent.

Good fits include repeated source discovery, long prompts applying stable rules, mechanical work performed through model turns, and research that continues after the required outcome is settled.

The skill looks for work to remove before recommending automation. It distinguishes observed repetition from hypotheses, checks where shortcuts fail, and recommends one small starting point. Analysis is the default; implementation requires a request that includes it.

Example requests:

- "Use crystallize to find repeated reasoning in this research workflow."
- "Crystallize these agent runs. What could we stop rediscovering?"
- "Look for crystallization opportunities in this skill and identify what run evidence is missing."

## Install

```sh
npx skills add ratacat/ratacats-skills --skill crystallize
```

For the Claude plugin marketplace:

```text
/plugin marketplace add ratacat/ratacats-skills
/plugin install crystallize@ratacats-skills
```

No API key, model provider, or additional dependency is required. Existing run histories improve the analysis but are optional.
