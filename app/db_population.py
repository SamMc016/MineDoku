from app import db
from app.models import Blocks, Conditions, User, Personal_Stats

blocks_to_add = [
    {"block_name": "Grass", "condition_compatibility": "1,5,7,10,12,13,15,17,18", "inv_texture_path": "assets/inventory_textures/grass.png", "face_texture_path": "assets/game_textures/grass.png"},
    {"block_name": "Sand", "condition_compatibility": "1,4,10,12,13,15", "inv_texture_path": "assets/inventory_textures/sand.png", "face_texture_path": "assets/game_textures/sand.png"},
    {"block_name": "Gravel", "condition_compatibility": "1,6,10,12,13,15", "inv_texture_path": "assets/inventory_textures/gravel.png", "face_texture_path": "assets/game_textures/gravel.png"},
    {"block_name": "Clay", "condition_compatibility": "1,6,10,11,12,13,15,17", "inv_texture_path": "assets/inventory_textures/clay.png", "face_texture_path": "assets/game_textures/clay.png"},
    {"block_name": "Dirt", "condition_compatibility": "1,7,10,11,12,13,15,16", "inv_texture_path": "assets/inventory_textures/dirt.png", "face_texture_path": "assets/game_textures/dirt.png"},
    {"block_name": "Cobblestone", "condition_compatibility": "1,6,11,12,13", "inv_texture_path": "assets/inventory_textures/cobblestone.png", "face_texture_path": "assets/game_textures/cobblestone.png"},
    {"block_name": "Stone", "condition_compatibility": "1,6,11,12,13,17", "inv_texture_path": "assets/inventory_textures/stone.png", "face_texture_path": "assets/game_textures/stone.png"},
    {"block_name": "Stone Bricks", "condition_compatibility": "1,6,12,13,14", "inv_texture_path": "assets/inventory_textures/stonebricks.png", "face_texture_path": "assets/game_textures/stonebricks.png"},
    {"block_name": "End Stone", "condition_compatibility": "2,4,12,13", "inv_texture_path": "assets/inventory_textures/endstone.png", "face_texture_path": "assets/game_textures/endstone.png"},
    {"block_name": "Oak Planks", "condition_compatibility": "1,7,10,12,13,14,15", "inv_texture_path": "assets/inventory_textures/oakplanks.png", "face_texture_path": "assets/game_textures/oakplanks.png"},
    {"block_name": "Oak Log", "condition_compatibility": "1,7,10,12,13,15,16,18", "inv_texture_path": "assets/inventory_textures/oaklog.png", "face_texture_path": "assets/game_textures/oaklog.png"},
    {"block_name": "Obsidian", "condition_compatibility": "1,2,9,11,12,13", "inv_texture_path": "assets/inventory_textures/obsidian.png", "face_texture_path": "assets/game_textures/obsidian.png"},
    {"block_name": "Netherrack", "condition_compatibility": "2,3,12,13", "inv_texture_path": "assets/inventory_textures/netherrack.png", "face_texture_path": "assets/game_textures/netherrack.png"},
    {"block_name": "Bedrock", "condition_compatibility": "1,2,6,11,13", "inv_texture_path": "assets/inventory_textures/bedrock.png", "face_texture_path": "assets/game_textures/bedrock.png"},
    {"block_name": "Magma Block", "condition_compatibility": "1,2,3,12,13,14", "inv_texture_path": "assets/inventory_textures/magmablock.png", "face_texture_path": "assets/game_textures/magmablock.png"},
    {"block_name": "Nether Brick", "condition_compatibility": "2,3,12,13,14", "inv_texture_path": "assets/inventory_textures/netherbrick.png", "face_texture_path": "assets/game_textures/netherbrick.png"},
    {"block_name": "Hay Bale", "condition_compatibility": "1,4,8,10,12,13,14,15,18", "inv_texture_path": "assets/inventory_textures/haybale.png", "face_texture_path": "assets/game_textures/haybale.png"},
    {"block_name": "Melon", "condition_compatibility": "1,5,8,10,12,13,14,15,17,18", "inv_texture_path": "assets/inventory_textures/melon.png", "face_texture_path": "assets/game_textures/melon.png"},
    {"block_name": "Pumpkin", "condition_compatibility": "1,8,10,12,13,15,16,18", "inv_texture_path": "assets/inventory_textures/pumpkin.png", "face_texture_path": "assets/game_textures/pumpkin.png"},
    {"block_name": "Diamond Block", "condition_compatibility": "1,9,12,13,14", "inv_texture_path": "assets/inventory_textures/diamondblock.png", "face_texture_path": "assets/game_textures/diamondblock.png"},
    {"block_name": "Gold Block", "condition_compatibility": "1,2,4,9,12,13,14", "inv_texture_path": "assets/inventory_textures/goldblock.png", "face_texture_path": "assets/game_textures/goldblock.png"},
    {"block_name": "Emerald Block", "condition_compatibility": "5,9,14", "inv_texture_path": "assets/inventory_textures/emeraldblock.png", "face_texture_path": "assets/game_textures/emeraldblock.png"},
    {"block_name": "Crafting Table", "condition_compatibility": "1,7,12,13,14,15,16", "inv_texture_path": "assets/inventory_textures/craftingtable.png", "face_texture_path": "assets/game_textures/craftingtable.png"},
    {"block_name": "Furnace", "condition_compatibility": "1,6,12,13,14,16", "inv_texture_path": "assets/inventory_textures/furnace.png", "face_texture_path": "assets/game_textures/furnace.png"},
    {"block_name": "White Wool", "condition_compatibility": "1,12,13,14,15", "inv_texture_path": "assets/inventory_textures/whitewool.png", "face_texture_path": "assets/game_textures/whitewool.png"},
    {"block_name": "Sponge", "condition_compatibility": "1,4,9,12,13,15", "inv_texture_path": "assets/inventory_textures/sponge.png", "face_texture_path": "assets/game_textures/sponge.png"},
    {"block_name": "TNT", "condition_compatibility": "1,3,9,12,13,14,15,16", "inv_texture_path": "assets/inventory_textures/tnt.png", "face_texture_path": "assets/game_textures/tnt.png"},
]

