import os
import neat
import pygame
from flappy_bird_game import Bird, Pipe, Base, draw_window, WIN_WIDTH, WIN_HEIGHT

def eval_genomes(genomes, config):
    # Tablice do przechowywania ptaków, ich sieci neuronowych i obiektów genów
    nets = []
    ge = []
    birds = []

    # Inicjalizacja populacji
    for genome_id, genome in genomes:
        genome.fitness = 0  # Startowy poziom fitness
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

    # Pętla gry działa dopóki żyje chociaż jeden ptak w generacji
    while run and len(birds) > 0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # Ustalenie, na którą rurę (przeszkodę) patrzy obecnie ptak
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1

        # Aktualizacja stanu każdego ptaka
        for x, bird in enumerate(birds):
            bird.move()
            
            # Nagroda za przeżycie każdej klatki (promuje najdłuższy lot)
            ge[x].fitness += 0.1 

            # Sensory agenta: przekazanie danych do sieci (y ptaka, odległość od górnej i dolnej krawędzi luki)
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].top), abs(bird.y - pipes[pipe_ind].bottom)))

            # Sieć zwraca wartość logiczną - jeśli > 0.5, to ptak skacze
            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                # Sprawdzanie kolizji
                if pipe.collide(bird):
                    ge[x].fitness -= 1 # Kara za zderzenie z rurą
                    # Usunięcie ptaka, który zginął z list
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        # Premia za przejście przez przeszkodę
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5 # Duża nagroda za zdobycie punktu (przejście rury)
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)

        # Sprawdzanie czy ptak uderzył w ziemię lub uciekł za górną krawędź ekranu
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        # Rysowanie okna (rysujemy na podstawie pierwszego żyjącego ptaka, żeby kamera nadążała)
        draw_window(win, birds[0] if len(birds) > 0 else bird, pipes, base, score)

def run_neat(config_path):
    # Wczytanie konfiguracji hiperparametrów
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # Utworzenie populacji
    p = neat.Population(config)

    # Dodanie raportowania postępów do konsoli
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Uruchomienie funkcji fitness (eval_genomes) na maksymalnie 50 generacji
    winner = p.run(eval_genomes, 50)

if __name__ == "__main__":
    # Zakładam, że plik konfiguracyjny znajduje się w tym samym folderze
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run_neat(config_path)