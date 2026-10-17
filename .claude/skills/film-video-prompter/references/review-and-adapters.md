# Review and provider adaptation

## Provider adapter

Keep the artistic specification stable while translating the interface:

| Concept | Verify before use |
|---|---|
| Named character or location | Does the provider resolve names automatically, or must ordered image slots be supplied? |
| First/last frame | Is this a dedicated image field, an ordinary reference, or unsupported? |
| Prior video | Does phrasing trigger editing/extension rather than new reference-guided generation? |
| Camera or lens | Is there an actual setting, a preset, or only prose? |
| Dialogue/audio | Native speech toggle, reference audio, saved voice ID, and lip-sync support differ. |
| Runtime/output | Use live supported values; distinguish native output from upscale/enhancement. |
| Cost | Estimate with actual settings; label estimated versus settled charge. |

At the 6 September 2026 Atlas check, `bytedance/seedance-2.5/reference-to-video` supported 15-second native 480p with `ratio: 16:9`, `generate_audio: true`, ordered `reference_images`, and `@Image1` syntax. This is a dated example, not a permanent schema. [Atlas model](https://www.atlascloud.ai/models/bytedance/seedance-2.5/reference-to-video), [billing](https://www.atlascloud.ai/docs/billing/model-billing).

## Failure diagnosis

| Observed problem | Investigate first | Candidate correction |
|---|---|---|
| Attractive but inert | No changing tactic, attention or relationship | Restage the scene or give the listener work; do not merely add adjectives. |
| Unmotivated camera | Move unrelated to action or information | Choose a start/end reveal or a deliberate hold. |
| Wrong person speaks | Ambiguous face/voice/speaker binding | Separate speaker IDs and turn windows; test a short exchange. |
| Rushed delivery | Too much speech/action for the window | Shorten lines or expand coverage/runtime within user constraints. |
| Reference collage appears | Mixed identity/composition roles | Supply relevant individual views and name their roles. |
| Room or screen-direction drift | Missing geography or incompatible references | Correct the spatial plan and input conflict. |
| Food/prop multiplication | No explicit ownership/contact transition | Specify physical transfer and resulting count. |
| Voice changes between clips | New identity interpretation/settings | Reuse the selected audio source and identity configuration. |

When a tool cannot support continuous playback or listening, retain a provisional review and state the limitation. Never turn an unperformed check into a pass.

## Research cautions

[Higgsfield's public prompt guidance](https://github.com/higgsfield-ai/skills/blob/main/higgsfield-generate/references/prompt-engineering.md) favors brief inputs, while [its Seedance 2.5 film guide](https://higgsfield.ai/blog/seedance-2-5-prompting-guide) uses extended structured examples. Adapt length to task complexity. The [Cinema Studio examples](https://higgsfield.ai/blog/cinema-studio-3.0) include both start-frame and Elements-only workflows; their product behavior is not a guarantee about other APIs. [Voice consistency guidance](https://higgsfield.ai/blog/consistent-ai-voice-across-videos) supports reusable sources/settings, but stable identity must still allow an actor's performance to change.
