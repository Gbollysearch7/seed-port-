---
name: film-video-prompter
description: Convert a directed film scene, shot plan and reference assets into model-specific AI video requests with timed action, dialogue, camera, sound and continuity; diagnose failed prompts and prepare controlled revisions. Use after the creative decisions exist, not as a substitute for story or cinematography development.
---

# Film Video Prompter

Compile the director's decisions into a request the chosen model can interpret. Preserve the scene's dramatic ambition while making its actions, references and constraints unambiguous.

## Establish what is being made

Read the current script, shot plan, look, asset versions, voice choices and user corrections. Separate approved decisions from draft options. If essential staging or spoken wording is missing, propose it before marking a request ready. A research or prompt-writing request does not itself authorize paid generation.

Keep creative decisions separate from API settings. Verify the exact provider/model/mode, duration and resolution, input roles and limits, supported audio controls and request cost before submission where the project's workflow requires it. A Higgsfield preset or Element name does not automatically exist in Atlas or another API. Never switch provider, model or mode just because a source example uses something else.

## Bind references to their jobs

Create an ordered asset manifest: file/version, subject, role and the submission slot. Identity, wardrobe, location, prop, composition and voice references can have different authority. If they conflict, resolve the conflict or state the intended priority clearly.

For this learner, wardrobe images are framed neck-down; portraits are separate. Bind the two images explicitly to the same complete character. This is a user preference to reduce ambiguity, not a proven universal rule. Preserve the canonical identity image; mark generative derivatives as new versions rather than pixel-identical crops.

A reference can guide a result without being its first frame. Use a start frame when it solves a concrete framing or continuity problem; do not require one when separate references suffice. Include only useful inputs, not the maximum allowed number.

## Write the minimum sufficient prompt

Use [the prompt assembly reference](references/prompt-assembly.md). For a simple image-to-video shot, focus on what moves and the required invariants. For interacting characters or multiple cuts, make the request self-contained: named people, start state, timed beats, speaker bindings, photographic choices, sound and end state.

Use chronological actions with contact and consequences. For an exchange, describe approach, contact, release and changed ownership. Keep a count of important objects through boundaries. Avoid rigid millisecond timing for every blink or breath; give crucial actions enough time and leave room for natural performance.

For multi-shot sequences, establish the purpose of each significant cut, its outgoing/incoming state, separate picture/audio boundaries and required source handles. A J-cut starts incoming audio before its picture; an L-cut carries outgoing audio over the incoming picture. Bind offscreen lines to the correct speaker and preserve sync. Separate editorial shots from generation jobs and cuts from camera movements. Where available, use film-editing for the coverage/cut plan before translating it into model-specific prompts.

Prefer positive descriptions of the desired result. Use short exclusions only for important failures, and a negative-prompt field only if supported. Do not turn advice about unwanted keyword associations into a claim that all negatives always fail. Do not impose a universal prompt token cap.

Specify camera behavior in terms of start/end framing, path and cue. Distinguish a move from a lens change. Put requested resolution in the API; aesthetic words such as 8K cannot upgrade a 480p render.

For footage intended to feel performed and photographed, use [the live-action realism rules](references/live-action-realism.md). Select the shot's relevant constraints rather than pasting a long universal negative list. Prioritise causal acting and listening, grounded contact, persistent identity and props, coherent geography, light and focus, correct speaker binding, and continuity through edits. Preserve expressive acting and necessary movement; do not eliminate them to make the shot easier. Grain, camera shake and smoothing are not substitutes for these decisions.

## Dialogue and sound

Use exact quoted lines, a stable speaker identity, addressee, delivery/task, listener behavior and a plausible speaking window. Read through the timing including breaths, pauses, action and responses. Do not remove requested dialogue for convenience.

Separate stable voice identity from changing performance. Reuse the selected source/settings when supported; text alone cannot guarantee the same voice. Choose native generated dialogue for an acting test, or a voice/audio-first route where exact delivery is essential and supported. A later dub must preserve synchronization or use a verified lip-sync workflow. Keep ambience, Foley, dialogue and music intentions distinct.

## Submission and iteration

Make generation requests only within the user's authorized scope. Save the exact prompt, settings, ordered references, job ID and versioned output. Preserve originals; a timeout in local polling is not a failed remote job. Resume it before considering another submission. Diagnose a failed take before proposing or spending on another; honor any project retry budget.

Use [the review and adapter reference](references/review-and-adapters.md) for provider translation and failure analysis. Review story comprehension, acting/listening, pacing, camera, continuity and sound as well as anatomy. Report what was actually viewed or heard. Sampled images cannot certify smooth motion, and audio metadata cannot certify dialogue.

For a live-action realism target, record a [take and sequence review](assets/take-review.md). Review full-speed playback with audio and joins in context when available; mark unavailable checks not checked and keep the result provisional. Note source/edit timecodes for material defects and choose the smallest useful correction. Do not certify realism from prompt wording, metadata, transcripts or contact sheets alone, or promise that footage is indistinguishable from a filmed performance. This is quality review, not an additional permission requirement for already authorised routine edits or an authorisation for paid retries.

## Deliver

Provide the request-ready prompt or generated result, reference manifest, checked settings and material open issues. Label mock requests and unrendered examples clearly. Separate a project's standing choices from reusable filmmaking principles when updating skills.
