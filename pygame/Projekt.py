import pygame
import os
pygame.font.init()


SIRINA, VISINA = 900, 500
PROZOR = pygame.display.set_mode((SIRINA, VISINA))
pygame.display.set_caption("Prva igrica")

bijela = (255,255,255)
crna = (0, 0, 0)
CRVENA = (255, 0, 0)
ŽUTA = (255,255,0)

GRANICA = pygame.Rect(SIRINA//2 - 5, 0, 10, VISINA)

ŽIVOT_FONT = pygame.font.SysFont('comicsans',40)
POBJEDNIK_FONT = pygame.font.SysFont('comicsans',100)

FPS = 60
brzina = 5
brz_metka = 7
max_metci = 3
Širina_letjelice, Visina_letjelice = 55,40

#Definiranje eventova koje pygame može osluškivati kada se pogodi pojedini igrač
ŽUTA_HIT = pygame.USEREVENT + 1
CRVENA_HIT = pygame.USEREVENT + 2



Žuta_Letjelica_png = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
Žuta_Letjelica = pygame.transform.rotate(pygame.transform.scale(Žuta_Letjelica_png, (Širina_letjelice,Visina_letjelice)),90)

Crvena_Letjelica_png = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
Crvena_Letjelica = pygame.transform.rotate(pygame.transform.scale(Crvena_Letjelica_png, (Širina_letjelice,Visina_letjelice)),270)


SVEMIR = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (SIRINA, VISINA))


def drawing(crvena, žuta, metci_crveni, metci_žuti, crvena_život, žuta_život):
    PROZOR.blit(SVEMIR, (0,0))
    
    pygame.draw.rect(PROZOR, crna, GRANICA)
    
    crvena_život_text = ŽIVOT_FONT.render("Život: " + str(crvena_život), 1, bijela)
    žuta_život_text = ŽIVOT_FONT.render("Život: " + str(žuta_život), 1, bijela)
    PROZOR.blit(crvena_život_text, (SIRINA - crvena_život_text.get_width() - 10, 10))
    PROZOR.blit(žuta_život_text, (10,10))
    
    PROZOR.blit(Žuta_Letjelica,(žuta.x, žuta.y))
    PROZOR.blit(Crvena_Letjelica,(crvena.x, crvena.y))
    


    for metak in metci_crveni:
        pygame.draw.rect(PROZOR, CRVENA, metak)

    for metak in metci_žuti:
        pygame.draw.rect(PROZOR, ŽUTA, metak)
    
    pygame.display.update() 


def žuta_micanje(keys_pressed, žuta):
    if keys_pressed[pygame.K_a] and žuta.x - brzina > 0:  # slovo "a" -> Lijevo
        žuta.x -= brzina 
    if keys_pressed[pygame.K_d] and žuta.x + brzina + žuta.width < GRANICA.x:  #slovo "d" -> Desno
        žuta.x += brzina
    if keys_pressed[pygame.K_w] and žuta.y - brzina > 0:  # slovo "w" -> Gore
        žuta.y -= brzina
    if keys_pressed[pygame.K_s] and žuta.y + brzina + žuta.height < VISINA - 15:  #slovo "s" -> Dolje
        žuta.y += brzina


def crvena_micanje(keys_pressed, crvena):
    if keys_pressed[pygame.K_LEFT] and crvena.x - brzina > GRANICA.x + GRANICA.width:  # Lijevo
        crvena.x -= brzina
    if keys_pressed[pygame.K_RIGHT] and crvena.x + brzina + crvena.width < SIRINA:  # Desno
        crvena.x += brzina
    if keys_pressed[pygame.K_UP] and crvena.y - brzina > 0:  # Gore
        crvena.y -= brzina
    if keys_pressed[pygame.K_DOWN] and crvena.y + brzina + crvena.height < VISINA - 15:  # Dolje
        crvena.y += brzina


