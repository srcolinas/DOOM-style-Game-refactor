# DOOM-style-Game-refactor

A few weeks ago, I saw [a great tutorial on game development on youtube](https://www.youtube.com/watch?v=ECqUrT7IdqQ). The tutorial shows how to create a DOOM-stlye 3D game in Python from scratch. The guy did a great job at explianing some of the basic ideas of 3D games and I truly appreciate his work. Howeve, I also noticed that the coding practices used through out the codebase are not what I consider to be best practices, so I decided to make a refactor to illustrate how I think the codebase could be improved for better maintainability.

I will try to show the impact of several design choices made on the overal maitainability of the project, as if it was a real life software project. Hopefully, the process shown in this post will help you improve the effectiveness of your own team, by having a codebase that is easier to maintain.


## Use most common conventions
There are tools that will give you an initial overview of the most common bad practices used in the codebase. In particular, let's use `flake8` for this job. The fact that I want to use `flake8` just means that I am familiar with it, but it doesn't necessarily mean that I think it is better at pointing bad practices. It is very likely that any tool will give you more or less the same results and will let you ignore any convention that you want to consciously ignore.

When you run `flake8 original`, you will se a huge list of errors, you can summarize them as *lines being too long* and *use of start (`*`) imports*. The first one makes it hard to read code in small screens, while the second makes it hard to keep track of where some objects are comming from. The second is particularly important when you are refactoring code, because you need to be able to quickly find when some objects are defined.

While I do not think that addressing such erros makes a big difference on the overall maintainability of the codebase, I do think it is a good easy first step, so let's do it. The more you can get for free the better, so I used `isort` and `black` to do some of the work automatically; this kind of tools also help you to reduce the amount of debate you have with your colleages about the likes and dislikes, simply follow the tool and people don't have to worry.

 You can see the end result in the [version one folder](./v1/). Now do `flake8 v1` to see that we do not have any issues. 

## Separate the Public from the Private
In the original implementation, you can see that every class defined a great deal of methods and attributes. We can argue whether such a number of attributes and methods is actually needed or not, but it would take us a long while, perhaps requiring to change the definition of some methods. Nonetheless, it is easy to notice that not all of the methods and attributes defined are being accessed outside of the class. For example, consider how the `RayCasting` class defines the `get_objects_to_render`, `ray_cast` and `update` methods, but only `update` is being called outside of the class. 

This is dangerous for a team project (and remember that you are also in the same team as your future self), because you don't possibly have time to supervise everyones' work to tell them what methods are supposed to be used outside of a class and which don't. Moreover, it prevent's you from changing things later without being afraid that something else will break. 

Within the Python community, it is common to distinguish what is supposed to be accessed and what doesn't by using underscore (`_`) before the a function or attribute. So let's follow that convention here to make the [version two of the game](./v2/).

The strategy I followed to achieve this is going class by class and looking for all of their attributes in the entire codebase, if they are only found inside the class definition, then I can safely add an `_` before the name. For example, you can see that the `add_sprite` method defined in the `ObjectHandler` class is only used by the class itself by searching in your IDE for the string `.add_sprite` and then replace it with `_add_sprite`. The same strategy would let you identify what attributes and methods are not used at all in the codebase, so we may as well remove them entirely.

The strategy sounds simple, but it wouldn't work in two cases:
1. Classes with inheritance relationships, like `NPC`, `AnimatedSprite` and so on.
2. Attributes with repeated names, like `screen` which appears in `Game` and `ObjectRenderer` (which happen to hold references to the same object).

For both cases you need to be more careful and only replace with the underscore named attribute after going through all apearances of the name. I know I can replace the `screen` of `ObjectRenderer` with `_screen`, because other places in the codebase doing `.screen` are doing it from the instance of `Game`, as in `self.game.screen`. 

## Add Type Annotations

In the last few years, the python community has started to use type annotations to improve the maintainability of their code. If you are wondering how this helps, imagine going to any function in the original implementation of the game and think of what are the possible values being passed around and count how long it takes you to figure out that something is an integer or a tuple of integers; with type annotations you get to know the answer inmediatly, which certainly reduces the amount of thinking and reading you have to do of the code. 

Type annotations are good to spot coding mistakes before you release your software. Imagine for example at some point you endup adding strings and integers, then a tool like `mypy`, which checks for correctness in type definitions will tell you that the addition is unsuported, instead of having a bug while playing with the application. We will use `mypy` to let us know when we should add type annotations to our code. If you do `mypy v2` you will find a great list of erros. Solving them will become [the third version of the codebase](./v3/).

Have you notice that nearly everywhere an instance of `main.Game` is a parameter to other classes? This makes things a bit more complicated. If you try to import the Game class to specify `__init__(self: game: main.Game) -> None`, then mypy will say everything is ok; however, the game will stop executing due to a circular dependency between the modudles. We can't allow this, we need to do only changes that allow the code to keep runing. The way to fix this is by defining the interface of the game class and use it for the type annotation. As long as such definition is not in `main`, things should work. 

## Make Code Testeable

## Depend Only on What is Used

## Make Sure There is Only One Reason to Change an Implementation

## Summary 


## DRAFT: DO NOT READ, I just want to keep it around in case I use it for the text later.

**Understanding the Codebase**

Before we start making changes, we need to make sure we understand the impact of the changes we are making. Achieving a perfect understanding of a big codebase is not an easy task, but thankfully ours is not too big; when it becomes to big, try to find isolated pieces on which you can start to contribute.

Understanding a codebase means being able to say:
1. What functions and classes depend on each other. 
2. What messages are being sent from one place to the codebase to the other, as well as when those messages are sent.

In otherwords, you need to know the interaction between all objects and functions in the codebase. To figure out and comunicate the dependencies, we can make a class diagram, for [the original implementation](./original/), we endup with the following:

```mermaid
classDiagram
    Game ..> Map
    Game ..> Player
    Game ..> ObjectRenderer
    Game ..> RayCasting
    Game ..> ObjectHandler
    Game ..> Weapon
    Game ..> Sound
    Game ..> PathFinding
    Game : +Surface screen
    Game : +Clock clock
    Game : +int delta_time
    Game : +bool global_trigger
    Game : +int global_event
    Game : +Map map
    Game : +Player player
    Game : +ObjectRenderer object_renderer
    Game : +RayCasting raycasting
    Game : +ObjectHandler object_handler
    Game : +Weapon weapon
    Game : +Sound sound
    Game : +PathFinding path_finding
    Game : +new_game()
    Game : +update()
    Game : +draw()
    Game : +check_events()
    Game : +run()

    Map ..> Game
    Map : +Game game
    Map : +list~list~int~~ mini_map
    Map : +dict world_map
    Map : +int rows
    Map : +int cols
    Map : +get_map()
    Map : +draw()

    Player ..> Game
    Player : +Game game
    Player : +float x
    Player : +float y
    Player : +float angle
    Player : +bool shot
    Player : +float health
    Player : +float int
    Player : +float health_recovery_delay
    Player : +int time_prev
    Player : +tuple~float,float~ pos
    Player : +tuple~int,int~ map_pos
    Player : +recover_health()
    Player : +check_health_recovery_delay() bool
    Player : +check_game_over()
    Player : +get_damage()
    Player : +single_fire_event()
    Player : +movement()
    Player : +check_wall()
    Player : +check_wall_collission()
    Player : +draw()
    Player : +mouse_control()
    Player : +update()

    ObjectRenderer ..> Game
    ObjectRenderer : +Game game
    ObjectRenderer : +Surface screen
    ObjectRenderer : +dict~int,Surface~ wall_textures
    ObjectRenderer : +Surface sky_image
    ObjectRenderer : +int sky_offset
    ObjectRenderer : +Surface blood_screen
    ObjectRenderer : +int digit_size
    ObjectRenderer : +list~Surface~ digit_images
    ObjectRenderer : +dict~str,Surface~ digits
    ObjectRenderer : +Surface game_over_image
    ObjectRenderer : +Surface win_image
    ObjectRenderer : +draw()
    ObjectRenderer : +win()
    ObjectRenderer : +game_over()
    ObjectRenderer : +draw_player_health()
    ObjectRenderer : +player_damage()
    ObjectRenderer : +draw_background()
    ObjectRenderer : +render_game_objects()
    ObjectRenderer : +load_wall_textures()
    ObjectRenderer : +get_texture()$

    RayCasting ..> Game
    RayCasting : +Game game
    RayCasting : +list ray_casting_result
    RayCasting : +list objects_to_render
    RayCasting : +dict~int,Surface~ wall_textures
    RayCasting : +get_objects_ro_render()
    RayCasting : +ray_cast()
    RayCasting : +update()

    ObjectHandler ..> Game
    ObjectHandler ..> SoldierNPC
    ObjectHandler ..> CacoDemonNPC
    ObjectHandler ..> CyberDemonNPC
    ObjectHandler ..> AnimatedSprite
    ObjectHandler : +Game game
    ObjectHandler : +list sprite_list
    ObjectHandler : +list npc_list
    ObjectHandler : +str npc_sprite_path
    ObjectHandler : +str static_sprite_path
    ObjectHandler : +str anim_sprite_path
    ObjectHandler : +int enemies
    ObjectHandler : +list~Type~NPC~~ npc_types
    ObjectHandler : +list~int~ weights
    ObjectHandler : +set~tuple~int,int~~ restricted_area
    ObjectHandler : +spawn_npc()
    ObjectHandler : +check_win()
    ObjectHandler : +update()
    ObjectHandler : +add_npc()
    ObjectHandler : +add_sprite()

    Sound ..> Game
    Sound : +Game game

    PathFinding ..> Game
    PathFinding : +Game game
    PathFinding : +list~list~int~~ map
    PathFinding : +tuple~list~int,int~~ ways
    PathFinding : +dict graph
    PathFinding : +get_path(start, goal)
    PathFinding : +bfs(int start, int goal, dict graph) dict~int,int~
    PathFinding : +get_next_nodes(int x, int y) list~tuple~float,float~~
    PathFinding : +get_graph

    SoldierNPC ..> Game
    SoldierNPC --|> NPC

    CacoDemonNPC ..> Game
    CacoDemonNPC --|> NPC

    CyberDemonNPC ..> Game
    CyberDemonNPC --|> NPC

    AnimatedSprite ..> Game
    AnimatedSprite --|> SpriteObject
    AnimatedSprite : +int animation_time
    AnimatedSprite : +str path
    AnimatedSprite : +deque~Surface~ images
    AnimatedSprite : +int animation_time_prev
    AnimatedSprite : +bool animation_trigger
    AnimatedSprite : +update()
    AnimatedSprite : +animate()
    AnimatedSprite : +check_animation_time()
    AnimatedSprite : +get_images(str path) deque~Surface~

    SpriteObject ..> Game
    SpriteObject : +Game game
    SpriteObject : +Player player
    SpriteObject : +float x
    SpriteObject : +float y
    SpriteObject : +Surface image
    SpriteObject : +int IMAGE_WIDTH
    SpriteObject : +int IMAGE_HALF_WIDTH
    SpriteObject : +float IMAGE_RATIO
    SpriteObject : +int dx
    SpriteObject : +int dy
    SpriteObject : +float theta
    SpriteObject : +int screen_x
    SpriteObject : +float dist
    SpriteObject : +float norm_dist
    SpriteObject : +int sprite_half_width
    SpriteObject : +float SPRITE_SCALE
    SpriteObject : +float SPITE_HEIGHT_SHIFT
    SpriteObject : +get_sprite_projection()
    SpriteObject : +get_sprite()
    SpriteObject : +update()

    NPC ..> Game
    NPC --|> AnimatedSprite
    NPC : +deque~Surface~ attack_images
    NPC : +deque~Surface~ death_images
    NPC : +deque~Surface~ iddle_images
    NPC : +deque~Surface~ pain_images
    NPC : +deque~Surface~ walk_images
    NPC : +int attack_dist
    NPC : +float speed
    NPC : +int size
    NPC : +int health
    NPC : +int attack_damage
    NPC : +float accuracy
    NPC : +bool alive
    NPC : +bool pain
    NPC : +bool ray_cast_value
    NPC : +int frame_counter
    NPC : +bool player_search_trigger
    NPC : +tuple~int,int~ map_poss
    NPC : +update()
    NPC : +check_wall(int x, int x)
    NPC : +check_wall_collision(int dx, int dy)
    NPC : +movement()
    NPC : +attack()
    NPC : +animate_death()
    NPC : +animate_pain()
    NPC : +check_hit_in_npc()
    NPC : +check_health()
    NPC : +run_logic()
    NPC : +ray_cast_player_npc()
    NPC : +draw_ray_cast()

    Weapon ..> Game
    Weapon --|> AnimatedSprite
    Weapon : +deque~Surface~ images
    Weapon : +tuple~int,int~ weapon_pos
    Weapon : +bool reloading
    Weapon : +int num_images
    Weapon : +int frame_counter
    Weapon : +int damage
    Weapon : +animate_shot()
    Weapon : +draw()
    Weapon : +update()
    
```

The class definitions not shown in the diagram are not defined in the game's codebase, but imported from `pygame` or from the standard library. Inherited proerties and methods are not shown either, as it is understood that all children classes have at least all properties of their parent class.

From this diagram, we notice that there is kind of a *main* class which is `Game` that imports most of the other classes and makes them interact, but those other classes also depend on `Game`. From this, you already know what places of the codebase you need to look into, if you are making a change in other places.

To help you understand how objects and functions interact, you can use sequence diagrams:

```mermaid
sequenceDiagram
    Main->>Game: run
    loop
        Game->>Player: single_fire_event 
        Player-->>Game: 
        Game->>Player: update
        Player->>Player: check_wall_collision
        Player->>Game: get delta_time
        Game-->>Player: 
        Player->>PyGame: get mouse position
        PyGame->>Player: 
        Player->>Player: recover_health
        Player->>PyGame: get_ticks
        PyGame->>Player: 
        Player-->>Game: 

        Game->>RayCasting: update
        rect rgb(255, 255, 240)
        Note over Game,RayCasting: required for the ray casting algorithm
        RayCasting->>Game: get player position in map
        Game-->>RayCasting: player.map_pos
        RayCasting->>Game: get world map
        Game-->>RayCasting: map.world_map
        end
        RayCasting->>RayCasting: get_objects_to_render
        RayCasting-->>Game: 

        Game->>ObjectHandler: update

        ObjectHandler-->>Game: 

        Game->>ObjectRenderer: draw
        ObjectRenderer-->>Game: 

        Game->>Weapon: draw
        Weapon-->>Game: 
        
    end
```

By using these two diagrams as a reference, we can start to question how relevant a particular function or class definition is and how it affects the overall functionality of our application. 

**A note on diagrams:** in the past, people use to make these kind of diagrams before starting to code anything, but the software engineering community has deprecated this practice, as it is hard to figure out everything in advance and people would endup having out of date diagrams; I recommend them as a tool mostly to communicate and understand what is already there.

**A note on documentation:** we find no docstrings in the codebase, likely because the author made a tutorial and that was his intention. In real life you can find yourself dealing with poorly documented code a lot of the times. One of the first great contributions you can make to the codebase is actually documenting it, it helps you make sure you understand the impact of a particular function and you can validate such newly added documentation with your colleages.

Now that we have got an understanding of the codebase, we can start improving it one step at the time. It is ok if the entire codebase is not understood before an *attempt* to refactor, it is very likely that the attempt will give you more information about it.