---
name: remove-ai-sins
description: Idempotent revision pass for literary and nonfiction prose. Invoke with /remove-ai-sins. Removes seven craft sins only — the not-X-but-Y frame, naming an emotion or theme the detail already carries, explaining an image or joke, inflated register, a summing-up ending, tying a raised question shut, and prose about the prose instead of the subject. If none of the seven are present, return the text unchanged. Do not restyle, do not add images or morals, do not apply general AI-slop lists (those are no-ai-slop / unslop). Use when asked to revise, restrain, unsin, strip craft sins, run a restraint pass, or when a draft needs those sins removed.
metadata:
  category: writing
  blurb: Idempotent pass that removes seven prose sins (antithesis frame, named feelings, glossed images, inflated register, moral endings, tied-off questions, meta overload) and otherwise leaves the draft alone.
  keywords:
    - writing
    - revision
    - restraint
    - ai-sins
    - frame
    - slop
    - nonfiction
    - prose
    - idempotent
---

# Remove AI sins

One pass. Remove the seven sins below. Touch nothing else.

This is not a rewrite, not Julian's three-pass polish, not unslop. Those improve writing. This one only takes sins out. A second run on the result must be a no-op.

The seven sins are the restraint layer (`name`, `explain`, `intensify`, `summary`, `resolve`) plus the antithesis frame ("not this but that") plus meta overload (prose about the prose).

## When

- The user invoked `/remove-ai-sins`.
- A draft of literary or narrative nonfiction exists and the job is to remove these sins.
- A continuation, chapter, or paragraph is full of frames, named feelings, glossed images, inflated register, or moral endings.

## Not

- First drafts. Write first, then run this.
- Annotation. Do not tag layers; edit the prose.
- General AI-slop (delve, foster, throat-clearing, emoji headings). Different skill.
- Flattening a writer's real diction. Distinctive words that are the voice stay. Intensify is inflating a *moment*, not deleting every uncommon word.
- Adding what the draft "should have said." No new events, objects, images, jokes, or morals.

## Contract

1. Read the whole draft before touching a sentence. Summary and resolve only fire at an ending. Explain needs the image it would gloss. Frame needs to know whether the denied X carries a fact.
2. Edit only spans that match a sin below. Prefer replace over cut for `frame`, `name`, `intensify`. Cut for `explain`, `summary`, `resolve`, `meta`. Replace for `meta` only when the staging carries a real claim the neighbors do not.
3. Keep content, order, voice, and claims. Word count may drop when a gloss or ending is cut. Never pad.
4. If a passage has no sin, leave it. Including every sentence of a paragraph that has a sin in only one sentence.
5. Stop. Do not "while you're at it" tighten, vary rhythm, swap synonyms, or fix commas.
6. Proof of idempotence: run the rules on your output in your head. If you would change anything, you already went too far. Undo the extra.

## Output

```
SINS: frame, name
```

or `SINS: none`, then a blank line, then the full revised draft and nothing else.

If the user asked for a detect-only pass, list each sin, quote the span, and stop. Do not rewrite.

---

## frame

The antithesis frame in any form:

- "not X but Y" / "not merely X; it was Y" / "wasn't just X, it was Y"
- "less X than Y" / "not as X but as Y"
- "X did not Y; it Z"
- split across two sentences: "It was not the wind. It was a song."

Rewrite as a plain statement of Y. Drop the denied X unless it carries a fact you would otherwise lose.

