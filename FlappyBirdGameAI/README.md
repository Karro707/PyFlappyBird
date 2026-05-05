# PyFlappyBird AI Training Guide

## Overview
This directory contains the AI training system for Flappy Bird using NEAT (NeuroEvolution of Augmenting Topologies) algorithm.

## Files

- **`flappy_bird_game.py`** - Flappy Bird game engine with Bird, Pipe, Base classes
- **`evaluate.py`** - Genome evaluation function for NEAT training
- **`train.py`** - Main training script (entry point)
- **`test_ai.py`** - Test and visualize trained AI playing the game
- **`config-fitness.txt`** - NEAT algorithm configuration

## Quick Start

### 1. Train the AI (50 generations)
```bash
cd FlappyBirdGameAI
python train.py
```

Output:
- Console: Real-time training progress and statistics
- File: `best_genome.pkl` - Trained neural network (saved after training completes)

**Expected duration:** ~5-10 minutes depending on your CPU

### 2. Test the Trained AI
```bash
python test_ai.py
```

The AI will play one game. Watch it navigate through pipes!
- **Press ESC** or close window to quit

## How It Works

### NEAT Configuration (`config-fitness.txt`)
- **Population size:** 50 birds per generation
- **Generations:** 50 (can be changed in `train.py`)
- **Fitness threshold:** 1000 (target score)
- **Mutation rates:** Configured for bird control learning

### Training Process (`train.py` → `evaluate.py`)

Each generation:

1. **Initialize Population** - 50 birds with random neural networks
2. **Evaluate Each Bird** - Play until collision/ground hit
   - **Inputs (3):** Bird Y position, distance to top pipe, distance to bottom pipe
   - **Output (1):** Jump decision (if > 0.5, bird jumps)
   - **Fitness Score:**
     - `+0.1` per frame (rewards survival)
     - `+5` per passed pipe (rewards progress)
     - `-1` per collision (punishes crashes)
3. **Selection & Mutation** - Keep best performers, breed with mutations
4. **Repeat** - Continue for 50 generations

### Neural Network Structure
- **Input layer:** 3 neurons (bird state sensors)
- **Output layer:** 1 neuron (jump action)
- **Hidden layers:** NEAT evolves these automatically based on fitness

## Expected Results

- **Early generations (1-10):** Birds barely survive, random jumps
- **Mid generations (15-30):** Birds start learning to dodge pipes
- **Late generations (40-50):** Specialized birds with scores >100

**Success criterion:** Find a genome that consistently scores >100

## Customization

### Adjust Training Parameters
In `train.py`, change:
```python
winner = p.run(eval_genomes, 50)  # Change 50 to desired generation count
```

### Tweak Fitness Rewards
In `evaluate.py`, modify:
```python
ge[x].fitness += 0.1  # Survival reward (lower = more selective)
g.fitness += 5        # Pipe passing bonus
ge[x].fitness -= 1    # Collision penalty
```

### Change NEAT Config
Edit `config-fitness.txt` for mutation rates, activation functions, etc.

## Troubleshooting

### ModuleNotFoundError: neat
```bash
pip install python-neat
```

### No sound/graphics
Ensure pygame is installed:
```bash
pip install pygame
```

### Training is slow
- Reduce generation count in `train.py`
- Close other applications
- The algorithm is computationally intensive by nature

### Test script won't run
Make sure `best_genome.pkl` exists (run `train.py` first)

## Project Phases Status

✅ **Complete:**
- Game implementation (Pygame)
- NEAT framework integration
- Sensor extraction (3 inputs)
- Fitness function
- Training loop
- Evaluation framework

📝 **To Be Added (Optional Improvements):**
- Visualization of neural network topology
- Population statistics graphs
- Multi-threaded evaluation for faster training
- Checkpoint/resume training feature
- Performance metrics logging

## Next Steps

1. Run `python train.py` to start training
2. Wait for 50 generations to complete (~10 minutes)
3. Run `python test_ai.py` to see results
4. Adjust parameters if needed and retrain

Good luck! 🐦
