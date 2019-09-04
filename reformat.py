import re
import sys
import argparse

parser = argparse.ArgumentParser(description="Format scenario updates")
parser.add_argument("filename", help="File containing unformatted scenario update")
parser.add_argument("players", metavar="player", default=[], nargs="*", help="Players to populate turn order")
parser.add_argument("--turn", "-t", type=int, default=0, help="Current turn")
args = parser.parse_intermixed_args()

with open(args.filename, "r", encoding="utf-8") as f:
    cont = f.read()

# some cards use ~ for newline
# and some have To Acquire on the same line as a trait
cont = re.sub(r"~", "\n", cont, flags=re.MULTILINE)
cont = re.sub(r"(?<!^)To (Acquire|Defeat):", r"\nTo \1:", cont, flags=re.MULTILINE)

# New bug puts things on the same line that shouldn't be on the same line, but there are 3 spaces in the middle; Convert that to newlines
cont = re.sub(r"   ", "\n", cont, flags=re.MULTILINE)

# trim trailing spaces and convert _ to periods
cont = re.sub(r" +$", "", cont, flags=re.MULTILINE)
cont = re.sub(r"_\b", ".", cont, flags=re.MULTILINE)
cont = re.sub(r" {2,}", " ", cont, flags=re.MULTILINE)

# Get rid of location numbers
cont = re.sub(r"Location #[0-9]+: ", "", cont, flags=re.MULTILINE)

# Add Open tag to at this location
cont = re.sub(r"(?<!\[b\]Closed\[/b\]\n)At This Location:", "At This Location (Open):", cont, flags=re.MULTILINE)

# Convert Random Cards spoiler
cont = re.sub(r"\[spoiler=Random Cards\]\n\[b\]Monsters\[/b\]\n(.*?)\n\[b\]Barriers\[/b\]\n(.*?)\n\[b\]Weapons\[/b\]\n(.*?)\n\[b\]Spells\[/b\]\n(.*?)\n\[b\]Armors\[/b\]\n(.*?)\n\[b\]Items\[/b\]\n(.*?)\n\[b\]Allies\[/b\]\n(.*?)\n\[b\]Blessings\[/b\]\n(.*?\[/spoiler\])\n\[/spoiler\]", r"[spoiler=Random Monsters]\n\1\n[/spoiler][spoiler=Random Barriers]\n\2\n[/spoiler][spoiler=Random Weapons]\n\3\n[/spoiler][spoiler=Random Spells]\n\4\n[/spoiler][spoiler=Random Armor]\n\5\n[/spoiler][spoiler=Random Items]\n\6\n[/spoiler][spoiler=Random Allies]\n\7\n[/spoiler][spoiler=Random Blessings]\n\8\n[/spoiler]", cont, flags=re.MULTILINE | re.DOTALL)

# collapse adjacent spoilers
cont = re.sub(r"\[/spoiler\]\n+\[spoiler", "[/spoiler][spoiler", cont, flags=re.MULTILINE)

