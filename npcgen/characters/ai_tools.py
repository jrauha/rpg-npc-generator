import openai

SYSTEM_PROMPT = (
    "You are a fantasy book author, skilled in writing background stories for "
    "fantasy characters."
)

SYSTEM_PROMPT_NAME = (
    "You are a fantasy name generator, skilled in generating fantasy names "
    "for fantasy characters. Response should only contain one name with max "
    "length of 200 characters."
)


def generate_name(race, class_name, alignment, template_name, hints):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_NAME},
            {
                "role": "user",
                "content": (
                    f"Create one name for {race} {template_name}. "
                    f"Alignment: {alignment}. Character class: {class_name}. "
                    f"Character hints: {hints}."
                ),
            },
        ],
    )
    return completion.choices[0].message.content


def generate_backstory(
    name, race, class_name, alignment, template_name, hints
):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Write short character summary for {race} {template_name}"
                    f"character named {name}. Character class: {class_name}. "
                    f"Alignment: {alignment}. Character hints: {hints}. It "
                    "should be max 500 characters long."
                ),
            },
        ],
    )
    return completion.choices[0].message.content


def generate_plot_hook(
    name, race, class_name, alignment, template_name, hints
):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Write tabletop RPG plot hook for {race} "
                    f"{template_name} character named {name}. Alignment: "
                    f"{alignment}. Character class: {class_name}. Character "
                    f"hints: {hints}. Plot hook should be max 150 characters "
                    "long."
                ),
            },
        ],
    )
    return completion.choices[0].message.content
