from transformers import pipeline 

summarization = pipeline("summarization")

full_txt = """
You and your friend need to ace 
Friday’s exam to avoid summer classes, and after a week of studying, you both
feel confident that you pulled it off. But when you get your grades back, they’re much lower 
than the two of you expected. You’re devastated. However, your friend doesn't
seem too bothered, and it's making you wonder why you can't
shake this off like they can. But should you really be trying
to look on the bright side? And is controlling our emotions 
even possible in the first place? The answer to the last question
is a definitive “yes.” There are numerous strategies
for regulating our emotions, and one framework to understand these
techniques is called the Process Model. Psychologists use this tool to identify
where and how to intervene in the process that forms our emotions. That process has four steps: first, we enter a situation, 
real or imagined, and that draws our attention. Then we evaluate, or appraise, 
the situation and whether it helps or hinders our goals. Finally, this appraisal leads to a set of 
changes in how we feel, think, and behave, known as an emotional response. Each step of this process offers 
an opportunity to consciously intervene and change our emotions, and the Process Model outlines what 
strategies we might try at each phase. To see this in action, let’s imagine
you’ve been invited to the same party as your least-favorite ex
and their new partner. Your first strategy could be avoiding
the situation altogether by skipping the party. But if you do attend, you could also try 
modifying the situation by choosing not to interact with your ex. If that’s proving difficult,
you might want to shift your attention, maybe by playing a game with your friends rather than focusing 
on your ex’s new partner. Another option would be to re-evaluate
how you think about the situation. After seriously reappraising things, you might realize that you don’t
care who your ex dates. If none of these strategies work, you can always try tempering 
your emotional response after the fact. But this can be tricky. Many of the easiest ways to do this, like hiding your emotions or trying 
to change them with recreational drugs, generally lead to more negative feelings
and health concerns in the long term. More sustainable strategies here include
going for a long walk, taking slow, deep breaths, or talking 
with someone in your support system. While using all these strategies well 
takes practice, learning to notice your emotions and reflect on where they’re coming from
is half the battle. And once you’ve truly internalized 
that you can regulate your emotions, doing so becomes much easier. But should you use these techniques 
to constantly maintain a good mood? That answer depends on how you define
what makes a mood “good.” It's tempting to think we should always
try to avoid sadness and frustration, but no emotion is inherently good or bad— they’re either helpful or unhelpful
depending on the situation. For example, if a friend is telling you
about the loss of a loved one, feeling and expressing sadness 
isn’t just appropriate, it can help you empathize
and support them. Conversely, while it’s unhealthy 
to regularly ignore your emotions, forcing a smile to get through a one-time
annoyance is perfectly reasonable. We hear a lot of mixed messages
about emotions. Some pressure us to stay upbeat while others tell us to simply take 
our emotions as they come. But in reality,
each person has to find their own balance. So if the question is:
“should you always try to be happy?” The answer is no. Studies suggest that people 
fixated on happiness often experience secondary
negative emotions, like guilt, or frustration over being upset, and disappointment that they
don't feel happier. This doesn't mean you should let
sadness or anger take over. But strategies like reappraisal can help
you re-evaluate your thoughts about a situation, allowing you to accept that you feel sad and cultivate hope 
that things will get better. """

short_txt = summarization(full_txt, max_length = 300, min_length = 100)[0]['summary_text']
print("Summary:", short_txt)