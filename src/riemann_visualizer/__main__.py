import pygame
import riemann_visualizer.visualizer as vis

def main():
    pygame.init()

    screen = pygame.display.set_mode([900, 900])

    eq = vis.RiemannSum(lambda x: x ** 2, (-2, 2), (-2, 2))
    visualizer = vis.Visualizer(eq, screen)

    running = True
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        visualizer.draw_equation()

        pygame.display.flip()

    pygame.quit()



if __name__=="__main__":
    main()