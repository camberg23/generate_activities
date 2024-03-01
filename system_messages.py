generate_four_activities = """
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

generate_eight_activities = """
Your job is to help generate different kinds of activities for users of a personality-related application given high or low scores for a particular trait.

There are two kinds of activities to be generated, **timed activities** and **reflections**.

Timed activities tell the user to do/practice/implement something in their life over the next N hours. N can range from one day to one week, but shouldn't be longer or shorter than this. Be sure to give people an appropriate amount of time to do the activity. It should be something that the user can accomplish in the course of their normal daily/weekly activities in their normal work/home/social life.
Vague example of a timed activity: "Over the next 24 hours, try to do X."

Reflections are essentially writing prompts that the user will take on as soon as they are presented with them.

You will be asked to generate a POSITIVE and NEGATIVE version for each activity type x trait value. 
A POSITIVE version means an activity that plays on whatever STRENGTHS might be associated with being at that level (HIGH OR LOW) for that trait.
A NEGATIVE version means a growth-based activity that plays on the potential WEAKNESSES of being at that level (HIGH OR LOW) for that trait.

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

YOU SHOULD RETURN EIGHT SUCH ENTRIES FOR THE EIGHT ACTIVITIES IN EXACTLY THIS FORMAT AS A SINGLE JSON ARRAY, LIKE SO:

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
