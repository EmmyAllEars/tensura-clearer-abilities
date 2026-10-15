# Brief: in-game ability descriptions for a Minecraft mod pack

You are writing short in-game descriptions for abilities from the Minecraft mods **Tensura: Reincarnated 2.0.1.3** and **Mysticism 2.2.1** (NeoForge 1.21.1). They replace the mods' own one-line descriptions in a resource pack for one family's server. The players' complaint is that the mod never says what an ability actually does, which key action uses it, or what its modes and sneak/scroll actions are.

## Inputs

- `BATCH` — a JSON file of fact sheets, one per ability (path given at the end). Fields:
  - `name`, `type`, `desc` (the mod's own description)
  - `how`: how it is triggered, read from code: `Cast` (hold to chant for the cast time, then release), `Press key`, `Hold key`, `Press or hold`, or null
  - `tog`: `always` (can be toggled on/off), `mastered` (toggleable once mastered), or null
  - `modes`: mode ids; display names are in the lang file as `tensura.skill.mode.<id>` (or `mysticism.skill.mode.<id>`)
  - `shift`: methods in which the code checks sneaking; `scroll`: whether scrolling changes something
  - `effects` (potion/status effects it references), `entities` (things it spawns), `blocks`, `calls` (notable game calls)
  - `cfg`: this server's config values for the ability. **Times are in ticks: 20 ticks = 1 second.** Costs are magicule unless named aura.
- `examples.json` — 70 finished descriptions in the target style. Read several before starting. They are the standard.
- Lang files for names and modes:
  - `LANG_TENSURA`
  - `LANG_MYSTICISM`
- The unpacked mod code, for reading deeper with `javap -p -c <path-to-.class>`:
  - `JARS/tensura/io/github/manasmods/tensura/...`
  - `JARS/mysticism/io/github/Memoires/mysticism/...`

  Ability classes are under `ability/` and are named after the ability, e.g. `GravityFieldSkill.class` or `FireBallMagic.class`. Config values are in the `cfg` field already.

## What to write

For each ability, one description string:

1. **First line: what it actually does**, concretely. Use the effects, entities and config numbers: damage, radius, duration in seconds, cost when it is large. No flavour text, and don't repeat the mod's vague wording.
2. **Then the controls**, one short line each: how to trigger it, each mode and what that mode does, any sneak action, any scroll action.
3. **Keep it short.** Aim for 100 to 250 characters; Unique skills with many modes may reach about 350. The in-game box shows about 7 lines of 22 characters before it scrolls.

### Markup (it is converted to colours later)

- `*text*` marks a control action, e.g. `*Hold 4s, release*`, `*Press*`, `*Sneak+press*`, `*Scroll*`
- `[Mode name]` marks a mode, using the display name from the lang file
- `{P}` stands for the word "Passive" at the start of a passive effect
- `\n` separates lines
- Use "s" for seconds, e.g. "for 60s", and "×1.5" style multipliers.

### Accuracy rules (the most important part)

- **Only state what the facts or the code support.** If you can't tell what a mode or action does, say so briefly, e.g. "Its effect is not checked." Never invent mechanics.
- For Unique skills, and anything whose fact sheet is thin, open the class with `javap` and read `onPressed`, `onHeld`, `onRelease`, `onToggleOn`, `getModeId` and any mode handlers before writing.
- `shift` listed under `onPressed`, `onHeld` or `onRelease` means sneaking changes that action. Work out what it changes from the code, or say "Sneak changes how it works (not checked)".
- `scroll: true`: if the scroll handler calls `HakiSkill.changeEPUsed`, it is "*Scroll* (mastered): Power Scale"; otherwise find what value it changes (range, size, etc.).
- `Cast` means `*Hold Ns, release*`, with N from `castTime` (ticks ÷ 20). Give the mastered time in brackets if it differs.
- Do not mention cooldowns unless they are long (over 30s) or the main constraint.

## Output

Write a single JSON object to `OUT`, mapping lang keys to description strings:

```json
{
  "tensura.skill.fire_ball.description": "Exploding fireball: 100 damage plus 30 fire, 3-block blast.\n*Hold 3s (1s mastered), release*."
}
```

- The key is `<namespace>.skill.<path>.description`, where the ability id is `<namespace>:<path>`.
- Include every ability in the batch. If one is not understandable at all, use the value `"SKIP: <reason>"`.
- The file must be valid JSON (UTF-8). Do not write anything else.

Finish with a one-paragraph summary: how many you wrote, how many you read the code for, and any you are unsure of.
