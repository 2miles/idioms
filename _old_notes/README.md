# Idioms

This repo contains all my scripts used to collect and manage the data for my idiom app. It also contains scripts for accessing the database and importing and exporting.

## Definition Scraper

It takes that list and scrapes free dictionary for definitions for every idiom in the list. The output will be a `.txt` file with the idioms, and their definitions.

- It is expecting a numbered markdown list of idioms to be in the directory.

### How to run

```shell
 python3 run_scraper input.md output.txt
```

There will be some console log output as it is scraping. It takes a bit of time. The default delay is 10 seconds for each idiom. For example to change the delay to 5 seconds instead run the command like this:

```shell
 python3 run_scraper input.md output.txt 5
```

### input:

```markdown
1. Middle of the road
2. stick up your ass
3. up in the air
4. spit on your grave
5. dont piss into the wind
6. go to bat
7. cooking something up
8. thumb up your ass
9. shit dont stink
10. cherry picking
11. hot to trot
12. a wake up call
13. cutting your teeth on something
14. dont go chasing waterfalls
```

### output:

```
['Middle of the road', 'middle-of-the-road', '1. Describing an option that is neither the most nor the least expensive. ']
['stick up your ass', "stick up (one's) ass", ' A rigid and uptight demeanor. ']
['up in the air', 'be up in the air', 'To be uncertain or subject to change. ']
['spit on your grave', '', '']
['dont piss into the wind', '', '']
['go to bat', 'go to bat for (one)', 'To act in support of one. ']
['cooking something up', 'cook up', 'A noun or pronoun can be used between "cook" and "up."']
['thumb up your ass', '', '']
['shit dont stink', '', '']
['cherry picking', 'cherry-pick', '1. To choose something very carefully to ensure that the best option is chosen, perhaps through means that provide one an unfair advantage or from a selection that others do not have ready access to. ']
['hot to trot', 'hot to trot', '1. Eager or impatient to do something. ']
['a wake up call', '', '']
['cutting your teeth on something', "cut (one's) teeth on (something)", "To gain experience with something, especially at a young age (when one's teeth would be coming in). "]
['dont go chasing waterfalls', '', '']
```

# TODO

# Update definition scraper

Right now all it does is return a txt file. I still need to update this script to return the data in a more useful format like json or csv.

I also should update the input to expect an idiom ID that it will carry with it. So that the output will be more usefull. This means that I need to add the incoming idioms to the database first to get an ID assigned first. This means that i will probably want the input to also be a csv or json file.
