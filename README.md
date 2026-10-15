# Tensura Clearer Abilities

A Minecraft 1.21.1 resource pack that rewrites the ability descriptions in **Tensura: Reincarnated** (2.0.1.3) and **Mysticism** (2.2.1) so each one says what the ability actually does and how to use it: passive or active, press / hold / cast, what each mode does, and any sneak or scroll actions.

Example, Gravity Field:

> Lighter gravity: Speed III and Slow Falling for 60s.
> **Self-radius** *press*: on you. *sneak+press*: end it.
> **Field** modes *press*: a sphere where allies get the same and enemies get Slowness and Burden. *sneak+press* looking at it: remove.

Coverage: 405 of the 410 abilities. Every active ability has a full description; passives are labelled "Passive: always on" above the mod's own text.

## Install

Download `Tensura-Clearer-Abilities-<version>.zip` from the [latest release](https://github.com/EmmyAllEars/tensura-clearer-abilities/releases/latest), put it in your `resourcepacks` folder, and enable it above other packs. A server can also send it to players through `resource-pack=` in `server.properties`.

## How it was made

Descriptions were written from the mods' compiled code and a server's config values, not from play. Numbers (damage, radius, durations, costs) match that server's config and may differ on yours.

- About 70 were written by Claude (Anthropic) in a working session with Emmy Ringuette.
- About 230 were written by Codex (OpenAI) and 24 by a Claude Sonnet subagent, each from a per-ability fact sheet plus its own reading of the code, following `data/agent_batches/BRIEF.md`. A sample of their numbers was checked against the config.
- Where the code left something unclear, the text says so instead of guessing. Some abilities are unfinished in these mod versions (Mimicry, Provide, Lust's Rebirth), and their descriptions say that too.

If a description is wrong in play, please open an issue.

## Building

`tools/build.py` regenerates `pack/assets/*/lang/en_us.json` from `data/` and the two mods' own `en_us.json` files (not included):

```
python3 tools/build.py <tensura en_us.json> <mysticism en_us.json>
```

- `data/handwritten.json` holds hand-written descriptions, which take priority.
- `data/agent_written.json` is merged from `data/agent_batches/` with `tools/merge_agent.py`.
- `data/controls.json` and `data/controls_rest.json` are facts read from the mods' code.

To release, zip the *contents* of `pack/` so that `pack.mcmeta` sits at the top of the zip.

## Licence

The descriptions and tools are MIT. Tensura: Reincarnated (ManasMods) and Mysticism are All Rights Reserved; this pack contains none of their code or art. It overrides their description text and quotes their one-line passive descriptions.
