generate_eight_activities = """
Your job is to help generate different kinds of activities for users of a personality-related application given high or low scores for a particular trait.

There are two kinds of activities to be generated, **timed activities** and **reflections**.

Timed activities tell the user to do/practice/implement/observe/notice something in their life over the next N hours. N can range from one day to one week, but shouldn't be longer or shorter than this. Be sure to give people an appropriate amount of time to do the activity. It should be something that the user can accomplish in the course of their normal daily/weekly activities in their normal work/home/social life.
Vague example of a timed activity: "Over the next 24 hours, try to do X."

Reflections are essentially writing prompts that the user will take on as soon as they are presented with them.

You will be asked to generate a 'HARNESS ADVANTAGES' and 'ADDRESS DISADVANTAGES' version for each activity type x trait value. 
A HARNESS ADVANTAGES version means an activity that plays on whatever STRENGTHS/ADVANTAGES might be associated with being at that level (HIGH OR LOW) for that trait. 
An ADDRESS DISADVANTAGES version means a GROWTH-BASED activity that plays on the potential WEAKNESSES/DISADVANTAGES of being at that level (HIGH OR LOW) for that trait.

IMPORTANT NOTE: for HARNESS ADVANTAGES TIMED ACTIVITIES, we might generally want to do observational-type activities given that we are NOT asking the user to implement some new behavior given that it is supposed to be harnessing already-existing advantages!

We will be generating activities related to trait {SCALE}. 
Example items that comprise this trait in our application are as follows (some may be reverse-scored): {ITEMS}

When creating the activities, you should find a way to pose them without necessarily invoking the actual word {SCALE} unless it is essential to understanding the question.
Also, be sure not to make the activities sound patronizing, judgy, or condescending.

Your job is to generate EIGHT activities related to trait {SCALE}:
1a. One 'HARNESS ADVANTAGES' TIMED ACTIVITY for someone HIGH in trait {SCALE}
1b. One 'ADDRESS DISADVANTAGES' TIMED ACTIVITY for someone HIGH in trait {SCALE}

2a. One 'HARNESS ADVANTAGES' TIMED ACTIVITY for someone LOW in trait {SCALE}*
2b. One 'ADDRESS DISADVANTAGES' TIMED ACTIVITY for someone LOW in trait {SCALE}

3a. One 'HARNESS ADVANTAGES' REFLECTION for someone HIGH in trait {SCALE}
3b. One 'ADDRESS DISADVANTAGES' REFLECTION for someone HIGH in trait {SCALE}

4a. One 'HARNESS ADVANTAGES' REFLECTION for someone LOW in trait {SCALE}*
4b. One 'ADDRESS DISADVANTAGES' REFLECTION for someone LOW in trait {SCALE}

*CRITICAL NOTE ON 2A AND 4A: IT MAY WELL BE EASIER TO COME UP WITH 'ADDRESS DISADVANTAGES' THAN 'HARNESS ADVANTAGES' ACTIVITIES FOR BEING LOW IN {SCALE}, BUT YOU MUST AVOID MIXING THESE UP.

FORMATTING REQUIREMENTS:
You will have two outputs:
OUTPUT 1—IDEATION: you should briefly reason generally about the four possibilities, apart from generating specific activities. You should think about the 'ADDRESS DISADVANTAGES' and 'HARNESS ADVANTAGES' for being HIGH and LOW in the trait.
You tend to have trouble coming up with 'ADDRESS DISADVANTAGES' of being HIGH in 'good' traits and the 'HARNESS ADVANTAGES' of being LOW in 'good' traits (and the converse for 'bad' traits), so be sure to overcome this and dig deep (succinctly) in your reasoning.
ALWAYS begin this part with 'IDEATION:"

OUTPUT 2—ACTIVITIES:
THEN, using your IDEATION as direct inspiration, generate the associated activities, being sure that they accord with the instructions and your IDEATION.

Format each of the eight activities as a separate block, using a key-value pair format like this (this is just one example):

{{
  "Activity Type": "TIMED ACTIVITY",
  "Trait": {SCALE} 
  "Trait Level": "HIGH",
  "Title": "Simple, unique, natural-sounding title/headline/encapsulation/foretaste of the activity; 30 characters MAX, with no word more than 10 characters (for formatting reasons). DON'T MAKE IT TOO 'TITLE-Y', AND IT SHOULD NOT USE THE WORDS TIMED, ACTIVITY, REFLECTION",
  "Description": "3 solid sentences that give the motivation/framing/introduction of why this activity might be relevant to someone who is low/high in {SCALE}.",
  "Activity": "The actual content of the activity; 1-2 sentences, being sure it accords with the categorization and desired content",
  "Categorization": "HARNESS ADVANTAGES/ADDRESS DISADVANTAGES",
  "Domain": "Self/Relationships/Purpose (whichever seems closest, this categorization is not a big deal)"
}}

Emphasizing that the description should be longer than the activity itself. IT MUST BE THREE FULL SENTENCES OF BACKGROUND/CONTEXT; ANYTHING SHORTER IS UNACCEPTABLE!

YOU SHOULD RETURN EIGHT SUCH ENTRIES FOR THE EIGHT ACTIVITIES IN EXACTLY THIS FORMAT AS A SINGLE JSON ARRAY, EXACTLY LIKE SO:

ACTIVITIES:
[
  {{
    "Activity Type": "TIMED ACTIVITY",
    "Trait": "Dutiful",
    "Trait Level": "HIGH",
    ...
  }},
  {{
    "Activity Type": "TIMED ACTIVITY",
    "Trait": "Dutiful",
    "Trait Level": "LOW",
    ...
  }},
  ...
]

Do not wrap this in ```json ```, just give the pure content of the array. Be sure to precede the array with the exact string 'ACTIVITIES:' so the output can be processed correctly.

YOUR OUTPUTS:
"""





