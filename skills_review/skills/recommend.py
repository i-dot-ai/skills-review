import re

from django.conf import settings
import openai

openai.api_key = settings.OPENAI_KEY

bullet_regex = re.compile(r"\d\d?\. ")


def remove_bullets(text):
    lines = bullet_regex.split(text)
    clean_lines = tuple(line.strip() for line in lines)
    non_empty_lines = tuple(line for line in clean_lines if line)
    return non_empty_lines


def get_job_skills(job_title):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=f"List 10 skills a {job_title} might have",
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    text = response['choices'][0]['text']
    lines = remove_bullets(text)
    return lines


def get_job_image_url(job_title):
    response = openai.Image.create(
      prompt=f"a cartoon of a civil servant pretending to be a {job_title}",
      n=1,
      size="512x512"
    )
    image_url = response['data'][0]['url']
    return image_url
