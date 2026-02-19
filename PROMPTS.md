# StoryGraph Prompt Templates

Copy-paste these into Claude Code. Replace the bracketed parts with your specifics.

---

## 1. The Explorer — "What's the story in this data?"

```
Look at [FILE.csv / this DataFrame]. Read it, explore it, and tell me:

1. What is the single most surprising or important finding?
2. What would an executive care about most?
3. Where is the biggest gap between groups?

Then create the graph that tells the most impactful story. Use the austin_style_kit.
After that, suggest 3-5 follow-up graphs that would complete the full picture.
```

---

## 2. The Trend — "How has X changed over time?"

```
Using [DATA SOURCE], show me how [METRIC] has changed over [TIME PERIOD].

Make it a line chart. Annotate:
- The starting and ending values (direct labels, no legend)
- Any inflection points where the direction changed
- WHY it changed if the data suggests a reason

Title should be the insight, not "X over time".
Use austin_style_kit. Save as PNG.
```

---

## 3. The Comparison — "How does A compare to B?"

```
Using [DATA SOURCE], compare [GROUP A] vs [GROUP B] on [METRIC].

Choose the best chart type:
- If over time → dual lines with direct labels and gap shading
- If single point → horizontal bar, sorted, with highlight
- If before/after → slope chart

Gray out the less important group. Color the story.
Use austin_style_kit.
```

---

## 4. The Rank — "What are the top/bottom X?"

```
Using [DATA SOURCE], show me the top [N] and bottom [N] [THINGS] by [METRIC].

Horizontal bar chart, sorted. Highlight the extremes:
- Top performers in PALETTE positive (green)
- Bottom performers in PALETTE negative (orange)
- Everyone else in PALETTE neutral (gray)

Add value labels directly on bars. No axis needed if labels are clear.
Use austin_style_kit.
```

---

## 5. The Headline — "What's the key number?"

```
From [DATA SOURCE], what is the single most important number about [TOPIC]?

Display it as a big text visualization:
- The number large and bold in PALETTE primary
- Context below it in smaller neutral text
- If there's a change, show the direction (up/down arrow or %)

No chart — just the number and its context. Use austin_style_kit.
```

---

## 6. The Gap — "Is the gap growing or shrinking?"

```
Using [DATA SOURCE], show the gap between [GROUP A] and [GROUP B] over [TIME].

Dual line chart with:
- Shaded area between the lines showing the gap
- Direct labels (no legend)
- Annotation at the widest or narrowest point
- Title as insight: "The gap is [growing/shrinking/stable]..."

Use austin_style_kit.
```

---

## 7. The Breakdown — "What's the composition?"

```
Using [DATA SOURCE], break down [TOTAL METRIC] by [CATEGORIES].

Horizontal stacked bar or grouped bar. Show:
- Each category labeled directly (no legend)
- Percentages if they add to 100%
- The dominant category highlighted, rest in neutral

Use austin_style_kit.
```

---

## 8. The Multi-Story — "Give me the full picture"

```
I have [DATA DESCRIPTION / FILE]. I want the complete story.

Create a sequence of 4-5 charts that together tell the full narrative:

1. THE HEADLINE — Big number showing the key metric
2. THE TREND — How it got here (line chart with inflection annotations)
3. THE COMPARISON — Who's winning and losing (ranked bar)
4. THE GAP — Is inequality growing or shrinking (dual line with gap)
5. THE RECOMMENDATION — What should we do (annotated chart with call-to-action)

Each chart should use austin_style_kit. Each title should be an insight.
Present them in narrative order so they tell a story.
```

---

## 9. The Challenge — "Is that actually true?"

```
The common assumption is that [ASSUMPTION]. Using [DATA SOURCE], test this.

Create a chart that either confirms or challenges this assumption.
- If confirmed: title states it confidently, annotate the evidence
- If challenged: title says "Actually..." and highlight the surprise

Use austin_style_kit. Make the evidence undeniable.
```

---

## 10. The Before/After — "What changed?"

```
Using [DATA SOURCE], compare [BEFORE PERIOD] vs [AFTER PERIOD] for [METRIC].

Slope chart or paired bar chart showing:
- Clear before and after states
- Who improved vs who declined
- Winners in positive (green), losers in negative (orange)
- The event/cause annotated between the two states

Use austin_style_kit.
```

---

## Meta-Prompt: Making Any Question Better

When you're not sure what to ask, start with this:

```
I have [DATA DESCRIPTION]. I don't know what the story is yet.

Step 1: Read the data and give me a summary (rows, columns, ranges, any obvious patterns)
Step 2: Tell me the 3 most interesting findings you see
Step 3: For each finding, tell me what chart type would show it best
Step 4: Build the single most impactful chart
Step 5: Tell me what questions I should ask next
```