generate_eight_activities_OLD = """
Your job is to help generate different kinds of activities for users of a personality-related application given high or low scores for a particular trait.

There are two kinds of activities to be generated, **timed activities** and **reflections**.

Timed activities tell the user to do/practice/implement something in their life over the next N hours. N can range from one day to one week, but shouldn't be longer or shorter than this. Be sure to give people an appropriate amount of time to do the activity. It should be something that the user can accomplish in the course of their normal daily/weekly activities in their normal work/home/social life.
Vague example of a timed activity: "Over the next 24 hours, try to do X."

Reflections are essentially writing prompts that the user will take on as soon as they are presented with them.

You will be asked to generate a POSITIVE and NEGATIVE version for each activity type x trait value. 
A POSITIVE version means an activity that plays on whatever STRENGTHS/ADVANTAGES might be associated with being at that level (HIGH OR LOW) for that trait.
A NEGATIVE version means a GROWTH-BASED activity that plays on the potential WEAKNESSES/DISADVANTAGES of being at that level (HIGH OR LOW) for that trait.

We will be generating activities related to trait {SCALE}. 
Example items that comprise this trait in our application are as follows (some may be reverse-scored): {ITEMS}

When creating the activities, you should find a way to pose them without necessarily invoking the actual word {SCALE} unless it is essential to understanding the question.
Also, be sure not to make the activities sound patronizing, judgy, or condescending.

Your job is to generate EIGHT activities related to trait {SCALE}:
1a. One POSITIVE TIMED ACTIVITY for someone HIGH in trait {SCALE}
1b. One NEGATIVE TIMED ACTIVITY for someone HIGH in trait {SCALE}

2a. One POSITIVE TIMED ACTIVITY for someone LOW in trait {SCALE}*
2b. One NEGATIVE TIMED ACTIVITY for someone LOW in trait {SCALE}

3a. One POSITIVE REFLECTION for someone HIGH in trait {SCALE}
3b. One NEGATIVE REFLECTION for someone HIGH in trait {SCALE}

4a. One POSITIVE REFLECTION for someone LOW in trait {SCALE}*
4b. One NEGATIVE REFLECTION for someone LOW in trait {SCALE}

*CRITICAL NOTE ON 2A AND 4A: IT MAY WELL BE EASIER TO COME UP WITH NEGATIVE THAN POSITIVE ACTIVITIES FOR BEING LOW IN {SCALE}, BUT THIS DOESN'T MATTER. 
DIG DEEP TO COME UP WITH ACTIVITIES/REFLECTIONS THAT INDEED PLAY ON THE *STRENGTHS* OF BEING LOW IN {SCALE} FOR 2A AND 4A! DO NOT ERRONEOUSLY SMUGGLE IN YOUR OWN VALUES INTO THESE QUESTIONS, AND JUST DO THE TASK AS INSTRUCTED.

FORMATTING REQUIREMENTS:
You will have two outputs:
OUTPUT 1—IDEATION: you should briefly reason generally about the four possibilities, apart from generating specific activities. You should think about the STRENGTHS (advantages) and WEAKNESSES (disadvantages) of being HIGH and LOW in the trait.
You tend to have trouble coming up with WEAKNESSES of being HIGH in 'good' traits and the STRENGTHS of being LOW in 'good' traits (and the converse for 'bad' traits), so be sure to overcome this and dig deep (succinctly) in your reasoning.
RECALL BOTH IN THIS AND IN THE NEXT OUTPUT THAT A 'POSITIVE' ACTIVITY SHOULD PLAY ON EXISTING STRENGTHS/ADVANTAGES OF THAT TRAIT LEVEL, WHILE A 'NEGATIVE' ACTIVITY SHOULD PLAY ON THE WEAKNESSES/DISADVANTAGES OF THAT TRAIT LEVEL. DON'T MIX THESE UP!

ALWAYS begin this part with 'IDEATION:"

OUTPUT 2—ACTIVITIES:
Format each of the eight activities as a separate block, using a key-value pair format like this (this is just one example):

{{
  "Activity Type": "TIMED ACTIVITY",
  "Trait": {SCALE} 
  "Trait Level": "HIGH",
  "Title": "Simple, unique, natural-sounding title for the activity; 30 characters MAX, with no word more than 10 characters (for formatting reasons). SHOULD NOT USE THE WORDS TIMED, ACTIVITY, REFLECTION",
  "Description": "3 solid sentences that give the motivation/framing/introduction of why this activity might be relevant to someone who is low/high in {SCALE}.",
  "Activity": "The actual content of the activity; 1-2 sentences",
  "Categorization": "Positive/Negative",
  "Domain": "Self/Relationships/Purpose (whichever seems closest, this categorization is not a big deal)"
}}

Emphasizing that the description should be longer than the activity itself. IT MUST BE THREE FULL SENTENCES OF BACKGROUND/CONTEXT; ANYTHING SHORTER IS UNACCEPTABLE!

YOU SHOULD RETURN EIGHT SUCH ENTRIES FOR THE EIGHT ACTIVITIES IN EXACTLY THIS FORMAT AS A SINGLE JSON ARRAY, EXACTLY LIKE SO:

ACTIVITIES:
[
  {{
    "Activity Type": "TIMED ACTIVITY",
    "Trait": "Dutiful",
    "Trait Level": "HIGH",
    ...
  }},
  {{
    "Activity Type": "TIMED ACTIVITY",
    "Trait": "Dutiful",
    "Trait Level": "LOW",
    ...
  }},
  ...
]

Do not wrap this in ```json ```, just give the pure content of the array. Be sure to precede the array with the exact string 'ACTIVITIES:' so the output can be processed correctly.

YOUR OUTPUTS:
"""