# space out random X spoilers and add labels
cont = re.sub(r"\[spoiler=Random Monsters\]\n(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])", r"[spoiler=Random Monsters]\nMonster 1\n\1\n\nMonster 2\n\2\n\nMonster 3\n\3\n\nMonster 4\n\4\n\nMonster 5\n\5", cont, flags=re.MULTILINE | re.DOTALL)
cont = re.sub(r"\[spoiler=Random Barriers\]\n(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])", r"[spoiler=Random Barriers]\nBarrier 1\n\1\n\nBarrier 2\n\2\n\nBarrier 3\n\3\n\nBarrier 4\n\4\n\nBarrier 5\n\5", cont, flags=re.MULTILINE | re.DOTALL)
cont = re.sub(r"\[spoiler=Random Weapons\]\n(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])", r"[spoiler=Random Weapons]\nWeapon 1\n\1\n\nWeapon 2\n\2\n\nWeapon 3\n\3\n\nWeapon 4\n\4\n\nWeapon 5\n\5", cont, flags=re.MULTILINE | re.DOTALL)
cont = re.sub(r"\[spoiler=Random Spells\]\n(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])", r"[spoiler=Random Spells]\nSpell 1\n\1\n\nSpell 2\n\2\n\nSpell 3\n\3\n\nSpell 4\n\4\n\nSpell 5\n\5", cont, flags=re.MULTILINE | re.DOTALL)
cont = re.sub(r"\[spoiler=Random Armor\]\n(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])", r"[spoiler=Random Armor]\nArmor 1\n\1\n\nArmor 2\n\2\n\nArmor 3\n\3", cont, flags=re.MULTILINE | re.DOTALL)
cont = re.sub(r"\[spoiler=Random Items\]\n(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])", r"[spoiler=Random Items]\nItem 1\n\1\n\nItem 2\n\2\n\nItem 3\n\3\n\nItem 4\n\4\n\nItem 5\n\5", cont, flags=re.MULTILINE | re.DOTALL)
cont = re.sub(r"\[spoiler=Random Allies\]\n(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])", r"[spoiler=Random Allies]\nAlly 1\n\1\n\nAlly 2\n\2\n\nAlly 3\n\3\n\nAlly 4\n\4\n\nAlly 5\n\5", cont, flags=re.MULTILINE | re.DOTALL)
cont = re.sub(r"\[spoiler=Random Blessings\]\n(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])(\[spoiler\].*?\[/spoiler])", r"[spoiler=Random Blessings]\nBlessing 1\n\1\n\nBlessing 2\n\2\n\nBlessing 3\n\3\n\nBlessing 4\n\4\n\nBlessing 5\n\5", cont, flags=re.MULTILINE | re.DOTALL)

# uncollapse Random Monsters
cont = re.sub(r"\]\[spoiler=Random Monsters\]", "]\n\n[spoiler=Random Monsters]", cont, flags=re.MULTILINE)

# fix niggles
cont = re.sub(", None", "", cont, flags=re.MULTILINE)
cont = re.sub("None 0", "None", cont, flags=re.MULTILINE)
cont = re.sub("Combat 0", "Combat See Below", cont, flags=re.MULTILINE)
cont = re.sub("See below", "See Below", cont, flags=re.MULTILINE)

# put set indicator on same line as card type
cont = re.sub(r"\[/b\]\n([^\n]+)\n(Loot|Henchman|Villain|Monster|Barrier|Weapon|Spell|Armor|Item|Ally|Blessing|Story)", r"[/b]\n\1 \2", cont, flags=re.MULTILINE)

# collapse traits
for i in range(1, 10):
    frag = r"([^\[\n]+)\n" * i
    repl = "Traits:"
    for j in range(1, i+1):
        repl += f" \\{j}"
    cont = re.sub("Traits:\n" + frag + "To ", repl + "\nTo ", cont, flags=re.MULTILINE)

# collapse checks to acquire/defeat
for i in range(9, 0, -1):
    frag = r"([^\[]{,20})\n" * i
    repl = "To Acquire:"
    for j in range(1, i+1):
        repl += f" \\{j}"
    cont = re.sub("To Acquire:\n" + frag, repl + "\n", cont, flags=re.MULTILINE)

for i in range(9, 0, -1):
    frag = r"([^\[]{,20})\n" * i
    repl = "To Defeat:"
    for j in range(1, i+1):
        repl += f" \\{j}"
    cont = re.sub("To Defeat:\n" + frag, repl + "\n", cont, flags=re.MULTILINE)

# fix blessings deck (note, turn order must be injected manually for now)
cont = re.sub(r"\[spoiler\](?:Blessings Deck Card [0-9]+ )?\[b\]Blessings Deck Card ([0-9]+)[^[]*?\[/b\]\n", r"\n\nBlessings Deck Card \1 - Turn \1 ??\n[spoiler]", cont, flags=re.MULTILINE)

