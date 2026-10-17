# Voice Consistency System

## Character voice bible

Create one record per character:

| Field | Stable record |
|---|---|
| Character voice ID | Machine-readable ID and version |
| Display name | Screenplay name |
| Casting intent | Narrative and relational role of the voice |
| Permission/provenance | Original design or authorized reference source and usage status |
| Language baseline | Primary language, dialect/accent, code-switching rules |
| Age presentation | Broad perceived age band when relevant |
| Pitch and range | Baseline region and permitted expressive range |
| Timbre and resonance | Bright/dark, smooth/textured, chest/head balance, vocal weight |
| Articulation | Precision, consonant attack, vowel shape, reductions, clarity |
| Rhythm | Baseline pace, phrase length, pauses, cadence, interruption behavior |
| Breath and effort | Breath presence, vocal effort, physicality, restraint |
| Status behavior | How delivery changes with power and relationship |
| Signature invariants | Two to four qualities that must remain recognizable |
| Avoid | Drift patterns, stereotypes, unwanted mannerisms, inconsistent qualities |
| Pronunciation lexicon | Versioned reference to approved pronunciations |
| Tool identity | Provider, model/version, voice/reference ID, seed or embedding if supported |
| Recording anchor | Distance, room, noise, processing, loudness-matching reference |
| Approval | Status, approver, date, and current version |

Avoid contradictory adjective piles. Use a few audible traits with explicit priorities.

## Reusable voice prompt

Keep the identity section unchanged for all of the character's lines:

```text
VOICE ID: [stable character voice ID and version]

LOCKED IDENTITY
[language and accent baseline]
[pitch region, timbre, resonance, vocal weight]
[articulation and habitual rhythm]
[signature invariants]
[stable recording perspective]

SCENE PERFORMANCE
Speaking to: [listener and relationship]
Playable objective: [action toward listener]
Pressure/state: [current physical and emotional facts]
Trajectory: [how delivery changes across the line]
Pace/energy/volume: [scene-specific direction]
Emphasis and pauses: [only meaningful markings]

PRONUNCIATION
[only relevant approved entries]

EXCLUSIONS
[known drift patterns and unwanted delivery]

LINE
[exact approved dialogue]
```

The `LOCKED IDENTITY` block is copied verbatim. Modify `SCENE PERFORMANCE`; do not compensate for weak acting direction by changing identity traits.

## Pronunciation lexicon

| Term | Language/context | Approved spoken form | Phonetic or IPA guide | Stress | Example line | Version |
|---|---|---|---|---|---|---|

Prefer the target tool's supported phoneme or lexicon format when known. Otherwise supply a plain-language guide plus an unambiguous example. Keep brand and character-name pronunciation consistent across speakers unless the story intentionally differs.

## Calibration set

Use a small stable set rather than repeatedly inventing tests:

- a neutral identity line at normal conversational pace
- a line containing recurring names and brand terms
- a quiet, restrained line
- a higher-pressure line that remains inside the approved identity range
- a line with difficult consonants, sibilants, or numbers relevant to the script

The purpose is comparison, not inclusion in the film.

## Take log

| Take ID | Character voice ID | Scene/line ID | Tool and model version | Voice/reference ID | Seed/settings | Prompt version | Processing version | Selected | QC notes |
|---|---|---|---|---|---|---|---|---|---|

Store exact inputs when the tool exposes them. Never treat a filename such as `final-final-2` as sufficient version control.

## Consistency QC

Compare the take to both the approved calibration anchor and adjacent edited lines:

- speaker identity remains immediately recognizable
- accent and phoneme patterns remain stable
- pitch region, timbre, resonance, and age presentation have not drifted
- scene emotion changes performance without replacing the identity
- pace, pause behavior, and articulation remain character-specific
- recurring words follow the pronunciation lexicon
- microphone perspective, room, noise, EQ, loudness, and dynamics match
- time-stretching or editing has not introduced a new vocal character
- breaths, exertion, laughs, cries, and nonverbal vocals belong to the same identity

If a take fails, label the drift category and change one relevant control before generating again.