conditions_to_add = [
    {"condition_name": "Overworld Block"},
    {"condition_name": "Other World Block"},
    {"condition_name": "Red Block"},
    {"condition_name": "Yellow Block"},
    {"condition_name": "Green Block"},
    {"condition_name": "Grey Block"},
    {"condition_name": "Brown Block"},
    {"condition_name": "Foodstuff Block"},
    {"condition_name": "Luxury Block"},
    {"condition_name": "Surface Block"},
    {"condition_name": "Underground Block"},
    {"condition_name": "Block Found In Structures"},
    {"condition_name": "Naturally Spawning Block"},
    {"condition_name": "Craftable Block"},
    {"condition_name": "Block Able To Be Mined By Hand"},
    {"condition_name": "Interactable Block"},
    {"condition_name": "Block That Requires Silk Touch To Obtain"},
    {"condition_name": "Nature Block"}
]

friends_to_add = [
    {"username": "Alice", "email": "alice@test.com"},
    {"username": "Bob", "email": "bob@test.com"},
    {"username": "Charlie", "email": "charlie@test.com"},
    {"username": "Dana", "email": "dana@test.com"},
    {"username": "Ellen", "email": "ellen@test.com"},
    {"username": "Frank", "email": "frank@test.com"},
]

friends_stats_to_add = [
    {"user_id": 1, "total_games_played": 1, "total_games_won": 0, "lowest_uniqueness": 100, "average_uniqueness": 100, "daily_uniqueness": 100},
    {"user_id": 2, "total_games_played": 2, "total_games_won": 1, "lowest_uniqueness": 10, "average_uniqueness": 200, "daily_uniqueness": 200},
    {"user_id": 3, "total_games_played": 3, "total_games_won": 2, "lowest_uniqueness": 20, "average_uniqueness": 300, "daily_uniqueness": 300} ,   
    {"user_id": 4, "total_games_played": 4, "total_games_won": 3, "lowest_uniqueness": 30, "average_uniqueness": 400, "daily_uniqueness": 400},
    {"user_id": 5, "total_games_played": 5, "total_games_won": 4, "lowest_uniqueness": 40, "average_uniqueness": 500, "daily_uniqueness": 500},
    {"user_id": 6, "total_games_played": 6, "total_games_won": 5, "lowest_uniqueness": 200, "average_uniqueness": 600, "daily_uniqueness": 600}
]

def populate_blocks():

    for block_data in blocks_to_add:
        existing_block = Blocks.query.filter_by(
            block_name=block_data["block_name"]
        ).first()

        if existing_block is None:
            block = Blocks(
                block_name=block_data["block_name"],
                condition_compatibility=block_data["condition_compatibility"],
                inv_texture_path=block_data["inv_texture_path"],
                face_texture_path=block_data["face_texture_path"]
            )

            db.session.add(block)

    db.session.commit()

def populate_conditions():
    
    for condition_data in conditions_to_add:
        existing_condition = Conditions.query.filter_by(
            condition_name=condition_data["condition_name"]
        ).first()

        if existing_condition is None:
            condition = Conditions(
                condition_name=condition_data["condition_name"]
            )
        
            db.session.add(condition)
        db.session.commit()

def populate_users():

    for friends in friends_to_add:
        existing_user = User.query.filter_by(
            username=friends["username"]
        ).first()

        if existing_user is None:
            user = User(
                username=friends["username"],
                email=friends["email"],
                password_hash="dummy12345"
            )

            db.session.add(user)
    db.session.commit()

def populate_user_stats():

    for friend_stats in friends_stats_to_add:
        existing_stats = Personal_Stats.query.filter_by(
            user_id=friend_stats["user_id"]
        ).first()

        if existing_stats is None:
            stats = Personal_Stats(
                user_id=friend_stats["user_id"],
                total_games_played=friend_stats["total_games_played"],
                total_games_won=friend_stats["total_games_won"],
                lowest_uniqueness=friend_stats["lowest_uniqueness"],
                average_uniqueness=friend_stats["average_uniqueness"],
                daily_uniqueness=friend_stats["daily_uniqueness"]
            )
            db.session.add(stats)
    db.session.commit()