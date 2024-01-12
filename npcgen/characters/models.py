class Gender:
    MALE = "Male"
    FEMALE = "Female"
    NOT_SPECIFIED = "Not specified"


class ItemType:
    MELEE_WEAPON = "Melee Weapon"
    RANGED_WEAPON = "Ranged Weapon"
    ARMOR = "Armor"
    GEAR = "Gear"
    TOOL = "Tool"
    CONSUMABLE = "Consumable"
    TREASURE = "Treasure"
    OTHER = "Other"


class Character:
    def __init__(
        self,
        alignment_id,
        class_id,
        race_id,
        level=1,
        gender=Gender.NOT_SPECIFIED,
        name=None,
        hints=None,
        backstory=None,
        plot_hook=None,
        strength=None,
        dexterity=None,
        constitution=None,
        intelligence=None,
        wisdom=None,
        charisma=None,
        perception=None,
        armor_class=None,
        hit_points=None,
        speed=None,
        fortitude_save=None,
        reflex_save=None,
        will_save=None,
        id=None,
        alignment_name=None,
        class_name=None,
        template_id=None,
        template_name=None,
        race_name=None,
        user_id=None,
        is_template=False,
        skills=[],
        items=[],
    ):
        self.user_id = user_id

        self.template_id = template_id
        self.template_name = template_name

        self.alignment_id = alignment_id
        self.alignment_name = alignment_name

        self.class_id = class_id
        self.class_name = class_name

        self.race_id = race_id
        self.race_name = race_name

        self.name = name
        self.hints = hints
        self.backstory = backstory
        self.plot_hook = plot_hook
        self.level = level
        self.gender = gender

        # Stats
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.armor_class = armor_class
        self.hit_points = hit_points
        self.speed = speed
        self.perception = perception

        # Saving Throws
        self.fortitude_save = fortitude_save
        self.reflex_save = reflex_save
        self.will_save = will_save

        self.id = id
        self.is_template = is_template

        self.skills = skills
        self.items = items


class Item:
    def __init__(
        self,
        name,
        item_type,
        damage,
        damage_type,
        traits,
        id=None,
    ):
        self.id = id
        self.name = name
        self.item_type = item_type
        self.damage = damage
        self.damage_type = damage_type
        self.traits = traits


class CharacterItem(Item):
    def __init__(self, item, proficiency, id=None):
        super().__init__(
            name=item.name,
            item_type=item.item_type,
            damage=item.damage,
            damage_type=item.damage_type,
            traits=item.traits,
            id=id,
        )
        self.proficiency = proficiency


class Skill:
    def __init__(self, name, description, id=None):
        self.id = id
        self.name = name
        self.description = description


class CharacterSkill(Skill):
    def __init__(self, skill, proficiency, id=None):
        super().__init__(
            name=skill.name,
            description=skill.description,
            id=id,
        )
        self.proficiency = proficiency


class Option:
    def __init__(self, name, description=None, id=None):
        self.id = id
        self.name = name
        self.description = description
