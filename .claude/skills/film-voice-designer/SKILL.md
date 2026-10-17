---
name: film-voice-designer
description: Create and maintain consistent character voice identities and reusable voice-generation prompts for film, animation, commercials, and AI video. Use for voice bibles, casting descriptions, TTS or voice-model prompts, pronunciation guides, performance direction, take tracking, and voice-drift diagnosis; do not use for writing dialogue or the wider sound mix.
---

# Film Voice Designer

Create a versioned voice system in which every character remains recognizably the same speaker while performance changes naturally from scene to scene.

## Read the character and performance handoff

Gather:

- character ID, role, age presentation, history, relationships, and dramatic function
- dialogue, language, dialect or accent, pronunciation, and code-switching requirements
- public manner, private pressure, status behavior, rhythm, verbal habits, and subtext
- scene objective, listener, physical activity, emotional trajectory, and timing
- target voice tool, model, voice ID, seed, reference audio, and supported controls when provided
- recording perspective and post-processing requirements

Do not infer sensitive identity traits from a voice sample. Describe audible and performable qualities only.

## Respect voice rights

Do not clone or impersonate an identifiable real person's voice without confirmed authorization and appropriate rights to the source material. Record the permission and provenance status when real voice references are used. If authorization is absent or unclear, design an original voice from non-identifying acoustic and performance characteristics instead of naming or approximating the person.

## Separate constants from variables

Maintain three layers:

1. **Identity anchor — locked across the production:** character voice ID, language and accent baseline, perceived age band, pitch region, timbre, resonance, vocal weight, articulation baseline, habitual rhythm, signature texture, and stable pronunciation rules.
2. **Session anchor — locked for a recording or generation batch:** provider, model/version, selected voice or reference, seed when supported, recording perspective, microphone/room simulation, baseline settings, processing chain, and prompt version.
3. **Scene performance — allowed to change:** objective, listener, emotional pressure, energy, pace, volume, breath, emphasis, pauses, physical state, and the direction of change within the line.

Never rewrite the identity anchor to express scene emotion. “Angry,” “whispering,” or “out of breath” is a performance state, not a new voice.

Treat accent baseline, accent prominence and intelligibility as distinct choices. Record the chosen regional variety and relevant approved pronunciations. Do not infer accent from appearance or use stereotyped phonetic spelling. Leave unspecified casting choices open; preserve an existing selected voice. Register changes or code-switching need an explicit character/scene reason and defined scope.

## Design and generate

1. Assign every character a stable machine-readable ID such as `CHR_MARA_V01`. Do not identify characters only by display name.
2. Build the voice bible before writing per-line prompts. Use [references/voice-consistency-system.md](references/voice-consistency-system.md).
   Use [the voice, accent and pacing sheet](assets/voice-accent-pacing.md) for a fillable handoff and [prompt patterns](references/voice-accent-pacing.md) for delivery alternatives and an exchange timing example.
3. Choose a short approved anchor sample or diagnostic line set when the tool supports references. Keep the same clean source and reference treatment across sessions.
4. Create and lock a pronunciation lexicon for names, brands, places, invented words, numbers, and recurring phrases.
5. Build prompts by reusing the identity block verbatim, appending only session and scene-performance instructions.
6. Generate neutral calibration lines before emotionally extreme scenes. Approve the base identity first.
7. Change one variable at a time when correcting drift. Preserve the last approved voice ID, model/version, seed, identity block, and session settings.
8. Compare new takes against the same anchor and adjacent edited lines, not only against memory.
9. Record every selected take and any intentional exception.

Budget speech, meaningful internal pauses, turn-taking, physical action and holds on one scene timeline. Count concurrent actions once. A speaking-rate estimate is a diagnostic, not a universal target; prefer actual read-through or selected-audio duration. Flag timing conflicts without automatically accelerating speech or rewriting approved dialogue. A picture cut can occur during an unbroken line. Carry unfinished thoughts, breath and perspective across joins; do not restart them with each generated clip.

Calibration and retries are generation actions: plan them without submitting when the request is for templates or prompting only. For an existing approved film, compare against its selected anchor before considering new casting tests.

Do not promise exact reproducibility from prompt text alone. Consistency also depends on reusing the same provider voice, model/version, source reference, seed or speaker embedding when available, settings, pronunciation dictionary, and processing chain.

## Diagnose drift

Classify differences before fixing them:

- identity drift: timbre, pitch region, resonance, age presentation, or accent changes
- performance drift: intensity, pace, emphasis, breath, or status behavior misses the scene
- pronunciation drift: recurring words or phonemes vary
- recording drift: room, microphone distance, noise, EQ, or loudness changes
- edit drift: timing, pitch correction, time-stretching, or processing makes matching takes diverge

Return the smallest correction and preserve everything already approved.

## Deliver

Produce the voice bible, reusable identity prompt, per-scene performance prompts, pronunciation lexicon, take log, and consistency-QC checklist described in the reference. Keep generation prompts model-neutral unless the user names a tool or supplies its supported controls.
