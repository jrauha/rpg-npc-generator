CREATE TYPE "gender" AS ENUM (
  'Male',
  'Female',
  'Not specified'
);

CREATE TYPE "item_type" AS ENUM (
    'Melee weapon',
    'Ranged weapon',
    'Armor',
    'Gear',
    'Tool',
    'Consumable',
    'Treasure',
    'Other'
);

CREATE TABLE "app_user" (
  "id" SERIAL PRIMARY KEY,
  "username" VARCHAR(255) NOT NULL,
  "password" VARCHAR(255) NOT NULL,
  "email" VARCHAR(255) NOT NULL,
  "superuser" BOOLEAN DEFAULT false,
  "created_at" TIMESTAMP DEFAULT (current_timestamp),
  "deleted" BOOLEAN DEFAULT false
);

CREATE TABLE "race" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR(255) NOT NULL,
  "description" TEXT
);

CREATE TABLE "character_class" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR(255) NOT NULL,
  "description" TEXT
);

CREATE TABLE "alignment" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR(255) NOT NULL,
  "description" TEXT
);

CREATE TABLE "character" (
  "id" SERIAL PRIMARY KEY,
  "user_id" INTEGER,
  "name" VARCHAR(255) NOT NULL,
  "race_id" INTEGER NOT NULL,
  "class_id" INTEGER NOT NULL,
  "alignment_id" INTEGER NOT NULL,
  "hints" TEXT,
  "backstory" TEXT,
  "plot_hook" TEXT,
  "created_at" TIMESTAMP DEFAULT (current_timestamp),
  "template_id" INTEGER,
  "is_template" BOOLEAN DEFAULT false,
  "level" INTEGER DEFAULT 1,
  "strength" INTEGER,
  "dexterity" INTEGER,
  "constitution" INTEGER,
  "intelligence" INTEGER,
  "wisdom" INTEGER,
  "charisma" INTEGER,
  "perception" INTEGER,
  "armor_class" INTEGER,
  "hit_points" INTEGER,
  "speed" INTEGER,
  "fortitude_save" INTEGER,
  "reflex_save" INTEGER,
  "will_save" INTEGER,
  "gender" gender,
  "deleted" BOOLEAN DEFAULT false
);

CREATE TABLE "skill" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR(255) NOT NULL,
  "description" TEXT
);

CREATE TABLE "character_skill" (
  "id" SERIAL PRIMARY KEY,
  "character_id" INTEGER NOT NULL,
  "skill_id" INTEGER NOT NULL,
  "proficiency" INTEGER NOT NULL
);

CREATE TABLE "character_item" (
  "id" SERIAL PRIMARY KEY,
  "character_id" INTEGER NOT NULL,
  "item_id" INTEGER NOT NULL,
  "proficiency" INTEGER NOT NULL
);

CREATE TABLE "item" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR(255) NOT NULL,
  "item_type" item_type NOT NULL,
  "damage" VARCHAR(255) NOT NULL,
  "damage_type" VARCHAR(255),
  "traits" VARCHAR(255)[]
);

ALTER TABLE "character" ADD FOREIGN KEY ("user_id") REFERENCES "app_user" ("id");

ALTER TABLE "character" ADD FOREIGN KEY ("race_id") REFERENCES "race" ("id");

ALTER TABLE "character" ADD FOREIGN KEY ("class_id") REFERENCES "character_class" ("id");

ALTER TABLE "character" ADD FOREIGN KEY ("alignment_id") REFERENCES "alignment" ("id");

ALTER TABLE "character" ADD FOREIGN KEY ("template_id") REFERENCES "character" ("id");

ALTER TABLE "character_skill" ADD FOREIGN KEY ("character_id") REFERENCES "character" ("id");

ALTER TABLE "character_skill" ADD FOREIGN KEY ("skill_id") REFERENCES "skill" ("id");

ALTER TABLE "character_item" ADD FOREIGN KEY ("character_id") REFERENCES "character" ("id");

ALTER TABLE "character_item" ADD FOREIGN KEY ("item_id") REFERENCES "item" ("id");


INSERT INTO race (id, name, description) VALUES
  (1, 'Human', 'Versatile and adaptable'),
  (2, 'Elf', 'Graceful and long-lived'),
  (3, 'Dwarf', 'Resilient and skilled artisans'),
  (4, 'Gnome', 'Inventive and curious'),
  (5, 'Half-Elf', 'A mix of human and elf'),
  (6, 'Half-Orc', 'A mix of human and orc'),
  (7, 'Halfling', 'Small and nimble'),
  (8, 'Goblin', 'Small and mischievous'),
  (9, 'Orc', 'Strong and aggressive');

INSERT INTO character_class (id, name, description) VALUES
  (1, 'None', 'No class'),
  (2, 'Warrior', 'Masters of combat'),
  (3, 'Wizard', 'Masters of arcane magic'),
  (4, 'Rogue', 'Masters of stealth and deception'),
  (5, 'Cleric', 'Divine spellcasters who serve a deity'),
  (6, 'Druid', 'Masters of nature and shapeshifting'),
  (7, 'Paladin', 'Holy warriors who uphold justice and righteousness'),
  (8, 'Ranger', 'Skilled hunters and trackers'),
  (9, 'Sorcerer', 'Innate spellcasters with magical bloodlines'),
  (10, 'Bard', 'Masters of music, poetry, and storytelling');

INSERT INTO alignment (id, name, description) VALUES
  (1, 'Lawful Good', 'Upholds honor and virtue'),
  (2, 'Neutral Good', 'Favors doing good over evil'),
  (3, 'Chaotic Good', 'Values individual freedom and kindness'),
  (4, 'Lawful Neutral', 'Follows the law over chaos or good over evil'),
  (5, 'Neutral', 'Has no strong alignment towards good or evil'),
  (6, 'Chaotic Neutral', 'Values individual freedom over law or good over evil'),
  (7, 'Lawful Evil', 'Uses society and order to benefit themselves'),
  (8, 'Neutral Evil', 'Serves their own interests over good or law'),
  (9, 'Chaotic Evil', 'Values individual freedom and power over good or law');