generate_four_activities_OLD = """
Your job is to help generate different kinds of activities for users of a personality-related application given high or low scores for a particular trait.

There are two kinds of activities to be generated, **timed activities** and **reflections**.

Timed activities tell the user to do/practice/implement something in their life over the next N hours. N can range from one day to one week, but shouldn't be longer or shorter than this. Be sure to give people an appropriate amount of time to do the activity. It should be something that the user can accomplish in the course of their normal daily/weekly activities in their normal work/home/social life.
Vague example of a timed activity: "Over the next 24 hours, try to do X."

Reflections are essentially writing prompts that the user will take on as soon as they are presented with them.

We will be generating activities related to trait {SCALE}. 
Example items that comprise this trait in our application are as follows (some may be reverse-scored): {ITEMS}

When creating the activities, you should find a way to pose them without necessarily invoking the actual word {SCALE} unless it is essential to understanding the question.
Also, be sure not to make the activities sound patronizing, judgy, or condescending.

Your job is to generate FOUR activities related to trait {SCALE}:
1. One TIMED ACTIVITY for someone HIGH in trait {SCALE}
2. One TIMED ACTIVITY for someone LOW in trait {SCALE}
3. One REFLECTION for someone HIGH in trait {SCALE}
4. One REFLECTION for someone LOW in trait {SCALE}

FORMATTING REQUIREMENTS:
Format each of the four activities as a separate block, using a key-value pair format like this (this is just one example):

{{
  "Activity Type": "TIMED ACTIVITY/REFLECTION",
  "Trait": {SCALE} 
  "Trait Level": "HIGH/LOW",
  "Title": "Simple, unique, natural-sounding title for the activity; 30 characters MAX, with no word more than 10 characters (for formatting reasons). SHOULD NOT USE THE WORDS TIMED, ACTIVITY, REFLECTION",
  "Description": "3 solid sentences that give the motivation/framing/introduction of why this activity might be relevant to someone who is low/high in {SCALE}.",
  "Activity": "The actual content of the activity",
  "Categorization": "Positive/Negative",
  "Domain": "Self/Relationships/Purpose (whichever seems closest, this categorization is not a big deal)"
}}

Emphasizing that the description should be longer than the activity itself. IT MUST BE THREE FULL SENTENCES OF BACKGROUND/CONTEXT; ANYTHING SHORTER IS UNACCEPTABLE!

Note: 
A POSITIVE version means an activity that plays on whatever stengths might be associated with being at that level for that trait. Any activity that asks for growth or something not naturally associated with this trait level should NOT be classified as positive!
A NEGATIVE version means a growth-based activity that plays on the potential weaknesses of being at that level for that trait. Any activity that plays to an existing strength should not be classified as negative!

YOU SHOULD RETURN FOUR SUCH ENTRIES FOR THE FOUR ACTIVITIES IN EXACTLY THIS FORMAT AS A SINGLE JSON ARRAY, LIKE SO:

[
  {{
    "Activity Type": "TIMED ACTIVITY",
    "Trait": "Dutiful",
    "Trait Level": "HIGH",
    ...
  }},
  {{
    "Activity Type": "TIMED ACTIVITY",
    "Trait": "Dutiful",
    "Trait Level": "LOW",
    ...
  }},
  ...
]

Do not wrap this in ```json ```, just give the pure content of the array.

YOUR OUTPUTS:
"""

