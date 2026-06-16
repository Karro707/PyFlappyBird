import os
import neat
import pygame
from flappy_bird_game import Bird, Pipe, Base, draw_window, WIN_WIDTH, WIN_HEIGHT

# ===== OPTYMALIZACJA: Ustaw False aby trening był 4x szybszy (bez okna) =====
DRAW_WINDOW = False
SPEED_MULTIPLIER = 120 if not DRAW_WINDOW else 30
# ============================================================================

def eval_genomes(genomes, config):

    nets = []
    ge = []
    birds = []

    #init populacji
    for genome_id, genome in genomes:
        genome.fitness = 0  #startowy fitness per genome
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        ge.append(genome)

    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True
    score = 0

    while run and len(birds) > 0:
        clock.tick(SPEED_MULTIPLIER)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1

        for x, bird in enumerate(birds):
            bird.move()

            ge[x].fitness += 0.1 

            #sensory birda 
            output = nets[x].activate((bird.y,
                                        abs(bird.y - pipes[pipe_ind].top),
                                        abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []
        birds_to_remove = []
        
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1 #kara za kolizje
                    birds_to_remove.append(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 10 #nagroda za pokonanie przeszkody
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds_to_remove.append(x)

        # Usuwaj z końca aby nie zniszczyć indeksy
        for x in sorted(birds_to_remove, reverse=True):
            birds.pop(x)
            nets.pop(x)
            ge.pop(x)

        base.move()

        # Rysuj tylko jeśli są żywe ptaki (i jeśli DRAW_WINDOW jest True)
        if DRAW_WINDOW and len(birds) > 0:
            draw_window(win, birds[0], pipes, base, score)

def run_neat(config_path):
    #wczytanie konfiguracji z pliku
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    #populacja
    p = neat.Population(config)

    #raporty
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    #50 generaccji
    winner = p.run(eval_genomes, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-fitness.txt")
    run_neat(config_path)