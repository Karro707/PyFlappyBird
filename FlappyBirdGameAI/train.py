"""
PyFlappyBird AI Training Script
Trains a NEAT-Python neural network to play Flappy Bird

Usage:
    python train.py

The trained network will be saved as best_genome.pkl
"""

import os
import sys
import pickle
import neat
import pygame
from evaluate import eval_genomes


def run_neat(config_path):
    """
    Run NEAT algorithm to train AI for Flappy Bird
    
    Args:
        config_path: Path to NEAT configuration file
    
    Returns:
        Best genome (winner) from training
    """
    # Load configuration
    config = neat.config.Config(
        neat.DefaultGenome, 
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet, 
        neat.DefaultStagnation,
        config_path
    )

    # Create initial population
    p = neat.Population(config)

    # Add reporters for progress tracking
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for 200 generations
    print("=" * 50)
    print("Starting NEAT training for Flappy Bird AI")
    print("=" * 50)
    
    winner = p.run(eval_genomes, 200)
    
    print("\n" + "=" * 50)
    print("Training complete!")
    print(f"Best genome fitness: {winner.fitness}")
    print("=" * 50)
    
    # Save winner to file
    with open("best_genome.pkl", "wb") as f:
        pickle.dump(winner, f)
    print("\n✅ Best genome saved as 'best_genome.pkl'")
    
    return winner


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-fitness.txt")
    
    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found at {config_path}")
        sys.exit(1)
    
    winner = run_neat(config_path)