Not a frame: a "but" that continues or partitions ("They mapped the coast, but the mission was company for the captain"). A real contrast the sentence needs ("He was twenty-two, but he looks like a white-bearded ancient" is the book's joke, keep it).

### 1 — not merely / but

A 2018 study found that after the Laurentide Ice Sheet retreated, the trees that migrated faster were the promiscuous ones: species that can pair with many fungi, and so stood a better chance of meeting a partner in new ground.

**Sin**

This suggests that the post-glacial recovery was not merely a matter of seeds catching the wind, but a complex subterranean negotiation. A lone spruce seedling, thrust into a landscape of fresh sterile soil, was essentially alone. Its survival hinged not just on light and water, but on the invisible handshake with a partner it had never met.

**Revised**

This suggests that the post-glacial recovery was a subterranean negotiation as well as seeds catching the wind. A lone spruce seedling, thrust into a landscape of fresh sterile soil, was essentially alone. Its survival hinged on light, on water, and on the handshake with a partner it had never met.

The denied halves ("merely seeds", "just light and water") are not extra facts. Keep "seeds catching the wind" only because it is a fact the previous paragraph did not state.

### 2 — split sentence

Stamets found the *Grower's Guide* in a used bookstore in the late seventies and kept it on the bench where other people keep a bible.

**Sin**

For him the book was not merely a manual. It was a permission slip. It validated the hunch that the forest's machinery could be coaxed indoors.

**Revised**

For him the book was a permission slip. It validated the hunch that the forest's machinery could be coaxed indoors.

### 3 — wasn't just / it was

Garum factories of varying standards went up on the coasts of Pompeii, southern Spain, Leptis Magna, Clazomenae. Britain, which already made salt and exported fish, was probably in the trade too.

**Sin**

The stench, one imagines, was a distinct flavor of empire. It was not merely the smell of rot; it was industry, alchemy, the sea's flesh reduced to a pungent amber liquid that could turn bland porridge into something a senator would eat.

**Revised**

The stench, one imagines, was a distinct flavor of empire: rot and industry, the sea's flesh reduced to a pungent amber liquid that could turn bland porridge into something a senator would eat.

### 4 — less X than Y

You have a plan for the new boundary. In real life it will need tweaks. Come back to the steps as you find what is actually yours.

**Sin**

As you iterate, the initial stiffness of the new boundary softens into something more natural, less like a performance than a breath. The goal is not to become rigid, but to become resilient.

**Revised**

As you iterate, the initial stiffness of the new boundary softens. The goal is to become resilient.

"Less like a performance than a breath" is the same frame in metaphor clothes. Cut it. "Not rigid but resilient" is the same frame again.

### 5 — X did not Y; it Z

The little tiger could only bleat and nibble grass. The big one took him by the neck to a pond. There was no wind. The water was still.

**Sin**

The water did not show him a goat. It showed him a tiger. He watched the ripples expand and fade until the orange-and-white blur in the pond remembered how to be a predator.

**Revised**

The water showed him a tiger. He watched the ripples expand and fade until the orange-and-white blur in the pond remembered how to be a predator.

---

## name

An emotion, state, or term of art stated outright where the concrete detail already carries it. "A profound sense of loss." "Deeply depressed, lonely, ashamed." Replace with the detail, or delete the label and keep the detail that was already there.

Not a name sin: a quoted feeling that belongs to a source ("wonder, astonishment, and devotion" in Darwin's Brazil). A clinical or technical term the book is teaching. A feeling the narrator has not yet given you any other way to know.

### 1 — labeled attention

Gould named the white-throated caracara from Darwin's specimen, still in a paper sleeve in the British Museum. It is almost a dead ringer for an alkamari, except the white of the underbelly runs all the way to the chin.

**Sin**

Darwin noted the bird with a brevity that belied the taxonomic headache it would cause. He saw it perched on a thorny acacia, watching the guanacos with an expression of profound, rapt attention.

**Revised**

Darwin noted the bird with a brevity that belied the taxonomic headache it would cause. He saw it perched on a thorny acacia, watching the guanacos without turning its head or shifting its feet.

### 2 — depression named on top of the scene

I was spending most of my time at home wheezing, working, and eating three meals a day out of the same bowl while hunched over week-old newspapers on the couch. I was in a rut — physically, mentally, and otherwise.

**Sin**

I was spending most of my time at home wheezing, working, and eating three meals a day out of the same bowl while hunched over week-old newspapers on the couch. I was in a rut — physically, mentally, and otherwise — and, if I'm honest, deeply depressed, lonely, ashamed of what I'd become.

**Revised**

I was spending most of my time at home wheezing, working, and eating three meals a day out of the same bowl while hunched over week-old newspapers on the couch. I was in a rut — physically, mentally, and otherwise.

The bowl and the newspapers are the name. "Deeply depressed, lonely, ashamed" is the label stacked on top.

### 3 — injustice labeled

If a woman married "a foreigner" — someone from out of town — her children got a half portion, thirteen sameaux, and their descendants nothing. A man could marry an out-of-towner and keep the full share for himself and his heirs. In the fourteenth century there were 200 part-prenant families; by the Revolution, 800.

**Sin**

If a woman married "a foreigner" — someone from out of town — her children got a half portion, thirteen sameaux, and their descendants nothing. A man could marry an out-of-towner and keep the full share for himself and his heirs. It was blatant sexism, and the injustice bred lasting resentment among the women of the town. In the fourteenth century there were 200 part-prenant families; by the Revolution, 800.

**Revised**

If a woman married "a foreigner" — someone from out of town — her children got a half portion, thirteen sameaux, and their descendants nothing. A man could marry an out-of-towner and keep the full share for himself and his heirs. In the fourteenth century there were 200 part-prenant families; by the Revolution, 800.

### 4 — guilt named at the snares

It takes several days and a string of small planes and boats to reach them, but the thrill of seeing them again never fades: even after I've helped trap them with snares, weighed them in burlap sacks, taken blood from their wings, and clipped rings to their legs, I've watched them ruffle their feathers and walk back toward the same bait.

**Sin**

It takes several days and a string of small planes and boats to reach them, but the thrill of seeing them again never fades, and neither does the guilt: even after I've helped trap them with snares, weighed them in burlap sacks, taken blood from their wings, and clipped rings to their legs, I've watched them ruffle their feathers and walk back toward the same bait.

**Revised**

It takes several days and a string of small planes and boats to reach them, but the thrill of seeing them again never fades: even after I've helped trap them with snares, weighed them in burlap sacks, taken blood from their wings, and clipped rings to their legs, I've watched them ruffle their feathers and walk back toward the same bait.

The snares are already in the sentence. Do not name the feeling they imply.

### 5 — comfort in impermanence

When a Pacific breeze blows in, the shadows on the backyard wall reorganize into Edward Gorey gentlemen, then Escher staircases, then ferns and bougainvillea. I have been watching this for years.

**Sin**

The bougainvillea asserts itself one second and the next is a smear of color, a bruise on the white stucco. The trees sway with a certain deliberate grace. There is a comfort in the impermanence of it.

**Revised**

The bougainvillea asserts itself one second and the next is a smear of color, a bruise on the white stucco. The trees sway. It comes apart and comes back, all night.

---

## explain

An image, metaphor, joke, or implication followed by a sentence or clause that spells out what it meant. "...like a cathedral. It was a sacred place." "..., which is to say he was afraid." Delete the explaining sentence or clause. Keep the image.

Not explain: an appositive that *names* a thing ("terra preta, anthropogenic dark earth"). A definition the book is introducing. A fact the image does not contain. The 2026-09-16 audit: 92% of a bad editor's "explain" cuts were appositives. Do not repeat that.

### 1 — which is to say

I didn't mention any of it to family or friends. I spent the next several years trying to figure out what had happened. Over that span I fixed up the house, got out of my funk, and got a lead.

**Sin**

Over that span of time I fixed up my house and got out of my funk, which is to say the depression that bad breathing had dragged me into finally lifted once I started breathing better. Then I got a lead. I went to Greece to write a story on freediving — which is to say, the people who had already solved my problem.

**Revised**

Over that span of time I fixed up my house, got out of my funk, and got a lead. I went to Greece to write a story on freediving, the ancient practice of diving hundreds of feet below the water's surface on a single breath of air.

### 2 — in other words after a list

The Diamond Crystal Salt Company of St. Clair, Michigan, published a booklet in the 1920s: "One Hundred and One Uses for Diamond Crystal Salt." The list included keeping boiled vegetables bright, making ice cream freeze, removing rust, sealing cracks, putting out grease fires, killing poison ivy, and treating dyspepsia, sprains, sore throats, and earaches.

**Sin**

The list included keeping boiled vegetables bright, making ice cream freeze, removing rust, sealing cracks, putting out grease fires, killing poison ivy, and treating dyspepsia, sprains, sore throats, and earaches. In other words, salt was being sold as a universal remedy, a substance so useful in the kitchen, the parlor, and the sickroom that no household could reasonably do without it.

**Revised**

The list included keeping boiled vegetables bright, making ice cream freeze, removing rust, sealing cracks, putting out grease fires, killing poison ivy, and treating dyspepsia, sprains, sore throats, and earaches.

The list is the joke. Do not score it.

### 3 — the point is

"I can very plainly see," Darwin wrote his sister, "there will not be much pleasure or contentment, till we get out of these detestable latitudes & are carrying on all sail to the land where Bananas grow."

**Sin**

"I can very plainly see," he confided in a letter to his sister, "there will not be much pleasure or contentment, till we get out of these detestable latitudes & are carrying on all sail to the land where Bananas grow." The homesick longing for the tropics is the complaint of a boy on a holiday gone wrong, not of a great man of science, and that is the point: it can be hard to picture Darwin as anything but a white-bearded ancient with a thousand-yard stare, when in fact he was twenty-two, a rich kid with an assured future as a country priest.

**Revised**

"I can very plainly see," he confided in a letter to his sister, "there will not be much pleasure or contentment, till we get out of these detestable latitudes & are carrying on all sail to the land where Bananas grow." It can be hard to picture Darwin as anything but a white-bearded ancient with a thousand-yard stare, but when the *Beagle* left England he was only twenty-two, a rich kid with an assured future as a country priest.

The bananas letter already does the joke. Do not announce it.

### 4 — irony flagged

Around 11,000 B.C. the Ice Age ended. At about this time the Asiatic wolf, a fierce predator that would eat a human if it had the chance, came under human control because its cubs could be fed and trained. A dangerous adversary was turned into a dedicated helper — the dog.

**Sin**

A dangerous adversary was turned into a dedicated helper — the dog. The irony is plain: the very animal that once hunted us now guards us, the enemy remade into the friend. As glaciers melted, huge fields of wild grain appeared.

**Revised**

A dangerous adversary was turned into a dedicated helper — the dog. As glaciers melted, huge fields of wild grain appeared.

### 5 — image then gloss

They had been walking since dawn. By the time they reached the ridge the valley below looked like a table set and then abandoned, the river a dropped napkin, the homesteads crumbs.

**Sin**

By the time they reached the ridge the valley below looked like a table set and then abandoned, the river a dropped napkin, the homesteads crumbs. It was a landscape of leftover lives, which is to say everyone who had lived there was gone.

**Revised**

By the time they reached the ridge the valley below looked like a table set and then abandoned, the river a dropped napkin, the homesteads crumbs.

---

## intensify

A big moment written in plain, small language — or a fact that could have been theatrical — gets inflated: grand words where plain ones serve, stacked adjectives, adverbs of degree, a dedicated drumroll for something the sentence had already demoted.

Replace one-for-one with the plain word. Do not rewrite the scene.

Not intensify: a writer's ordinary unusual word ("wasp-waisted islands", "mighty Pacific swells" in a book that talks that way). The test is whether the *moment* got bigger than the book allowed, not whether a thesaurus would prefer "walk" to "soaring."

### 1 — thesaurus over a still landscape

Without ants or termites to mill them down, Tierra del Fuego's dead trees stand and lie beside the living for years, and crow-sized woodpeckers knock splinters from their trunks with the dull thunk of hatchets.

**Sin**

Even now, when one may traverse the length of Darwin's five-year odyssey in a mere two days, Tierra del Fuego's mist-shrouded channels remain seldom frequented, largely unattainable, and since the extinction of the Amerindians who dwelt there for millennia, depopulated. Vessels occasionally employ them as refuge from the mighty Pacific swells, but scarcely anyone tarries.

**Revised**

Even now, when you can fly the length of Darwin's five-year odyssey in two days, Tierra del Fuego's fog-bound channels are seldom visited, largely inaccessible, and since the demise of the Amerindians who lived there for thousands of years, unpeopled. Ships occasionally use them to shelter from the mighty Pacific swells, but almost no one lingers.

One-for-one. "Mighty" stays: it is the book's word, not the inflation.

### 2 — a broken neck written up

The penguin's foot was still in his crop. He wasn't obviously dehydrated, or visibly diseased. Then she turned her attention to his head, pressing up on his lower mandible.

**Sin**

Then she turned her attention to his head, pressing up on his lower mandible — and with a wet, sickening give, his skull flopped backward, the column of the neck undone.

"There you go," she said softly. "His neck's been snapped clean through."

**Revised**

Then she turned her attention to his head, pressing up on his lower mandible, and his skull flopped backward.

"There you go," she said. "His neck's broken."

### 3 — war promoted out of a clause

Aging Land Rovers trundled through the streets on the left, and English was the official language. In the time since Darwin's visit, humans have transformed the Falklands' two large islands.

**Sin**

In the time since Darwin's visit, humans have transformed the Falklands' two large islands. In 1982 a war was fought here, brutal and short, young men dying in burning ships and freezing holes, and the islands have never been the same.

**Revised**

In the time since Darwin's visit, humans have transformed the Falklands' two large islands, including a war in 1982.

The published move is the demotion: the war lives in a clause, not a paragraph of flames.

### 4 — adverbs of degree

He spent the day hurling rocks at them, recovering his club, and left twelve dead birds on the beach.

**Sin**

He spent the day hurling rocks at them in a rising fury, recovering his club again and again, and left twelve utterly ruined birds on the beach, a slaughter he would not let himself name.

**Revised**

He spent the day hurling rocks at them, recovering his club and leaving twelve dead birds on the beach.

### 5 — a farewell written as an epic

I've come here to see where all this air is supposed to enter our bodies. And I've come to say goodbye to my nose for the next ten days.

**Sin**

I have journeyed hither to perceive, apprehend, and comprehend where all this atmosphere is destined to enter our corporeal forms. And I have journeyed hither to bid farewell to my nose for the ensuing ten days.

**Revised**

I've come here to see, feel, and learn where all this air is supposed to enter our bodies. And I've come to say goodbye to my nose for the next ten days.

Cartoon thesaurus is still intensify. Same fix: one-for-one, back to the plain word.

---

## summary

The last sentence or two of a stretch sum up, moralize, or tell the reader what the details added up to. Only the ending counts. Cut or replace the summing-up so the passage ends on a fact, an image, or a quote.

Not summary: a mid-paragraph claim. A first sentence that says what the next paragraph will do. A caption that is only a caption.

When `summary` and `explain` both fit, paragraph end is `summary` unless the missing sentence is a fact the reader must supply. When `summary` and `intensify` both fit, `intensify` if the refusal is the register of the last sentence, `summary` if it is the absence of a next sentence.

### 1 — scene ends on the log

The black plastic ring I'd fastened to his leg a few weeks earlier, with its yellow letter and number, was good as new. I opened my notebook.

**Sin**

The black plastic ring I'd fastened to his leg a few weeks earlier, with its yellow letter and number, was good as new. I opened my notebook.

3 September 2012, I wrote. Found a body. I had lost him, and the work felt suddenly small.

**Revised**

The black plastic ring I'd fastened to his leg a few weeks earlier, with its yellow letter and number, was good as new. I opened my notebook.

3 September 2012, I wrote. Found a body.

### 2 — in other words, a scientific voyage

He was twenty-two, a rich kid with an assured future as a country priest. He'd been invited aboard as much to keep the ship's melancholy young captain company as to advance the cause of science, and his unpaid role as a naturalist was incidental to the ship's official mission of mapping the treacherous coasts at the southern tip of South America.

**Sin**

He'd been invited aboard as much to keep the ship's melancholy young captain company as to advance the cause of science, and his unpaid role as a naturalist was incidental to the ship's official mission of mapping the coasts of southern South America. In other words, the voyage that would remake biology was, at its outset, nobody's idea of a scientific expedition.

**Revised**

He'd been invited aboard as much to keep the ship's melancholy young captain company as to advance the cause of science, and his unpaid role as a naturalist was incidental to the ship's official mission of mapping the treacherous coasts at the southern tip of South America.

### 3 — we have been losing the skill

Few of these scientists set out to study breathing. But, somehow, breathing kept finding them. They discovered that our capacity to breathe has changed through the long processes of human evolution, and that the way we breathe has gotten markedly worse since the dawn of the Industrial Age.

**Sin**

They discovered that our capacity to breathe has changed through the long processes of human evolution, and that the way we breathe has gotten markedly worse since the dawn of the Industrial Age. In other words, breathing is no fixed biological given but a skill our species has been steadily losing.

**Revised**

They discovered that our capacity to breathe has changed through the long processes of human evolution, and that the way we breathe has gotten markedly worse since the dawn of the Industrial Age.

### 4 — the customs-house joke scored

In the nineteenth century, when mummies from Saqqara and Thebes were taken from tombs and brought to Cairo, they were taxed as salted fish before being permitted entry to the city.

**Sin**

In the nineteenth century, mummies brought from tombs to Cairo were taxed as salted fish. The joke of the customs house was really a recognition of chemistry: flesh cured in salt is flesh cured in salt, whatever its species or its sanctity.

**Revised**

In the nineteenth century, when mummies from Saqqara and Thebes were taken from tombs and brought to Cairo, they were taxed as salted fish before being permitted entry to the city.

### 5 — industry announced

Li Bing found that the natural brine did not originate in the pools where it was found but seeped up from underground. In 252 B.C. he ordered the drilling of the world's first brine wells.

**Sin**

In 252 B.C. he ordered the drilling of the world's first brine wells. Salt would no longer be merely gathered where nature happened to offer it; it could now be hunted deliberately, beneath the earth, which was the beginning of an industry.

**Revised**

In 252 B.C. he ordered the drilling of the world's first brine wells.

The last sentence of the sin is also a frame. Ending sins win at the ending: cut it.

---

## resolve

A tension or mystery the text itself opened is closed too neatly. A last sentence that ties the bow. Leave it open; end on the detail.

Not resolve: a question the text never raised. A fact the next paragraph will need. A preview of a later chapter with no dwelling. `summary` is "what this scene meant." `resolve` is "here is the answer to the thing I asked."

### 1 — three questions paid in the same breath

All the while I'd be thinking of Darwin's unanswered questions, and a few of my own:

Why are you like this? Why are there so few of you? How did you come to be?

**Sin**

Why are you like this? Why are there so few of you? How did you come to be? The answers, I would learn, were diet, isolation, and a split in the falcon line some ten million years back. Each time I've tugged on these threads, their story has grown larger and wilder than I could have imagined.

**Revised**

Why are you like this? Why are there so few of you? How did you come to be?

Each time I've tugged on these threads, their story has grown larger and wilder than I could have imagined.

### 2 — the cause of death supplied

At first this seemed to confirm what we all suspected: that he'd tangled with something on the beach.

**Sin**

At first this seemed to confirm what we all suspected: that he'd tangled with a sea lion. He had. The necropsy said so, and the story of G7 ends there, a young bird who guessed wrong.

**Revised**

At first this seemed to confirm what we all suspected: that he'd tangled with something on the beach.

(If the draft never raised the question, there is nothing to leave open. Do not delete a cause of death the passage was always going to give. This sin is paying a hold the prose itself installed.)

### 3 — the debate declared settled

Over the centuries many popular uprisings protested the salt monopoly, including an angry mob that took over Xi'an in 880. And the other great moral and political questions of the debate on salt and iron — the need for profits, the rights of nobility, aid to the poor, a balanced budget, the tax burden, the risk of anarchy, the line between law and tyranny — have all remained unresolved issues.

**Sin**

And the other great moral and political questions of the debate on salt and iron — the need for profits, the rights of nobility, aid to the poor, a balanced budget, the tax burden, the risk of anarchy, the line between law and tyranny — were all settled long ago, in favor of the state.

**Revised**

And the other great moral and political questions of the debate on salt and iron — the need for profits, the rights of nobility, aid to the poor, a balanced budget, the tax burden, the risk of anarchy, the line between law and tyranny — have all remained unresolved issues.

### 4 — tears explained as chemistry

What exactly had happened? How did sitting cross-legged in a funky house and breathing for an hour trigger such a profound reaction? I returned to the breathing class the next week: same experience, fewer waterworks.

**Sin**

What exactly had happened? How did sitting cross-legged in a funky house and breathing for an hour trigger such a profound reaction? The answer, I'd learn, was simple: heavy breathing had flushed carbon dioxide from my blood, constricting vessels, flooding my brain with a chemical panic that my body released as tears. Nothing mystical, just gas exchange. I returned to the class the next week: same experience, fewer waterworks, and now I knew why.

**Revised**

What exactly had happened? How did sitting cross-legged in a funky house and breathing for an hour trigger such a profound reaction? I returned to the breathing class the next week: same experience, fewer waterworks.

### 5 — the rumor confirmed

Crested caracaras in Patagonia are said to spread wildfires by dropping burning sticks in dry grass, and feast on the ensuing stream of refugees. Despite these behaviors, scientists and falconers from the northern world have largely ignored them.

**Sin**

Crested caracaras in Patagonia are said to spread wildfires by dropping burning sticks in dry grass. Scientists ignored them for a simple reason: they scavenge, and scavengers were held to be cowards. That prejudice has finally lifted. Today they are studied as among the most inventive problem-solvers in the bird world.

**Revised**

Crested caracaras in Patagonia are said to spread wildfires by dropping burning sticks in dry grass, and feast on the ensuing stream of refugees. Despite these behaviors, scientists and falconers from the northern world have largely ignored them. Even Darwin called them "false eagles" who "ill become so high a rank," and a sense that there's something unwholesome or disappointing about them has been slow to ebb.

"Are said to" is the open thing. Do not close it. Do not rehabilitate them in the last sentence.

## meta

A sentence about the prose instead of the subject. "That is where the simple sentence ends and the useful one begins." "They are the finding." "So much for the map; now for the clock." The subject of the sentence is the draft itself: what was said, what comes next, which part matters. Delete it and let the announced sentence do the work. Some meta is load-bearing navigation in long exposition; this sin is the overload, the staging that carries no information the neighbors do not.

Fix is cut, or shrink to the real claim when the staging carries one the neighbors lack. "The best evidence comes from the places where the simple story strained" keeps its claim and loses its staging. If deletion would strand the reader or remove a fact, it is navigation, not overload. Leave it.

Not a meta sin: a sentence that says what the next passage will do when the passage needs it ("Three burns per life period follow, from childhood to adulthood"). A heading or caption. A first-person admission that does narrative work ("I went to Greece to write about freediving"). `explain` glosses backward, what the image meant; `meta` glosses forward or sideways, what the prose is doing. When both fit, `meta` wins if the sentence is about the draft, `explain` if it is about the world.

### 1 — where the simple sentence ends

Ultraviolet radiation in sunlight causes most cutaneous melanoma. A global model attributed 267,353 of the 331,722 melanomas estimated for 2022 to UV, about four in five.

**Sin**

That is where the simple sentence ends and the useful one begins: the exposure that matters most is intense, intermittent, and burning, on skin that tans poorly.

**Revised**

The exposure that matters most is intense, intermittent, and burning, on skin that tans poorly.

The staging names two sentences and adds no fact. The useful sentence survives on its own.

### 2 — they are the finding

The short answer assumes all sun exposure is the same exposure. It assumes all people respond to it the same way. It assumes all melanomas are the same tumor.

**Sin**

None of those is close to true, and the corrections are not footnotes. They are the finding.

**Revised**

None of those is close to true.

The second sentence judges the paragraph's own importance. Cut it; the paragraph already said the thing.

### 3 — the key to everything that follows

For lentigo maligna, the slow tumor of weathered faces, the same data ran the other way. There, risk tracked the whole length of a life outdoors.

**Sin**

That split is the key to almost everything that follows. Melanoma is at least two diseases wearing one name, and they keep different time.

**Revised**

Melanoma is at least two diseases wearing one name, and they keep different time.

The first sentence announces the importance of the sentence beside it. The sentence beside it is the importance.

### 4 — shrink to the claim

In 1985 the Buffalo study found that light-complexioned men with the most lifetime hours in the sun had a fraction of the melanoma risk of men with the least.

**Sin**

The best evidence for each correction comes from the places where the simple story visibly strained: the studies that seemed to let the sun off the hook.

**Revised**

The studies that seemed to let the sun off the hook are the ones to take seriously first.

The staging carried a real claim about where to look. Keep the claim, drop the draft talking about itself.

### 5 — navigation stays

A methods section has named three exposure classes: remembered summers, job titles, place-level light. The next three paragraphs take them in order.

Not a sin. This sentence is navigation, and the paragraphs below need it:

Remembered summers came first, in the case-control interviews of the early eighties. Job titles came next, in the occupational cohorts. Place-level light came last, in the registry comparisons.

A roadmap that tells the reader where a long passage is going is allowed. Meta fires only when the sentence can be deleted without stranding anyone.

---


## Idempotence example

Run the pass on this. It has none of the seven.

Even now, when you can fly the length of Darwin's five-year odyssey in two days, Tierra del Fuego's fog-bound channels are seldom visited, largely inaccessible, and since the demise of the Amerindians who lived there for thousands of years, unpeopled. Ships occasionally use them to shelter from the mighty Pacific swells, but almost no one lingers. Nor do the winds.

**Output**

```
SINS: none

Even now, when you can fly the length of Darwin's five-year odyssey in two days, Tierra del Fuego's fog-bound channels are seldom visited, largely inaccessible, and since the demise of the Amerindians who lived there for thousands of years, unpeopled. Ships occasionally use them to shelter from the mighty Pacific swells, but almost no one lingers. Nor do the winds.
```

"Mighty" stays. "Nor do the winds" stays. A second run changes nothing.

---

## Pitfalls (from the training work)

- **Appositives are not explain.** "terra preta, anthropogenic dark earth" stays. Explain is the sentence after an image that tells you what the image meant.
- **Do not flatten voice.** Intensify is a moment written too big, not a ban on the book's words.
- **Endings only at endings.** `summary` and `resolve` do not fire mid-stretch. If you cut a moral in paragraph two, you invented a sin.
- **Frame is antithesis, not every but.** "They mapped the coast, but the real job was company" is a partition. Leave it.
- **Quoted feelings stay.** Darwin's "wonder, astonishment, and devotion" is his sentence, not yours to un-name.
- **Meta is overload, not all navigation.** Some prose about the prose is load-bearing. Fire only when deletion loses nothing and strands nobody. A roadmap a long passage needs stays.
- **One sin per span, worst one if several fire.** At an ending, `resolve` beats `summary` when the open thing is a question the text raised. `intensify` beats `summary` when the refusal is the register of the last sentence. `name` beats `summary` at a paragraph end when the refusal is a specific unnamed feeling.
- **Do not run unslop in the same pass.** Banned-word lists will eat "tapestry" in a rug and "foster" in a foster parent. Different job.

## Workflow

1. Read the whole draft.
2. Walk it once, marking candidate spans against the seven. When unsure, leave it.
3. Edit only those spans, smallest change.
4. Re-read the result as if it were the input. If you would edit again, you overshot.
5. Emit `SINS:` then the full draft.