def handle_metci(metci_žuti, metci_crveni, žuta, crvena):
    for metak in metci_žuti:
        metak.x += brz_metka #Pomakni metak po x osi u desno
        if crvena.colliderect(metak):
            pygame.event.post(pygame.event.Event(CRVENA_HIT)) #Ako je pogođen crveni igrač emitaj event da je CRVENI POGOĐEN
            metci_žuti.remove(metak) #Pop-aj metak iz polja
        elif metak.x > SIRINA: #Metak je izašao iz prozora igre
            metci_žuti.remove(metak)
    
    for metak in metci_crveni:
        metak.x -= brz_metka #Pomakni metak po x osi u lijevo
        if žuta.colliderect(metak):
            pygame.event.post(pygame.event.Event(ŽUTA_HIT))
            metci_crveni.remove(metak)
        elif metak.x < 0:
            metci_crveni.remove(metak)


def pobjednik(text):
    draw_text = POBJEDNIK_FONT.render(text, 1, bijela)
    PROZOR.blit(draw_text, (SIRINA/2 - draw_text.get_width()/2, VISINA/2 - draw_text.get_height()/2)) #Nacrtaj na sredini prozora
    pygame.display.update()
    pygame.time.delay(5000) #Prikazuj tekst 5000 ms == 5s


def main():
    crvena = pygame.Rect(700, 300, Širina_letjelice, Visina_letjelice)
    žuta = pygame.Rect(100, 300, Širina_letjelice, Visina_letjelice)
    
    metci_crveni = []

    metci_žuti = []
    
    crvena_život = 10
    žuta_život = 10

    
    clock = pygame.time.Clock()
    game_running = True

    #Glavna petlja koja određuje kretanje igrača i pomicanje metaka
    while game_running:
        clock.tick(FPS)
        #Osluškuj sve eventove koje emita pygame
        for event in pygame.event.get():
            #Event QUIT => Ugasi igru
            if event.type == pygame.QUIT:
                game_running = False
                pygame.quit()

            #Provjera evenata tipki na tipkovnici
            if event.type == pygame.KEYDOWN:
                #Ako je pritisnuta tipka lijevi "Ctrl" i ako je žuti igrač ispalio manje od zadanih max metaka
                if event.key == pygame.K_LCTRL and len(metci_žuti) < max_metci:
                   metak = pygame.Rect(žuta.x + žuta.width, žuta.y + žuta.height//2 - 2, 10, 5) #Iscrtaj žuti metak
                   metci_žuti.append(metak) #Pushaj žuti metak u polje
                   
                #Ako je pritisnuta tipka desni "Ctrl" i ako je crveni igrač ispalio manje od zadanih max metaka
                if event.key == pygame.K_RCTRL and len(metci_crveni) < max_metci:
                    metak = pygame.Rect(crvena.x, crvena.y + crvena.height//2 - 2, 10, 5) #Iscrtaj crveni metak
                    metci_crveni.append(metak) #Pushaj crveni metak u polje
                    
            #Ako je pogođen crveni igrač oduzmi mu život
            if event.type == CRVENA_HIT:
                crvena_život -= 1


            #Ako je pogeđen žuti igrač oduzmi mu život
            if event.type == ŽUTA_HIT:
                žuta_život -= 1

    
        win_text = ""
        #Ako crveni ima 0 ili manje života spremi poruku
        if crvena_život <= 0:
            win_text = "Žuti je pobijedio!"

        #Ako žuti ima 0 ili manje života spremi poruku
        if žuta_život <= 0:
            win_text = "Crveni je pobijedio!"
        
        #Ako tekst postoji i različit je od praznog stringa pozovi funkciju pobjednik i predaj joj vrijednost varijable "win_text"
        if win_text != "":
            pobjednik(win_text)
            break


        #Osluškivanje svih evenata koji su pritisnuti na tipkovnici
        keys_pressed = pygame.key.get_pressed()
        žuta_micanje(keys_pressed, žuta)
        crvena_micanje(keys_pressed, crvena)
        
        handle_metci(metci_žuti, metci_crveni, žuta, crvena) #Funkcija koja određuje pomicanje metaka i je li meta pogođena
        
        drawing(crvena, žuta, metci_crveni, metci_žuti,crvena_život, žuta_život) #Iscrtaj prozor
    
    main()

if __name__ == "__main__":
    main()  