from sqlalchemy import text

from ..core.db_utils import (
    create_record,
    delete_record,
    read_record_by_attr,
    record_exists,
    update_record,
)
from ..core.pagination import PaginatedResponse, Pagination
from .models import (
    Character,
    CharacterItem,
    CharacterSkill,
    Item,
    Option,
    Skill,
)


class CharacterDao:
    def __init__(self, session):
        self.session = session

    def get_character(self, id, populate_items=False, populate_skills=False):
        record = self.session.execute(
            text(
                """
            SELECT
            ch.*,
            a.id alignment_id,
            a.name alignment_name,
            cc.id class_id,
            cc.name class_name,
            r.id race_id,
            r.name race_name,
            t.id AS template_id,
            t.name AS template_name
            FROM character ch
            LEFT JOIN character_class cc ON
            cc.id = class_id
            JOIN race r ON
            r.id = race_id
            JOIN alignment a ON
            a.id = alignment_id
            LEFT JOIN character t ON
            t.id = ch.template_id
            WHERE ch.id = :id
            AND ch.deleted = FALSE
            """
            ),
            {"id": id},
        ).fetchone()

        if record is None:
            return None

        character = self._map_record_to_character(record)
        if populate_items:
            character.items = self.get_character_items(id)
        if populate_skills:
            character.skills = self.get_character_skills(id)

        return character

    def get_characters_by_user(
        self, user_id, template=False, page=1, page_size=20
    ):
        offset = (page - 1) * page_size

        records = self.session.execute(
            text(
                """
            SELECT
            count(*) OVER() AS total_count,
            ch.*,
            a.id alignment_id,
            a.name alignment_name,
            cc.id class_id,
            cc.name class_name,
            r.id race_id,
            r.name race_name,
            t.id AS template_id,
            t.name AS template_name
            FROM character ch
            LEFT JOIN character_class cc ON
            cc.id = class_id
            JOIN race r ON
            r.id = race_id
            JOIN alignment a ON
            a.id = alignment_id
            LEFT JOIN character t ON
            t.id = ch.template_id
            WHERE ch.is_template = :template
            AND ch.deleted = FALSE
            AND ch.user_id = :user_id
            OR ch.user_id IS NULL
            ORDER BY ch.created_at DESC
            LIMIT :page_size OFFSET :offset
            """
            ),
            {
                "user_id": user_id,
                "template": template,
                "page_size": page_size,
                "offset": offset,
            },
        ).fetchall()

        return PaginatedResponse(
            data=[self._map_record_to_character(record) for record in records],
            pagination=Pagination(
                page,
                page_size,
                records[0].total_count // page_size + 1,
            ),
        )

    def create_character(self, character):
        character_dict = self._character_to_dict(character)
        character_id = create_record(
            self.session, "character", "id", **character_dict
        )[0]

        if character.items:
            for item in character.items:
                self.add_item_to_character(
                    character_id, item.id, item.proficiency
                )

        if character.skills:
            for skill in character.skills:
                self.add_skill_to_character(
                    character_id, skill.id, skill.proficiency
                )

        self.session.commit()
        return character_id

    def delete_character(self, character_id):
        delete_record(self.session, "character", character_id)
        self.session.commit()

    def soft_delete_character(self, character_id):
        update_record(self.session, "character", character_id, deleted=True)
        self.session.commit()

    def character_with_name_exists(self, name):
        return record_exists(self.session, "character", "name", name)

    def add_item_to_character(self, character_id, item_id, proficiency):
        create_record(
            self.session,
            "character_item",
            character_id=character_id,
            item_id=item_id,
            proficiency=proficiency,
        )
        self.session.commit()

    def get_character_items(self, character_id):
        records = self.session.execute(
            text(
                """
            SELECT
            i.id,
            i.name,
            i.item_type,
            i.damage,
            i.damage_type,
            i.traits,
            ci.proficiency
            FROM item i
            JOIN character_item ci ON
            ci.item_id = i.id
            WHERE ci.character_id = :character_id
            ORDER BY i.item_type, i.name
            """
            ),
            {"character_id": character_id},
        )
        return [self._map_record_to_item(record) for record in records]

    def add_skill_to_character(self, character_id, skill_id, proficiency):
        create_record(
            self.session,
            "character_skill",
            character_id=character_id,
            skill_id=skill_id,
            proficiency=proficiency,
        )
        self.session.commit()

    def get_character_skills(self, character_id):
        records = self.session.execute(
            text(
                """
            SELECT
            s.id,
            s.name,
            s.description,
            cs.proficiency
            FROM skill s
            JOIN character_skill cs ON
            cs.skill_id = s.id
            WHERE cs.character_id = :character_id
            ORDER BY s.name
            """
            ),
            {"character_id": character_id},
        )
        return [self._map_record_to_skill(record) for record in records]

    def get_character_template_options(self):
        records = self.session.execute(
            text(
                """
            SELECT
            ch.id,
            ch.name || ' (' || ch.level || ')' AS name
            FROM character ch
            WHERE ch.is_template = TRUE
            ORDER BY ch.level, ch.name
            """
            )
        )
        return [self._map_record_to_option(record) for record in records]

    def get_template_name(self, template_id):
        record = self.session.execute(
            text(
                """
            SELECT
            ch.name
            FROM character ch
            WHERE ch.is_template = TRUE
            AND ch.id = :template_id
            """
            ),
            {"template_id": template_id},
        ).fetchone()
        return record.name if record else None

    def get_alignment_name(self, alignment_id):
        record = self.session.execute(
            text(
                """
            SELECT
            a.name
            FROM alignment a
            WHERE a.id = :alignment_id
            """
            ),
            {"alignment_id": alignment_id},
        ).fetchone()

        return record.name if record else None

    def get_character_class_name(self, class_id):
        record = self.session.execute(
            text(
                """
            SELECT
            c.name
            FROM character_class c
            WHERE c.id = :class_id
            """
            ),
            {"class_id": class_id},
        ).fetchone()

        return record.name if record else None

    def get_race_name(self, race_id):
        record = self.session.execute(
            text(
                """
            SELECT
            r.name
            FROM race r
            WHERE r.id = :race_id
            """
            ),
            {"race_id": race_id},
        ).fetchone()

        return record.name if record else None

    def get_character_alignment_options(self):
        records = self.session.execute(
            text(
                """
            SELECT
            a.id,
            a.name
            FROM alignment a
            """
            )
        )
        return [self._map_record_to_option(record) for record in records]

    def get_character_class_options(self):
        records = self.session.execute(
            text(
                """
            SELECT
            c.id,
            c.name
            FROM character_class c
            """
            )
        )
        return [self._map_record_to_option(record) for record in records]

    def get_character_race_options(self):
        records = self.session.execute(
            text(
                """
            SELECT
            r.id,
            r.name
            FROM race r
            """
            )
        )
        return [self._map_record_to_option(record) for record in records]

    def _character_to_dict(self, character):
        return {
            "user_id": character.user_id,
            "name": character.name,
            "race_id": character.race_id,
            "class_id": character.class_id,
            "alignment_id": character.alignment_id,
            "hints": character.hints,
            "backstory": character.backstory,
            "plot_hook": character.plot_hook,
            "template_id": character.template_id,
            "level": character.level,
            "gender": character.gender,
            "strength": character.strength,
            "dexterity": character.dexterity,
            "constitution": character.constitution,
            "intelligence": character.intelligence,
            "wisdom": character.wisdom,
            "charisma": character.charisma,
            "perception": character.perception,
            "armor_class": character.armor_class,
            "hit_points": character.hit_points,
            "speed": character.speed,
            "fortitude_save": character.fortitude_save,
            "reflex_save": character.reflex_save,
            "will_save": character.will_save,
            "is_template": character.is_template,
        }

    def _map_record_to_character(self, record):
        return Character(
            user_id=record.user_id,
            name=record.name,
            race_id=record.race_id,
            race_name=record.race_name,
            class_id=record.class_id,
            class_name=record.class_name,
            alignment_id=record.alignment_id,
            alignment_name=record.alignment_name,
            hints=record.hints,
            backstory=record.backstory,
            plot_hook=record.plot_hook,
            template_id=record.template_id,
            template_name=record.template_name,
            level=record.level,
            gender=record.gender,
            strength=record.strength,
            dexterity=record.dexterity,
            constitution=record.constitution,
            intelligence=record.intelligence,
            wisdom=record.wisdom,
            charisma=record.charisma,
            perception=record.perception,
            armor_class=record.armor_class,
            hit_points=record.hit_points,
            speed=record.speed,
            fortitude_save=record.fortitude_save,
            reflex_save=record.reflex_save,
            will_save=record.will_save,
            id=record.id,
            is_template=record.is_template,
        )

    def _map_record_to_skill(self, record):
        return CharacterSkill(
            Skill(
                id=record.id,
                name=record.name,
                description=record.description,
            ),
            proficiency=record.proficiency,
        )

    def _map_record_to_item(self, record):
        return CharacterItem(
            item=Item(
                id=record.id,
                name=record.name,
                item_type=record.item_type,
                damage=record.damage,
                damage_type=record.damage_type,
                traits=record.traits,
            ),
            proficiency=record.proficiency,
        )

    def _map_record_to_option(self, record):
        return Option(id=record.id, name=record.name)


