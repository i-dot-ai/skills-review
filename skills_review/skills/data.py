import csv
import itertools

from skills_review.skills import models


def key(row):
    return (
        row["level_B_name"],
        row["level_C_name"],
        row["clean skill name"],
        row["skill_name"],
    )


def process_file(file_object):
    reader = csv.DictReader(file_object)
    lines = (line for line in reader if line["text"])
    lines = sorted(lines, key=key)
    groups = itertools.groupby(lines, key=key)

    for ((level_1_name, level_2_name, clean_name, skill_name), group) in groups:
        name = clean_name or skill_name
        skill = models.Skill(name=name, level_1_name=level_1_name, level_2_name=level_2_name)
        skill.save()

        for row in group:
            sentence = models.SkillSentence(skill=skill, text=row["text"])
            sentence.save()

    return lines
