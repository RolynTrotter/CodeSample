Note: all code not otherwise labeled was written by me. This was in the
Linguistics department, and the idea for the test was mine so I had
to implement it.

# Intro
Over the summer of 2016 (and for the surrounding semesters), 
I worked on making a stress correlate database
with Anya Lunden at William and Mary.

The database, here held in LangDatabase.csv, 
compiles a number of attributes about the realization
of stress in a wide number of languages. 
The sources vary widely in their detail and methodologies. 
Some are based on acoustic studies, others by a researcher's
own ear in the field. With this code, we wanted to check that, 
on the whole, the languages in the database gel with each other.

Lang_Prob_Parser.py looks at the database's language families
and checks that languages within one family are, on average, 
more similar with each other than with random groupings of
languages. Because, well, they're related. This was one of a couple
checks we came up with, but it's the one with code involved.

# Gist of the math

Languages generally use some number of duration, pitch, or intensity
as correlates of stress.
If every language in a family had exactly the same set of correlates,
that would be a sign that the sources have at least some
consistency with each other. On the other hand, if a family
has an internal distribution of correlates that looks the same
as the database at large, that would suggest a bunch of nonsense
datapoints.

The difference between the 'global' distribution and the 'family'
distribution is calculated as a z-score. Then the z-scores of
all families (of a minimum size) are compared with that of
what random families would look like. That is the 'meta z-score'
that we hope to be greater than about 1.65.

That's enough to reject the null hypothesis of randomness. But 
then we actually randomize a bunch of families 
to see how many tries it takes to happenstance our way into
a set with a meta-z-score higher than our actual one. 
I often write a Monte Carlo sim when the math is
otherwise unintuitive

# Running it
Running Lang_Prob_Parser at the command either takes 
a few arguments or asks for your input as it runs. 
I suggest the latter on first run-through since 
I just slapped on the arguments in the order you would type them in.

$python3 Lang_Prob_Parser.py LangDatabase.csv 10 100

By default, it uses the actual database 
(or the database as it was back when I wrote it, anyway).
But You can swap in either Extreme.csv to see how a 
bunch of language families in total agreement have a very high
meta-z-score (and probably won't ever get you through the 
Monte Carlo part), or swap in Random.csv for a set with a very low 
meta-z-score.

You can also see differences with varying minimum sizes for languages.
Five and ten are good places to start. There are only a few families 
with ten or more languages in them in the database, 
but there are enough.

# Resources
You can find the current version of the stress correlate database here:
https://wmpeople.wm.edu/site/page/sllund/stresscorrelatedatabase

The corresponding paper that talks more about the database, along with
an application of it, is here:
https://www.cambridge.org/core/journals/phonology/article/vowellength-contrasts-and-phonetic-cues-to-stress-an-investigation-of-their-relation/2839919AEA482697DBDAA513EE086D04
