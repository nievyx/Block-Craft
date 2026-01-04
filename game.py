from ursina import *

#Pre-programmed Player
from ursina.prefabs.first_person_controller import FirstPersonController

import json
import os

SAVE_FILE = 'save_data.json'

def save_game():
    """Saves player position and all block data to a JSON file."""
    data = {
        "player_position": [player.x, player.y, player.z],
        "blocks": []
    }

    # Loop through all entities in the scene and save block positions & textures
    for entity in scene.entities:
        if isinstance(entity, Block):
            data["blocks"].append({
                "position": [entity.x, entity.y, entity.z],
                "texture": list(texture.keys())[list(texture.values()).index(entity.texture)],  # Get texture ID
                "breakable": entity.breakable
            })

    # Write data to file
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f, indent=4)

    print("Game Saved!")


def load_game():
    """Loads the player position and world blocks from a JSON file."""
    if not os.path.exists(SAVE_FILE):
        print("No save file found!")
        return

    with open(SAVE_FILE, 'r') as f:
        data = json.load(f)

    # Restore player position
    player.position = tuple(data["player_position"])

    # Clear the scene before loading new blocks
    for entity in scene.entities:
        if isinstance(entity, Block):
            destroy(entity)

    # Load blocks
    for block_data in data["blocks"]:
        Block(
            position=tuple(block_data["position"]),
            texture=texture[block_data["texture"]],
            breakable=block_data["breakable"]
        )

    print("Game Loaded!")


app = Ursina()

# load all assets
texture = {
    1: load_texture('Assets/Textures/Grass.png'),
    2: load_texture('Assets/Textures/Dirt.png'),
    3: load_texture('Assets/Textures/Brick.png'),
    4: load_texture('Assets/Textures/Wood.png'),
    5: load_texture('Assets/Textures/Stone.png'),

}

sky_background = load_texture('Assets/Textures/Sky.png') 
build_sound = Audio('Assets/SFX/Build_Sound.wav', loop=False, autoplay=False)

block_pick = 1

# Every click is a button, so we need to create a class
class Block(Button):
    def __init__(self, position=(0,0,0), texture=texture[1], breakable=True):
        super().__init__(
            parent=scene,
            position=position,
            model='Assets/Models/Block.obj',
            texture=texture,
            color=color.color(0,0,random.uniform(0.9,1)),
            highlight_color=color.pink,
            scale=0.5
        )
        self.breakable = breakable

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                build_sound.play()
                new_block = Block(position=self.position + mouse.normal, texture=texture[block_pick])
            elif key == 'right mouse down' and self.breakable:
                build_sound.play()
                destroy(self)

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_background, #TODO: sky.png texture not loading
            scale=150,
            double_sided=True
        )

#Custom 3d model class, Get more free models from https://itch.io/game-assets/free
class Tree(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent=scene,
            position=position,
            model='Assets/Models/lowpoly_tree_sample.obj',
            # Size of trees
            scale=(0.6,0.6,0.6),
            # A colliders is a box that surrounds the object, it allows the player to stop when they hit the object
            collider='mesh'
        )

def generate_trees(num_trees=3, terrain_size=20):
    for _ in range(num_trees):
        #Must put -1 as without the tree could be placed out of bounds
        x = random.randint(0, terrain_size-1)
        # How high in ground the tree is
        y = 3
        z = random.randint(0, terrain_size-1)
        Tree(position=(x,y,x))



def generate_terrain():
    #Can dig 5 deep
    height = 5
# Game world is 20 by 20
    for z in range(20):
        for x in range(20):
            
            for y in range(height):
                if y == height - 1:
                    Block(position=(x,y,z), texture=texture[1])
                elif y >= height-3:
                    Block(position=(x,y,z), texture=texture[2])
                else:
                    Block(position=(x,y,z), texture=texture[5])

            # Bedrock
            Block(position=(x,-1,z), texture=texture[5], breakable=False)

        #block = Block(position=(x,0,z))
       # bedrock = Block(position=(x,-1,z), texture=texture[5], breakable=False)


#Ursina will automatically look for update function and call it every frame
def update():
    #Pick which block to place
    global block_pick
    #1 - 6 is range of our blocks, if blocks increase, increase range
    for i in range(1,6):
        if held_keys[str(i)]:
            block_pick = i
            break

    if held_keys['escape']:
        save_game()
        application.quit()

    #Respawn player if they fall off the world
    if player.y < -10:
        player.position = (10,10,10)

    # Save game on "Shift + S" keys
    if held_keys['shift'] and held_keys['s']:
        save_game()

    # Load game on "Shift + L" keys
    if held_keys['shift'] and held_keys['l']:
        load_game()

# Player makes the game 3D
player = FirstPersonController(position=(10,10,10))
player.cursor.visible = False
sky = Sky()
#generate_trees()
generate_terrain()

if __name__ == '__main__':
    load_game()
    app.run()
