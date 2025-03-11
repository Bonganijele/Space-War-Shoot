# Copyright (c) 2025, Bongani. All rights reserved.
# This file is part of the Space War Shoot project.
# Author: Bongani Jele <jelebongani43@gmail.com>

########################################################################################
# Pygame doc: https://www.pygame.org/docs/ref/rect.html                                #
#                                                                                      #
# For just in case if you experience issues Email me or                                #
# contribute to github I'll appreciate support                                         #
#                                                                                      #
########################################################################################

import pygame
import subprocess
import game_engine as game_engine

  

pygame.init()

# Screen resolution
resolution = (1020, 600)
canvas = pygame.display.set_mode(resolution)
pygame.display.set_caption('Space War Shooter')

pygame.mixer_music.load("music/space.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Colors
color_text_button = (170, 170, 170)
bg_color_button = (100, 100, 100)
hover_color_button = (50, 50, 50)  # Light black for hover
color = (255, 255, 255)

# Load and scale background image
bg_image = pygame.image.load('assets/galaxy_space/parallax-space-background.png')
planet_image = pygame.image.load('assets/galaxy_space/parallax-space-big-planet.png')
space_stars = pygame.image.load('assets/galaxy_space/parallax-space-stars.png')

DEFAULT_IMAGE_SIZE = (1020, 600)

planet_size = (200, 200)  # Resize the planet if needed
stars_size = (120, 120)

planet_image = pygame.transform.scale(planet_image, planet_size)
space_stars = pygame.transform.scale(space_stars, stars_size)
bg_image = pygame.transform.scale(bg_image, DEFAULT_IMAGE_SIZE)

planet_x = resolution[0] - planet_size[0]
planet_y = 0

# Text font
small_font = pygame.font.SysFont('Corbel', 35)

# Button texts
play_text = small_font.render('Play', True, color)
options_text = small_font.render('Options', True, color)
quit_text = small_font.render('Quit', True, color)

# Button dimensions and positions
button_width, button_height = 200, 50
button_gap = 20  # Small gap between buttons

# Button positions for the main menu
center_x = canvas.get_width() // 2 - button_width // 2
play_button_y = canvas.get_height() // 2 - button_height - button_gap
options_button_y = canvas.get_height() // 2
quit_button_y = canvas.get_height() // 2 + button_height + button_gap


def get_system_volume():
    """Get the current system volume using `amixer`."""
    try:
        result = subprocess.run(
            ['amixer', 'sget', 'Master'],
            stdout=subprocess.PIPE,
            text=True
        )
        output = result.stdout
        for line in output.splitlines():
            if "%" in line:
                return int(line.split("[")[1].split("%")[0])
    except Exception as e:
        print(f"Error getting system volume: {e}")
    return 50  # Default volume

def set_system_volume(level):
    """Set the system volume using `amixer`."""
    try:
        subprocess.run(['amixer', 'sset', 'Master', f'{level}%'], stdout=subprocess.DEVNULL)
    except Exception as e:
        print(f"Error setting system volume: {e}")




def open_options_window():
    options_running = True

    # Load the background image (same as main menu)
    background_image = pygame.image.load('assets/galaxy_space/parallax-space-background.png')

    # Scale the background image to match the window size (resolution)
    background_image = pygame.transform.scale(background_image, resolution)

    # Load the additional image (for bottom-left corner)
    corner_image = pygame.image.load('assets/galaxy_space/parallax-space-ring-planet.png')
    other_planets = pygame.image.load('assets/galaxy_space/parallax-space-far-planets.png')

    # Optional: Scale the corner image if necessary
    corner_image = pygame.transform.scale(corner_image, (160, 160))  # Adjust the size as needed
    other_planets = pygame.transform.scale(other_planets, (180, 180))  # Adjust size of far planet image

    # Rotate the corner image (ring planet) 90 degrees to the right
    corner_image = pygame.transform.rotate(corner_image, -90)

    # Button alignment
    total_width = 3 * button_width + 2 * button_gap
    button_start_x = (resolution[0] - total_width) // 2
    button_y = 10

    # Toggle for showing the sliders
    show_sliders = False
    control_button_clicked = False

    # Slider settings
    slider_x = resolution[0] // 2 - 203
    slider_width = 410
    slider_height = 6
    slider_handle_width = 20
    slider_handle_height = 20

    # Initial system volume
    volume_level = get_system_volume()


    slider_handle_x = slider_x + int((volume_level / 100) * (slider_width - slider_handle_width))
    dragging = False

    # Initial music volume
    music_volume_level = 50  # Default music volume
    music_slider_handle_x = slider_x + int((music_volume_level / 100) * (slider_width - slider_handle_width))

    # Initial effect volume
    effect_volume_level = 50  # Default effect volume
    effect_slider_handle_x = slider_x + int((effect_volume_level / 100) * (slider_width - slider_handle_width))

    # Vertical space between sliders
    slider_gap = 100

    # Starting Y position for the first slider (volume)
    slider_y = button_y + button_height + 50
    # Position for the music volume slider
    music_slider_y = slider_y + slider_height + slider_gap

    # Position for the effect volume slider
    effect_slider_y = music_slider_y + slider_height + slider_gap

    while options_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                mouse_x, mouse_y = event.pos
                # Check if Control button is clicked
                if button_start_x <= mouse_x <= button_start_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    control_button_clicked = True
                    show_sliders = False  # Hide sliders when "Control" is active

                # Check if Volume button is clicked
                elif button_start_x + button_width + button_gap <= mouse_x <= button_start_x + 2 * button_width + button_gap and button_y <= mouse_y <= button_y + button_height:
                    show_sliders = True
                    control_button_clicked = False  # Hide control text when "Volume" is active


                # Check for Main Menu button click
                elif button_start_x + 2 * (button_width + button_gap) <= mouse[0] <= button_start_x + 3 * button_width + 2 * button_gap and button_y <= mouse[1] <= button_y + button_height:
                    options_running = False

                # Check if sliders are clicked
                if show_sliders:
                    if slider_x <= mouse[0] <= slider_x + slider_width and slider_y <= mouse[1] <= slider_y + slider_handle_height:
                        dragging = True
                    elif slider_x <= mouse[0] <= slider_x + slider_width and music_slider_y <= mouse[1] <= music_slider_y + slider_handle_height:
                        dragging = True
                    elif slider_x <= mouse[0] <= slider_x + slider_width and effect_slider_y <= mouse[1] <= effect_slider_y + slider_handle_height:
                        dragging = True

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            elif event.type == pygame.MOUSEMOTION and dragging:
                if show_sliders:
                    if slider_x <= event.pos[0] <= slider_x + slider_width and slider_y <= event.pos[1] <= slider_y + slider_handle_height:
                        slider_handle_x = max(slider_x, min(event.pos[0] - slider_handle_width // 2, slider_x + slider_width - slider_handle_width))
                        volume_level = int(((slider_handle_x - slider_x) / (slider_width - slider_handle_width)) * 100)
                        set_system_volume(volume_level)

                    elif slider_x <= event.pos[0] <= slider_x + slider_width and music_slider_y <= event.pos[1] <= music_slider_y + slider_handle_height:
                        music_slider_handle_x = max(slider_x, min(event.pos[0] - slider_handle_width // 2, slider_x + slider_width - slider_handle_width))
                        music_volume_level = int(((music_slider_handle_x - slider_x) / (slider_width - slider_handle_width)) * 100)
                        pygame.mixer.music.set_volume(music_volume_level / 100)

                    elif slider_x <= event.pos[0] <= slider_x + slider_width and effect_slider_y <= event.pos[1] <= effect_slider_y + slider_handle_height:
                        effect_slider_handle_x = max(slider_x, min(event.pos[0] - slider_handle_width // 2, slider_x + slider_width - slider_handle_width))
                        effect_volume_level = int(((effect_slider_handle_x - slider_x) / (slider_width - slider_handle_width)) * 100)
                        # set_effect_volume(effect_volume_level)
                        pygame.mixer.gunshot_sound.set()

        # Draw the options window with the background image scaled to window size
        canvas.blit(background_image, (0, 0))  # Draw background image

        # Draw the corner image in the bottom-left corner
        canvas.blit(corner_image, (0, resolution[1] - corner_image.get_height()))  # Position it at the bottom-left
        canvas.blit(other_planets, (resolution[0] // 4 - other_planets.get_width() // 2, resolution[1] // 2 - other_planets.get_height() // 2))  # Center the far planet image

        # Draw buttons
        draw_button(button_start_x, button_y, "Controls")
        draw_button(button_start_x + button_width + button_gap, button_y, "Audio")
        draw_button(button_start_x + 2 * (button_width + button_gap), button_y, "Main Menu")


        # Load arrow images (ensure these files exist in the specified path)
        arrow_up = pygame.image.load("assets/controls_img/upbutton.png")
        arrow_down = pygame.image.load("assets/controls_img/downbutton.png")
        arrow_left = pygame.image.load("assets/controls_img/leftbutton.png")
        arrow_right = pygame.image.load("assets/controls_img/rightbutton.png")
        space_btn = pygame.image.load("assets/controls_img/space.png")

        # Resize images (optional)
        arrow_size = (30, 30)  # Adjust size as needed
        arrow_up = pygame.transform.scale(arrow_up, arrow_size)
        arrow_down = pygame.transform.scale(arrow_down, arrow_size)
        arrow_left = pygame.transform.scale(arrow_left, arrow_size)
        arrow_right = pygame.transform.scale(arrow_right, arrow_size)
        space_btn = pygame.transform.scale(space_btn, arrow_size)

        # Draw "Control" instructions if the Control button is active
        if control_button_clicked:
            # Define control instructions and corresponding arrow images
            control_texts = [
                ("Move Up", arrow_up),
                ("Move Down", arrow_down),
                ("Move Left", arrow_left),
                ("Move Right", arrow_right),
                ("Shoot", space_btn)  # No image for "Shoot"
            ]

            # Get screen dimensions dynamically
            screen_surface = pygame.display.get_surface()
            screen_width, screen_height = screen_surface.get_width(), screen_surface.get_height()

            # Define dimensions for each text box
            text_box_width = 600
            text_box_height = 40
            text_box_gap = 10

            # Calculate total height of all text boxes and gaps
            total_text_boxes_height = len(control_texts) * (text_box_height + text_box_gap) - text_box_gap
            start_x = (screen_width - text_box_width) // 2
            start_y = (screen_height - total_text_boxes_height) // 2

            # Render each control instruction
            for i, (text, arrow_image) in enumerate(control_texts):
                # Calculate position
                current_y = start_y + i * (text_box_height + text_box_gap)
                pygame.draw.rect(canvas, (50, 50, 50),
                                 (start_x, current_y, text_box_width, text_box_height))  # Box background
                pygame.draw.rect(canvas, (255, 255, 255), (start_x, current_y, text_box_width, text_box_height),
                                 2)  # Border

                # Render arrow image (if available)
                if arrow_image:
                    canvas.blit(arrow_image, (start_x + 10, current_y + (text_box_height - arrow_size[1]) // 2))

                # Render text
                rendered_text = small_font.render(text, True, (255, 255, 255))
                text_x = start_x + 50  # Adjust text position to leave space for the arrow
                text_y = current_y + (text_box_height - rendered_text.get_height()) // 2
                canvas.blit(rendered_text, (text_x, text_y))

        # Draw sliders for Volume, Music, and Effect
        if show_sliders:
                # Get screen dimensions dynamically
                screen_surface = pygame.display.get_surface()
                screen_width, screen_height = screen_surface.get_width(), screen_surface.get_height()

                # Calculate total height of sliders and gaps
                num_sliders = 3
                total_sliders_height = num_sliders * slider_height + (num_sliders - 1) * slider_gap

                # Calculate starting positions to center the sliders
                start_x = (screen_width - slider_width) // 2
                start_y = (screen_height - total_sliders_height) // 2

                # Slider Y positions
                slider_y = start_y
                music_slider_y = slider_y + slider_height + slider_gap
                effect_slider_y = music_slider_y + slider_height + slider_gap


                # Drawing the sliders at the center
                pygame.draw.rect(canvas, (200, 200, 200),
                                 (start_x, slider_y, slider_width, slider_height), border_radius=5)  # Volume slider background
                pygame.draw.circle(canvas, (255, 255, 255),
                                   (slider_handle_x + slider_handle_width // 2, slider_y + slider_height // 2),
                                   slider_handle_height // 2)  # Volume slider handle

                pygame.draw.rect(canvas, (200, 200, 200),
                                 (start_x, music_slider_y, slider_width, slider_height), border_radius=5)  # Music slider background
                pygame.draw.circle(canvas, (255, 255, 255),
                                   (music_slider_handle_x + slider_handle_width // 2, music_slider_y + slider_height // 2),
                                   slider_handle_height // 2)  # Music slider handle

                pygame.draw.rect(canvas, (200, 200, 200),
                                 (start_x, effect_slider_y, slider_width, slider_height), border_radius=5)  # Effect slider background
                pygame.draw.circle(canvas, (255, 255, 255),
                                   (effect_slider_handle_x + slider_handle_width // 2, effect_slider_y + slider_height // 2),
                                   slider_handle_height // 2)  # Effect slider handle

                # Volume Text
                volume_text = small_font.render(f"Volume: {volume_level}%", True, color)

                canvas.blit(volume_text, (slider_x, slider_y - 40))

                # Music Volume Text
                music_volume_text = small_font.render(f"Music Volume: {music_volume_level}%", True, color)
                canvas.blit(music_volume_text, (slider_x, music_slider_y - 40))

                # Effect Volume Text
                effect_volume_text = small_font.render(f"Effect Volume: {effect_volume_level}%", True, color)
                canvas.blit(effect_volume_text, (slider_x, effect_slider_y - 40))


        pygame.display.update()

def draw_button(x, y, text):
    mouse = pygame.mouse.get_pos()
    hover = x <= mouse[0] <= x + button_width and y <= mouse[1] <= y + button_height
    button_color = hover_color_button if hover else bg_color_button
    pygame.draw.rect(canvas, button_color, [x, y, button_width, button_height])
    text_surface = small_font.render(text, True, color)
    canvas.blit(text_surface, (x + 50, y + 10))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False



        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            # Check for button clicks
            if center_x <= mouse[0] <= center_x + button_width:
                if play_button_y <= mouse[1] <= play_button_y + button_height:
                    print("Play button clicked")
                    game_engine.open_play_window()
                elif options_button_y <= mouse[1] <= options_button_y + button_height:
                    open_options_window()  # Open the options window
                elif quit_button_y <= mouse[1] <= quit_button_y + button_height:
                    pygame.quit()
                    running = False

    # Draw background
    canvas.blit(bg_image, (0,0))
    canvas.blit(space_stars, (250, 390))
    canvas.blit(planet_image, (planet_x, planet_y))

    # Get mouse position
    mouse = pygame.mouse.get_pos()
    
    
    

    # Draw buttons
    draw_button(center_x, play_button_y, 'Play')
    draw_button(center_x, options_button_y, "Options")
    draw_button(center_x, quit_button_y, 'Exit')

    pygame.display.update()