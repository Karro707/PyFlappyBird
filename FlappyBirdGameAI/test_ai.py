"""
Test trained Flappy Bird AI
Loads the best genome and plays the game with AI control

Usage:
    python test_ai.py
"""

import os
import pickle
import neat
import pygame
from flappy_bird_game import Bird, Pipe, Base, draw_window, WIN_WIDTH, WIN_HEIGHT


def test_ai(genome, config):
    """
    Test a trained genome by playing one game with it
    
    Args:
        genome: The trained genome to test
        config: NEAT configuration
    """
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    
    pygame.init()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flappy Bird AI - Test Mode")
    clock = pygame.time.Clock()
    
    run = True
    score = 0
    
    print("Starting test... Press ESC or close window to quit")
    
    while run:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        
        pipe_ind = 0
        if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_ind = 1
        
        bird.move()
        
        # AI Decision
        output = net.activate((
            bird.y, 
            abs(bird.y - pipes[pipe_ind].top), 
            abs(bird.y - pipes[pipe_ind].bottom)
        ))
        
        if output[0] > 0.5:
            bird.jump()
        
        # Collision detection
        for pipe in pipes:
            if pipe.collide(bird):
                print(f"\nGame Over! Final Score: {score}")
                print(f"Bird crashed at Y position: {bird.y}")
                run = False
                break
        
        # Remove off-screen pipes and add new ones
        rem = []
        for pipe in pipes:
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                score += 1
                pipes.append(Pipe(700))
                print(f"Score: {score}")
            
            pipe.move()
        
        for r in rem:
            pipes.remove(r)
        
        # Check if bird hit the ground or flew too high
        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
            print(f"\nGame Over! Final Score: {score}")
            run = False
        
        base.move()
        draw_window(win, bird, pipes, base, score)
    
    pygame.quit()


def main():
    local_dir = os.path.dirname(__file__)
    genome_path = os.path.join(local_dir, "best_genome.pkl")
    config_path = os.path.join(local_dir, "config-fitness.txt")
    
    if not os.path.exists(genome_path):
        print(f"Error: Trained genome not found at {genome_path}")
        print("Please run 'python train.py' first to train the AI")
        return
    
    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found at {config_path}")
        return
    
    # Load configuration
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    
    # Load trained genome
    with open(genome_path, "rb") as f:
        winner = pickle.load(f)
    
    print("=" * 50)
    print("Testing trained Flappy Bird AI")
    print(f"Loaded genome with fitness: {winner.fitness}")
    print("=" * 50)
    
    test_ai(winner, config)


if __name__ == "__main__":
    main()