# collapse 1st blessing
cont = re.sub(r"\n+Blessings Deck Card 1", r"\nBlessings Deck Card 1", cont, flags=re.MULTILINE)

# collapse space between location block and location deck
cont = re.sub(r"\[b\]Located/Displayed Here:\[/b\] (.*)\n+\[", r"[b]Located/Displayed Here:[/b] \1\n[", cont, flags=re.MULTILINE)

# collapse space between opening spoiler and card name
cont = re.sub(r"Card ([0-9]+)\]\s*\[b\]", r"Card \1][b]", cont, flags=re.MULTILINE)

# ensure adequate space between locations
cont = re.sub(r"\]\n*\[b\]((?!Closed\[).*?)\[/b\]\n(\[b\]Closed\[/b\]\n)?(\[i\]Traits:\[/i\].*?\n)?\[i\]At This Location", r"]\n\n[b]\1[/b]\n\2\3[i]At This Location", cont, flags=re.MULTILINE)
cont = re.sub(r"(\[b\]Located/Displayed Here:\[/b\] .*?)\n*\[b\]((?!Closed\[).*?)\[/b\]\n(\[b\]Closed\[/b\]\n)?(\[i\]Traits:\[/i\].*?\n)?\[i\]At This Location", r"\1\n\n[b]\2[/b]\n\3\4[i]At This Location", cont, flags=re.MULTILINE)

# ensure adequate space between blessing deck cards
cont = re.sub(r"\]\n*Blessings Deck Card", r"]\n\nBlessings Deck Card", cont, flags=re.MULTILINE)

# bold Trigger and Mythic traits
cont = re.sub(r"Traits:(.*?\s)Trigger", r"Traits:\1[b]Trigger[/b]", cont, flags=re.MULTILINE)
cont = re.sub(r"Traits:(.*?\s)Mythic", r"Traits:\1[b]Mythic[/b]", cont, flags=re.MULTILINE)

# add Abyssal trait to relevant locations
abyssal = {"Abyssal River", "Battlebliss", "Befouled Altar", "Blackburgh", "Gate of the Worldwound", "Harem of Ardent Dreams", "Harvester's Pit", "Ivory Labyrinth", "Lightless Maze", "Locust Shrine", "Molten Pool", "Prison Vault", "Qlippoth Runestone", "Rapture of Rupture", "Sanctum", "Shrine to Baphomet", "Soul Foundry", "The Rasping Rifts", "Threshold", "Wounded Lands", "Yearning House"}
for loc in abyssal:
    cont = re.sub(r"\[b\]" + loc + r"\[/b\]\n\[i\]At", "[b]" + loc + "[/b]\n[i]Traits:[/i] Abyssal\n[i]At", cont, flags=re.MULTILINE)

# Special handling for locations: Abyssal Rift, Grinder, Middle of Nowhere, Seaside Warehouse
# NOT IMPLEMENTED YET

# add turn order if specified
# TODO: re-number the blessings deck itself so that it maintains the same numbering throughout a game instead of restarting at 1
# This way players can easily see how many cards in the blessings deck are left even if it's been a while between updates
if args.players:
    # sometimes the blessings deck numbering starts at 0 instead of 1, account for that
    if cont.find("Turn 0 ??") != -1:
        # Blessing 0 found, subtract 1 from our turn numbering since we're zero-based
        zerofix = 1
    else:
        # Starting at blessing 1, so no adjustments needed
        zerofix = 0
    off = args.turn
    np = len(args.players)
    j = args.turn % np
    for i in range(1, 41):
        cont = re.sub(f"Turn {i-zerofix} \\?\\?", f"Turn {i+off} " + args.players[j], cont, flags=re.MULTILINE)
        j = (j + 1) % np

# final cleanup: trim leading spaces
cont = re.sub(r"^ +", "", cont, flags=re.MULTILINE)

# write new contents
with open(args.filename, "w", encoding="utf-8") as f:
    f.write(cont)
