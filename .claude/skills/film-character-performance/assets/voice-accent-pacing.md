# Voice, accent and pacing sheet

Use alongside the [character performance sheet](character-performance.md). Create one identity card per character, then one delivery/timing sheet per scene. Reuse the chosen identity block unchanged; change delivery to serve the scene. Mark undecided casting choices as proposals.

## Character voice identity

| Field | Selected direction |
|---|---|
| Character / stable voice ID / version | |
| Status | Proposed / selected for testing / approved from playback |
| Anchor take | Exact file, version and useful time range, if available |
| Language | Spoken language and any approved switches |
| Accent baseline | Specific chosen regional variety where relevant; avoid an ambiguous label such as “foreign” |
| Accent prominence | Light / clearly audible / pronounced, relative to the chosen anchor; independent of clarity |
| Pitch region and range | Relative register and expressive range |
| Timbre / resonance / weight | Two or three compatible audible qualities |
| Articulation | Consonant attack, word endings, clarity and approved reductions |
| Habitual rhythm | Thought grouping, baseline pace and cadence |
| Breath / texture | Baseline breath presence and texture; do not add rasp to every emotional line |
| Recognisable constants | Traits that survive whispering, laughter, shouting or exertion |
| Pronunciation lexicon | Version or entries below |

Accent is a casting decision. Do not infer it from a face, skin colour, name or outfit, or use it as shorthand for intelligence, morality or personality. Characters can share a regional background while sounding individually distinct.

## Accent and pronunciation

- Chosen baseline and reference anchor:
- Specific words or sounds to check: use an approved reference or qualified pronunciation source when precision matters; do not invent phonetic rules.
- Register changes with relationship or situation, if relevant:
- Code-switching: exact language/variety, trigger, words affected and return point, only when part of the character design:
- Continuity: preserve the accent baseline through emotional changes unless a specific change is intended.

| Term | Intended spoken form / plain pronunciation guide | Stress or approved phonetic notation | Context / exception | Source and version |
|---|---|---|---|---|
| | | | | |

Preserve normal screenplay spelling. Keep pronunciation instructions outside the spoken line. Use a supported lexicon or phoneme field when available; do not insert SSML or stage directions into speech unless the tool is confirmed to interpret them correctly.

## Session anchor

- Provider / model / version, if exposed:
- Selected voice ID or reference / settings / seed, only where supported:
- Reference provenance and permitted use, if reference audio is involved:
- Recording perspective: distance, environment and on-screen/off-screen position:
- Existing processing and loudness-matching reference:
- Identity prompt version / pronunciation version:

Text alone cannot lock a generated voice. Reuse supported voice/reference controls and compare against the selected take. This sheet does not authorise audio uploads or generation. For an existing film, preserve its selected voice rather than silently recasting it.

## Scene delivery

- Scene / take / duration / selected branch:
- Speaker → addressee and relationship:
- Starting breath, effort and emotional state inherited from the previous shot:
- Objective and trigger:
- Delivery arc: starting tactic → turning point → consequence:
- Voice level: whisper / soft / conversational / projected / raised / shouted; where and why it changes:
- Pace arc: measured / flowing / clipped / accelerating / hesitant / interrupted / slowing; where and why:
- Operative words: the few words whose emphasis changes meaning:
- Meaningful pauses: placement, approximate length and what happens in the silence:
- Interruption / overlap: who interrupts, exact word or event, whether the first speaker finishes, and whose words must remain intelligible:
- Physical activity: appropriate breath and effort without replacing the voice identity:
- Listener's response and next turn:

Do not make every line slower to sound serious or louder to sound passionate. Uneven thought lengths, a delayed answer, sudden acceleration or a failed attempt to speak can be intentional. Avoid extra fillers, sobs, laughter or words unless directed.

## Timing ledger

| Window | Speaker / exact approved line, or silence | Speech and internal pauses | Concurrent physical action | Listener / turn-taking | Picture cut or sound bridge |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

- Mark one scene timeline. Include intake, line, internal pause, response, action and final hold; count simultaneous activity once.
- Use a read-through or selected audio duration when available. A rough check is `speech seconds ≈ word count × 60 ÷ words per minute`, plus separately budgeted pauses and reactions. This is not a universal speed target or proof the performance fits.
- Keep the key line intelligible at the intended force. Finish the last word before a protected silent hold.
- If timing does not fit, identify the conflict. Reallocate time or propose a wording change; preserve approved dialogue unless a rewrite is authorised. Do not automatically speed up speech or remove the listener's response.
- A camera cut need not create a vocal pause. A line may continue over a reaction shot. At generation joins, carry the unfinished thought, breath and sound perspective forward without restarting the last sentence.
- Keep extra generation handles separate from final runtime. Trim duplicated handles while preserving emotional timing.

## Reusable prompt

```text
VOICE ID: [character ID and version]

IDENTITY — reuse unchanged
[Chosen language/accent baseline and prominence]
[Pitch region, timbre/resonance and articulation]
[Habitual rhythm and recognisable constants]

SESSION
[Actual supported voice/reference controls, if any]
[Recording perspective and selected session anchor]

THIS SCENE
Speaking to: [addressee]
Intent and trigger: [tactic and cause]
Delivery: [force, pace trajectory, breath, operative words]
Timing: [line window, meaningful pauses, response and hold]
Listener: [reaction, interruption or silence]
Continuity: [incoming/outgoing thought and breath]
Pronunciation: [only relevant approved entries]

SPOKEN LINE ONLY
“[Exact approved dialogue]”
```

Provider syntax is an adapter step. Separate creative direction, literal spoken text and actual API controls.

## Calibration and take review

When new voice generation is authorised, plan a brief comparison of the same identity in neutral, quiet and raised delivery. Add a relevant pronunciation line when needed. For an already approved film voice, compare against its selected take instead of replacing it with new casting tests.

| Take / scene / line | Voice ID / anchor | Model and supported settings | Prompt / lexicon version | Measured duration | Review result / selected? |
|---|---|---|---|---|---|
| | | | | | |

Compare against the same anchor and adjacent edited lines: recognisable speaker, accent, pronunciation, emphasis, breath, intelligibility, turn timing, perspective and lip-sync. Record what was actually heard or seen. Transcription cannot establish accent, speaker assignment or acting quality.

Classify the defect before revising: **identity**, **accent/pronunciation**, **delivery**, **timing**, **recording**, or **edit**. Correct the relevant cue or setting while preserving what works. Record intentional exceptions.