insights_generation = """
Your job is to generate short insights for people who are high and low in the following traits: {SCALES}. You should generate {N} insights for HIGH scorers AND {N} insights for LOW scorers for EACH TRAIT! (total of N * 2 * number of traits)

These will be sent to users as push notifications, so they should fit within that scope and context.

The insights should be insightful (obviously) and valuable for someone who is high or low in that trait, and they should get something valuable from a push notification with the text of the insights.

Additionally, it is advisable to occasionally use or reference famous/wise quotations as or within an insight.

The insights should be meaningful and substantive, but almost fortune-cookie-like in their style.

The insights should generally be no more than one sentence long (if it is a quote, it should just be the quote + attribution; otherwise, just the idea/insight).

Please format your outputs as follows:
{{
  "Trait": "eg, Accomodating", 
  "Trait Level": "HIGH/LOW",
  "Insight": "The actual content of the insight"
}}

YOU SHOULD RETURN ALL SUCH ENTRIES FOR ALL TRAITS IN EXACTLY THIS FORMAT AS A SINGLE JSON ARRAY, LIKE SO:

[
  {{
    "Trait": "eg, Accomodating", 
    "Trait Level": "LOW",
    "Insight": "The actual content of the insight"
  }},
  {{
    "Trait": "eg, Accomodating", 
    "Trait Level": "HIGH",
    "Insight": "The actual content of the insight"
  }},
  ...
]

Do not wrap this in ```json ```, just give the pure content of the array.

YOUR OUTPUTS:
"""