class ItemDao:
    def __init__(self, session):
        self.session = session

    def get_item_by_properties(self, **kwargs):
        query = self.session.execute(
            text(
                """
            SELECT
            id,
            name,
            item_type,
            damage,
            damage_type,
            traits
            FROM item
            WHERE name = :name
            AND damage = :damage
            AND damage_type = :damage_type
            AND item_type = :item_type
            """
            ),
            kwargs,
        )
        record = query.fetchone()
        return self._map_record_to_item(record) if record else None

    def create_item(self, item):
        item_dict = self._map_item_to_dict(item)
        record = create_record(self.session, "item", "id", **item_dict)
        self.session.commit()
        return record[0]

    def _map_item_to_dict(self, item):
        return {
            "name": item.name,
            "item_type": item.item_type,
            "damage": item.damage,
            "damage_type": item.damage_type,
            "traits": item.traits,
        }

    def _map_record_to_item(self, record):
        return Item(
            id=record.id,
            name=record.name,
            item_type=record.item_type,
            damage=record.damage,
            damage_type=record.damage_type,
            traits=record.traits,
        )


class SkillDao:
    def __init__(self, session):
        self.session = session

    def get_skill_by_name(self, name):
        record = read_record_by_attr(self.session, "skill", "name", name)
        return self._map_record_to_skill(record) if record else None

    def create_skill(self, skill):
        skill_dict = self._map_skill_to_dict(skill)
        record = create_record(self.session, "skill", "id", **skill_dict)
        self.session.commit()
        return record[0]

    def _map_skill_to_dict(self, skill):
        return {
            "name": skill.name,
            "description": skill.description,
        }

    def _map_record_to_skill(self, record):
        return Skill(
            id=record.id,
            name=record.name,
            description=record.description,
        )
