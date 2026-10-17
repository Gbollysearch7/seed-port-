# Reference-to-video and vocal performance handoff

## Mode contract

Record the user's intended mode before selecting a provider. Reference-to-video uses identity, outfit, location and object images to guide a new moving scene. Those references need not define its first frame. An image animation / stills-to-video endpoint is a different mode; do not silently substitute it when the user specifies reference-to-video.

Before any authorized submission, inspect current documentation for the exact provider/model/mode: number and role of image references, audio input and synchronization support, supported duration and resolution, and any person/reference restrictions. Do not invent request fields. If one endpoint cannot combine identity, wardrobe and source-song audio, explain the gap and prepare a supported route; switching to a later lip-sync stage or a different provider needs to respect the user's existing authorization.

## Ordered reference roles

1. Canonical identity: face, hair, skin, tattoos and body identity; never replace with a celebrity reference.
2. Wardrobe: same character ID and selected look state; materials, silhouette, closures, shoes and accessories.
3. Location: geography, lighting anchors and material palette.
4. Hero object when handled or prominent: object design and ownership.
5. Audio excerpt only for actual sung performance when supported.

Priority is deliberate: identity controls the person, wardrobe controls clothing, location controls the environment. Reconcile conflicts before submission. A contact sheet should be labelled as a reference sheet so the model does not render its grid. Extracting an existing view for a supported input slot is ordinary preparation, not a new generative image; keep the parent reference and provenance.

## Singing close-ups

Use the original song excerpt rather than a generated voice or a paraphrase. Record source master, exact verified source in/out seconds, sample rate and channels, lead-in/tail handles, sung words, visible singer and the reference-to-video endpoint that supports the intended audio use. Treat a lyric sheet as wording authority, not timestamp authority.

Plan short, purposeful performance pockets. A face close-up can hold a whole phrase while narrative cutaways carry other lines. Keep the mouth unobstructed, specify natural breath and expression, and bind the artist as the only visible singer unless the plan explicitly includes others. Jewellery, neckline and skin highlights must remain stable while head, shoulders and fabric move naturally.

Uploading audio is not proof that a model will lip-sync it. An audio guide, generated soundtrack and audio-conditioned lip sync are different capabilities. Do not generate a replacement song, clone a voice or claim exact synchronization from a still review. No provider upload or paid generation follows merely from discussing a possible clip.

Verify actual output dimensions and normal-speed movement with sound when available. Report unreviewed playback rather than certifying realism from metadata. Preserve the project resolution preference; in FILMS X this is currently 480p unless explicitly changed.
