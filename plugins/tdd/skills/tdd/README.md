# TDD

This skill helps an agent build or fix software with a red-green-refactor loop.

Use it when the user wants test-first work, integration tests, regression coverage, or a careful fix that proves behavior before changing code. The skill favors public interfaces over private internals, so tests describe what the system does instead of how it happens inside.

TDD gives the work a steady heartbeat: write the failing behavior, make it pass, clean up without changing the promise. That rhythm keeps agents from overbuilding or fixing the wrong thing.

Good fits:

- Reproducing a bug before patching it
- Adding a feature through a public API
- Protecting a refactor with behavior tests
- Choosing when mocks help and when they hide risk

It is not "write all tests first." It is one thin slice at a time.
