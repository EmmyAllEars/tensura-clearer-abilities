# Tensura Clearer Abilities

A Minecraft 1.21.1 resource pack for the family's Tensura server. It rewrites the ability descriptions in Tensura's ability screen so each one starts with its controls (passive or active, press / hold / cast, modes, sneak and scroll actions), followed in grey by the mod's own description. It also uses Tensura's creative-mode HUD frame in survival.

- `pack/` is the resource pack. Copy it into a profile's `resourcepacks` folder (or zip its contents).
- `tools/build.py` regenerates the lang files: `python3 tools/build.py <tensura en_us.json> <mysticism en_us.json>`.
- `data/controls.json` holds facts read from the mod jars (modes, sneak and scroll handlers). `data/abilities_in_use.json` is the abilities the three players had on 2026-10-15. `data/handwritten.json` holds descriptions written by hand, which the build uses as-is.
- Facts come from reading the mods' code and are untested in play unless noted. Five abilities are left with Tensura's text because the build could not match them to code.

Pack format 34 (Minecraft 1.21.1). Tensura 2.0.1.3, Mysticism 2.2.1.
