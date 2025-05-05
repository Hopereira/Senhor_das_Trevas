import pygame
import sys
import random
import time
import os # Necessário para construir caminhos de forma segura

# --- Constantes ---
LARGURA_JANELA = 1280; ALTURA_JANELA = 720
LARGURA_TANQUE, ALTURA_TANQUE = 60, 60; LARGURA_ALIEN, ALTURA_ALIEN = 60, 30
LARGURA_MISSIL, ALTURA_MISSIL = 10, 30; LARGURA_MISSIL_ALIEN, ALTURA_MISSIL_ALIEN = 40, 40
LARGURA_BOMBA, ALTURA_BOMBA = 50, 45 # Tamanho da bomba
LARGURA_EXPLOSAO, ALTURA_EXPLOSAO = 70, 70

VELOCIDADE_TANQUE = 5; VELOCIDADE_MISSIL_JOGADOR = 7; VELOCIDADE_MISSIL_ALIEN = 5
VELOCIDADE_BOMBA = 1 # Velocidade lenta da bomba
VELOCIDADE_BASE_ALIEN_X = 1.5; VELOCIDADE_BASE_ALIEN_Y = 0.8
INCREMENTO_VELOCIDADE_POR_ONDA = 0.15; FATOR_AUMENTO_VEL_POR_PERDA = 1.5
MAX_MULTIPLICADOR_INTRA_ONDA = 10.0; FATOR_SEGUIDOR_BASE = 0.05

INTERVALO_ESPERA_TIRO = 1.5; INTERVALO_BASE_DISPARO_ALIEN = 1.1
REDUCAO_INTERVALO_DISPARO_POR_ONDA = 0.03; INTERVALO_MIN_DISPARO_ALIEN = 0.4
NUM_ALIENS_BASE = 7; INCREMENTO_ALIENS_POR_ONDA = 1; MAX_ALIENS = 20
LIMITE_DISPAROS_JOGADOR = 5; CHANCE_DISPARO_ALIEN = 15
CHANCE_SOLTAR_BOMBA = 50 # % de chance de soltar bomba (em vez de míssil, a partir da onda 2)
CHANCE_MUDAR_DIRECAO_ALIEN = 2
DURACAO_EXPLOSAO = 0.3; TEMPO_INVENCIBILIDADE = 2.0
PONTOS_POR_NAVE = 10; VIDAS_INICIAIS = 3
PONTOS_POR_BOMBA = 10 # Pontos por destruir bomba

COR_PRETA = (0,0,0); COR_BRANCA = (255,255,255); COR_DESTAQUE = (255,255,0)
COR_VERMELHA = (255,0,0); COR_VERDE = (0,255,0)

# --- Inicialização do Pygame e Mixer ---
pygame.init()
pygame.font.init()
try:
    pygame.mixer.init() # Inicializa o mixer de som
    mixer_iniciado = True
    print("Mixer de som iniciado com sucesso.")
except pygame.error as e:
    print(f"Erro ao iniciar o mixer de som: {e}")
    mixer_iniciado = False

janela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption("Senhor das Trevas"); clock = pygame.time.Clock(); FPS = 60

# --- Funções Auxiliares ---
def carregar_imagem(arquivo, largura, altura, alpha=True):
    caminho_completo = os.path.join("imagens", arquivo)
    try:
        imagem = pygame.image.load(caminho_completo)
        if alpha: imagem = imagem.convert_alpha()
        else: imagem = imagem.convert()
        imagem = pygame.transform.scale(imagem, (largura, altura))
        return imagem
    except pygame.error as e: print(f"Erro img '{caminho_completo}': {e}"); return None

def carregar_som(arquivo):
    if not mixer_iniciado: return None
    caminho_completo = os.path.join("sounds", arquivo)
    try: som = pygame.mixer.Sound(caminho_completo); print(f"Som '{caminho_completo}' OK."); return som
    except pygame.error as e: print(f"Erro som '{caminho_completo}': {e}"); return None

# --- Carregamento de Recursos ---
fundo = carregar_imagem("fundo.png", LARGURA_JANELA, ALTURA_JANELA, alpha=False)
tanque_img = carregar_imagem("tanque.png", LARGURA_TANQUE, ALTURA_TANQUE)
missil_img = carregar_imagem("missil.png", LARGURA_MISSIL, ALTURA_MISSIL)
missil_alien_img = carregar_imagem("missil_alien.png", LARGURA_MISSIL_ALIEN, ALTURA_MISSIL_ALIEN)
alien_img = carregar_imagem("alien.png", LARGURA_ALIEN, ALTURA_ALIEN)
bomba_img = carregar_imagem("bomba.png", LARGURA_BOMBA, ALTURA_BOMBA)
explosao_img = carregar_imagem("explosao.png", LARGURA_EXPLOSAO, ALTURA_EXPLOSAO)

# Fontes...
try:
    fonte_titulo=pygame.font.Font(None, 80); fonte_opcao=pygame.font.Font(None, 50)
    fonte_game_over=pygame.font.Font(None, 100); fonte_instrucao=pygame.font.Font(None, 40)
    fonte_hud=pygame.font.Font(None, 36)
except Exception as e:
     print(f"Erro ao carregar fontes: {e}")
     # Fallbacks...
     fonte_titulo=pygame.font.SysFont('Arial', 80); fonte_opcao=pygame.font.SysFont('Arial', 50)
     fonte_game_over=pygame.font.SysFont('Arial', 100); fonte_instrucao=pygame.font.SysFont('Arial', 40)
     fonte_hud=pygame.font.SysFont('Arial', 30)

if not fundo: pygame.quit(); sys.exit()

# Sons...
som_explosao = carregar_som("explosion.mp3")
som_tiro_tanque = carregar_som("missil_tank.mp3")
som_game_over = carregar_som("game_over.mp3")
# Música...
if mixer_iniciado:
    caminho_musica = os.path.join("sounds", "fundo.mp3")
    try: pygame.mixer.music.load(caminho_musica); pygame.mixer.music.set_volume(0.6); pygame.mixer.music.play(loops=-1); print("Música OK.")
    except pygame.error as e: print(f"Erro música '{caminho_musica}': {e}")

# --- Funções de Tela e Jogo ---

def mostrar_menu(surface, background, clock_menu):
    opcoes = ["Iniciar Jogo", "Sair"]
    opcao_selecionada = 0
    menu_ativo = True

    while menu_ativo:
        mouse_pos = pygame.mouse.get_pos()
        clique_mouse = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                elif event.key == pygame.K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if opcoes[opcao_selecionada] == "Iniciar Jogo":
                        return 'start'
                    elif opcoes[opcao_selecionada] == "Sair":
                        return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clique_mouse = True

        surface.blit(background, (0, 0))
        texto_titulo = fonte_titulo.render("Senhor das Trevas", True, COR_BRANCA)
        rect_titulo = texto_titulo.get_rect(center=(LARGURA_JANELA // 2, ALTURA_JANELA // 4))
        surface.blit(texto_titulo, rect_titulo)

        y_pos_opcao = ALTURA_JANELA // 2
        for i, opcao_texto in enumerate(opcoes):
            cor = COR_DESTAQUE if i == opcao_selecionada else COR_BRANCA
            texto_opcao = fonte_opcao.render(opcao_texto, True, cor)
            rect_opcao = texto_opcao.get_rect(center=(LARGURA_JANELA // 2, y_pos_opcao + i * 60))

            if rect_opcao.collidepoint(mouse_pos):
                texto_opcao = fonte_opcao.render(opcao_texto, True, COR_DESTAQUE)
                opcao_selecionada = i
                if clique_mouse:
                    if opcoes[i] == "Iniciar Jogo":
                        return 'start'
                    elif opcoes[i] == "Sair":
                        return 'quit'
            surface.blit(texto_opcao, rect_opcao)

        pygame.display.flip()
        clock_menu.tick(FPS)

# <<<<< FUNÇÃO mostrar_game_over CORRIGIDA >>>>>
def mostrar_game_over(surface, background, clock_go):
    # Para a música principal (com fade out) e toca o som de game over
    if mixer_iniciado:
        pygame.mixer.music.fadeout(1500) # Fade out em 1.5 segundos
    if som_game_over:
        som_game_over.play()

    texto_go=fonte_game_over.render("GAME OVER", True, COR_VERMELHA); rect_go=texto_go.get_rect(center=(LARGURA_JANELA//2, ALTURA_JANELA//2 - 60))
    texto_inst=fonte_instrucao.render("Pressione ESPAÇO ou ENTER para voltar ao menu", True, COR_BRANCA); rect_inst=texto_inst.get_rect(center=(LARGURA_JANELA//2, ALTURA_JANELA//2 + 40))
    esperando_input=True; fade_surface=pygame.Surface((LARGURA_JANELA, ALTURA_JANELA)); fade_surface.fill(COR_PRETA); fade_surface.set_alpha(150); start_time=time.time()

    while esperando_input:
        surface.blit(background, (0,0)); surface.blit(fade_surface, (0,0)); surface.blit(texto_go, rect_go); surface.blit(texto_inst, rect_inst)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type==pygame.KEYDOWN:
                 # Adiciona uma pequena espera para evitar registro acidental da mesma tecla
                 if time.time()-start_time > 0.5:
                    if event.key==pygame.K_SPACE or event.key==pygame.K_RETURN:
                        esperando_input = False # Termina o loop da tela de game over
                        # <<<< INDENTAÇÃO CORRIGIDA ABAIXO >>>>
                        # Reinicia a música ao voltar para o menu
                        if mixer_iniciado: # Indentado sob o if event.key...
                            try: # Indentado sob o if mixer_iniciado...
                                pygame.mixer.music.load(os.path.join("sounds", "fundo.mp3"))
                                pygame.mixer.music.play(loops=-1)
                            except pygame.error as e: # Alinhado com o try...
                                print(f"Erro reiniciar música: {e}")
        clock_go.tick(FPS)


def criar_onda_aliens(num_onda, num_aliens_base, inc_aliens, max_aliens, vel_base_x, vel_base_y, inc_vel):
    naves_onda=[]; num_aliens=min(num_aliens_base+(num_onda-1)*inc_aliens, max_aliens); mult_velocidade_onda=1.0+(num_onda-1)*inc_vel
    vel_x_atual=vel_base_x*mult_velocidade_onda; vel_y_atual=vel_base_y*mult_velocidade_onda; print(f"--- Onda {num_onda} --- Aliens: {num_aliens}, Vel Base: {mult_velocidade_onda:.2f}")
    for i in range(num_aliens):
        nx=random.randint(0,LARGURA_JANELA-LARGURA_ALIEN); ny=random.randint(50,ALTURA_JANELA//2-ALTURA_ALIEN-100)
        speed_x_base_lider=random.choice([-vel_x_atual,vel_x_atual]) if i==0 else 0; speed_y_base_lider=random.choice([-vel_y_atual,vel_y_atual]) if i==0 else 0
        nave={'rect':pygame.Rect(nx,ny,LARGURA_ALIEN,ALTURA_ALIEN),'speed_x_base':speed_x_base_lider,'speed_y_base':speed_y_base_lider}
        naves_onda.append(nave)
    return naves_onda

# --- Programa Principal ---
executando_programa = True
while executando_programa:
    escolha = mostrar_menu(janela, fundo, clock)
    if escolha == 'quit': executando_programa = False; break
    elif escolha == 'start':
        # Reset/Inicialização do JOGO
        pontuacao=0; vidas=VIDAS_INICIAIS; onda_atual=1; fundo_x=0
        multiplicador_intra_onda=1.0

        x_tanque=LARGURA_JANELA//2-LARGURA_TANQUE//2; y_tanque=ALTURA_JANELA-ALTURA_TANQUE-50
        tanque_rect=pygame.Rect(x_tanque,y_tanque,LARGURA_TANQUE,ALTURA_TANQUE)
        tanque_visivel=True; tanque_invencivel=False; tempo_fim_invencibilidade=0

        misseis_jogador=[]; misseis_alien=[]; explosoes_ativas=[]
        bombas_ativas = [] # Lista para bombas

        naves = criar_onda_aliens(onda_atual,NUM_ALIENS_BASE,INCREMENTO_ALIENS_POR_ONDA,MAX_ALIENS,
                                 VELOCIDADE_BASE_ALIEN_X,VELOCIDADE_BASE_ALIEN_Y,INCREMENTO_VELOCIDADE_POR_ONDA)

        contador_disparos_sequenciais=0; ultimo_disparo_jogador=0
        intervalo_espera_jogador_atual=0; pode_disparar_jogador=True
        intervalo_disparo_alien_atual=max(INTERVALO_BASE_DISPARO_ALIEN-(onda_atual-1)*REDUCAO_INTERVALO_DISPARO_POR_ONDA,INTERVALO_MIN_DISPARO_ALIEN)
        ultimo_disparo_alien=time.time()

        rodando_jogo = True; game_over = False; quit_solicitado = False

        if mixer_iniciado and not pygame.mixer.music.get_busy():
             try: pygame.mixer.music.play(loops=-1)
             except pygame.error as e: print(f"Erro play música início jogo: {e}")

        # --- Loop Principal do Jogo ---
        while rodando_jogo:
            tempo_atual=time.time(); delta_time=clock.tick(FPS)/1000.0

            # Eventos
            for event in pygame.event.get():
                if event.type==pygame.QUIT: rodando_jogo=False; quit_solicitado=True
                elif event.type==pygame.KEYDOWN:
                    if not game_over and event.key==pygame.K_SPACE and pode_disparar_jogador and tanque_visivel:
                        if som_tiro_tanque: som_tiro_tanque.play()
                        missil_x=tanque_rect.centerx-LARGURA_MISSIL//2; missil_y=tanque_rect.top
                        misseis_jogador.append(pygame.Rect(missil_x,missil_y,LARGURA_MISSIL,ALTURA_MISSIL))
                        contador_disparos_sequenciais+=1; ultimo_disparo_jogador=tempo_atual
                        if contador_disparos_sequenciais>=LIMITE_DISPAROS_JOGADOR: pode_disparar_jogador=False; intervalo_espera_jogador_atual=INTERVALO_ESPERA_TIRO

            # Invencibilidade
            if tanque_invencivel and tempo_atual >= tempo_fim_invencibilidade:
                tanque_invencivel = False; tanque_visivel = True

            # Atualizações (se não for game over)
            if not game_over:
                # Cooldown jogador
                if not pode_disparar_jogador and tempo_atual - ultimo_disparo_jogador >= intervalo_espera_jogador_atual:
                    pode_disparar_jogador=True; contador_disparos_sequenciais=0; intervalo_espera_jogador_atual=0

                # Disparo aliens (Míssil OU Bomba a partir da Onda 2)
                if naves and tempo_atual - ultimo_disparo_alien >= intervalo_disparo_alien_atual:
                    for nave_info in naves:
                        if random.randint(1, 100) <= CHANCE_DISPARO_ALIEN:
                            soltar_bomba = False
                            if onda_atual >= 2 and bomba_img:
                                if random.randint(1, 100) <= CHANCE_SOLTAR_BOMBA:
                                    soltar_bomba = True
                            if soltar_bomba:
                                bomba_x = nave_info['rect'].centerx - LARGURA_BOMBA // 2
                                bomba_y = nave_info['rect'].bottom
                                bombas_ativas.append(pygame.Rect(bomba_x, bomba_y, LARGURA_BOMBA, ALTURA_BOMBA))
                            else:
                                missil_ax=nave_info['rect'].centerx-LARGURA_MISSIL_ALIEN//2
                                missil_ay=nave_info['rect'].bottom
                                misseis_alien.append(pygame.Rect(missil_ax,missil_ay,LARGURA_MISSIL_ALIEN,ALTURA_MISSIL_ALIEN))
                    ultimo_disparo_alien = tempo_atual

                # Movimento tanque
                if tanque_visivel:
                    keys=pygame.key.get_pressed();
                    if keys[pygame.K_LEFT] and tanque_rect.left>0: tanque_rect.x-=VELOCIDADE_TANQUE
                    if keys[pygame.K_RIGHT] and tanque_rect.right<LARGURA_JANELA: tanque_rect.x+=VELOCIDADE_TANQUE

                # Movimento aliens
                if naves:
                    mult_vel_onda = 1.0+(onda_atual-1)*INCREMENTO_VELOCIDADE_POR_ONDA; lider = naves[0]; lider_speed_x_base = lider['speed_x_base']; lider_speed_y_base = lider['speed_y_base']
                    lider_speed_x_final = lider_speed_x_base*multiplicador_intra_onda; lider_speed_y_final = lider_speed_y_base*multiplicador_intra_onda
                    lider['rect'].x+=lider_speed_x_final; lider['rect'].y+=lider_speed_y_final
                    if random.randint(1,100)<=CHANCE_MUDAR_DIRECAO_ALIEN: vel_base_x_onda=VELOCIDADE_BASE_ALIEN_X*mult_vel_onda; vel_base_y_onda=VELOCIDADE_BASE_ALIEN_Y*mult_vel_onda; lider['speed_x_base']=random.choice([-vel_base_x_onda,vel_base_x_onda]); lider['speed_y_base']=random.choice([-vel_base_y_onda,vel_base_y_onda])
                    if lider['rect'].left<0: lider['rect'].left=0; lider['speed_x_base']=abs(lider['speed_x_base'])
                    elif lider['rect'].right>LARGURA_JANELA: lider['rect'].right=LARGURA_JANELA; lider['speed_x_base']=-abs(lider['speed_x_base'])
                    if lider['rect'].top<10: lider['rect'].top=10; lider['speed_y_base']=abs(lider['speed_y_base'])
                    elif lider['rect'].bottom>ALTURA_JANELA//2: lider['rect'].bottom=ALTURA_JANELA//2; lider['speed_y_base']=-abs(lider['speed_y_base'])
                    fator_seguidor=FATOR_SEGUIDOR_BASE
                    for i in range(1,len(naves)):
                        atual=naves[i]['rect']; anterior=naves[i-1]['rect']; dist_x=anterior.centerx-atual.centerx; dist_y=anterior.centery-atual.centery
                        fator_mov=fator_seguidor*mult_vel_onda*multiplicador_intra_onda
                        if abs(dist_x)>LARGURA_ALIEN*0.6 or abs(dist_y)>ALTURA_ALIEN*0.6: delta_x=int(dist_x*fator_mov); delta_y=int(dist_y*fator_mov); atual.x+=delta_x; atual.y+=delta_y

            # Movimento mísseis e bombas (sempre)
            for m in misseis_jogador: m.y -= VELOCIDADE_MISSIL_JOGADOR
            for ma in misseis_alien: ma.y += VELOCIDADE_MISSIL_ALIEN
            for b in bombas_ativas: b.y += VELOCIDADE_BOMBA

            # Remoção de projéteis fora da tela
            misseis_jogador = [m for m in misseis_jogador if m.bottom > 0]
            misseis_alien = [ma for ma in misseis_alien if ma.top < ALTURA_JANELA]
            bombas_ativas = [b for b in bombas_ativas if b.top < ALTURA_JANELA]

            # Atualizar explosões
            explosoes_ativas = [exp for exp in explosoes_ativas if tempo_atual-exp['start_time'] <= DURACAO_EXPLOSAO]

            # Colisões (se não for game over)
            if not game_over:
                # Colisão Míssil Jogador -> Bomba
                misseis_atingiram_bomba = set(); bombas_atingidas_por_missil = set()
                for i, missil_rect in enumerate(misseis_jogador):
                    for j, bomba_rect in enumerate(bombas_ativas):
                        if i not in misseis_atingiram_bomba and j not in bombas_atingidas_por_missil:
                            if missil_rect.colliderect(bomba_rect):
                                misseis_atingiram_bomba.add(i); bombas_atingidas_por_missil.add(j)
                                pontuacao += PONTOS_POR_BOMBA; print(f"Bomba destruída! +{PONTOS_POR_BOMBA} pts.")
                                if som_explosao: som_explosao.play()
                                if explosao_img: expl_rect = explosao_img.get_rect(center=bomba_rect.center); explosoes_ativas.append({'rect': expl_rect, 'start_time': tempo_atual})
                if misseis_atingiram_bomba: misseis_jogador = [m for idx, m in enumerate(misseis_jogador) if idx not in misseis_atingiram_bomba]
                if bombas_atingidas_por_missil: bombas_ativas = [b for idx, b in enumerate(bombas_ativas) if idx not in bombas_atingidas_por_missil]

                # Colisão Míssil Jogador -> Alien
                misseis_atingidos_indices=set(); aliens_atingidos_indices=set(); aliens_atingidos_neste_frame=0
                for i, missil_rect in enumerate(misseis_jogador):
                    for j, nave_info in enumerate(naves):
                        if j not in aliens_atingidos_indices:
                            if missil_rect.colliderect(nave_info['rect']):
                                misseis_atingidos_indices.add(i); aliens_atingidos_indices.add(j)
                                pontuacao+=PONTOS_POR_NAVE; aliens_atingidos_neste_frame+=1
                                if som_explosao: som_explosao.play()
                                if explosao_img: expl_rect=explosao_img.get_rect(center=nave_info['rect'].center); explosoes_ativas.append({'rect':expl_rect,'start_time':tempo_atual})
                if aliens_atingidos_neste_frame > 0:
                    multiplicador_intra_onda *= (FATOR_AUMENTO_VEL_POR_PERDA ** aliens_atingidos_neste_frame)
                    multiplicador_intra_onda = min(multiplicador_intra_onda, MAX_MULTIPLICADOR_INTRA_ONDA)
                if aliens_atingidos_indices: naves=[nave for idx,nave in enumerate(naves) if idx not in aliens_atingidos_indices]
                if misseis_atingidos_indices: misseis_jogador=[m for idx,m in enumerate(misseis_jogador) if idx not in misseis_atingidos_indices]

                # Colisão Projéteis Alien -> Tanque
                if tanque_visivel and not tanque_invencivel:
                    atingido = False; misseis_alien_colidiram=set(); bombas_colidiram_tanque = set()
                    for i, missil_alien_rect in enumerate(misseis_alien):
                        if tanque_rect.colliderect(missil_alien_rect): misseis_alien_colidiram.add(i); atingido=True; break
                    if not atingido:
                        for i, bomba_rect in enumerate(bombas_ativas):
                            if tanque_rect.colliderect(bomba_rect): bombas_colidiram_tanque.add(i); atingido=True; break
                    if atingido:
                        if som_explosao: som_explosao.play()
                        vidas-=1; print(f"Vida perdida! Vidas: {vidas}")
                        if explosao_img: expl_rect=explosao_img.get_rect(center=tanque_rect.center); explosoes_ativas.append({'rect':expl_rect,'start_time':tempo_atual})
                        if vidas<=0: print("Game Over!"); game_over=True; tanque_visivel=False
                        else: tanque_invencivel=True; tanque_visivel=False; tempo_fim_invencibilidade=tempo_atual+TEMPO_INVENCIBILIDADE; print(f"Invencível até {tempo_fim_invencibilidade:.2f}")
                    if misseis_alien_colidiram: misseis_alien=[m for idx,m in enumerate(misseis_alien) if idx not in misseis_alien_colidiram]
                    if bombas_colidiram_tanque: bombas_ativas=[b for idx,b in enumerate(bombas_ativas) if idx not in bombas_colidiram_tanque]

            # Verificar Fim da Onda
            if not game_over and not naves and not any('rect' in exp for exp in explosoes_ativas):
                onda_atual+=1; multiplicador_intra_onda = 1.0; print("-" * 20)
                naves = criar_onda_aliens(onda_atual,NUM_ALIENS_BASE,INCREMENTO_ALIENS_POR_ONDA,MAX_ALIENS,VELOCIDADE_BASE_ALIEN_X,VELOCIDADE_BASE_ALIEN_Y,INCREMENTO_VELOCIDADE_POR_ONDA)
                intervalo_disparo_alien_atual=max(INTERVALO_BASE_DISPARO_ALIEN-(onda_atual-1)*REDUCAO_INTERVALO_DISPARO_POR_ONDA,INTERVALO_MIN_DISPARO_ALIEN)
                print(f"Intervalo disparo alien: {intervalo_disparo_alien_atual:.2f}s"); time.sleep(0.5)

            # Desenho
            rel_x=fundo_x%fundo.get_rect().width; janela.blit(fundo,(rel_x-fundo.get_rect().width,0))
            if rel_x<LARGURA_JANELA: janela.blit(fundo,(rel_x,0)); fundo_x-=0.5
            # HUD
            texto_pontos=fonte_hud.render(f"Pontos: {pontuacao}",True,COR_VERDE); janela.blit(texto_pontos,(10,10))
            texto_vidas=fonte_hud.render(f"Vidas: {vidas}",True,COR_VERDE); rect_vidas=texto_vidas.get_rect(topright=(LARGURA_JANELA-10,10)); janela.blit(texto_vidas,rect_vidas)
            texto_onda=fonte_hud.render(f"Onda: {onda_atual}",True,COR_BRANCA); rect_onda=texto_onda.get_rect(midtop=(LARGURA_JANELA//2,10)); janela.blit(texto_onda,rect_onda)
            # Tanque
            if tanque_visivel: janela.blit(tanque_img, tanque_rect.topleft)
            elif tanque_invencivel and int(tempo_atual*10)%2==0: janela.blit(tanque_img, tanque_rect.topleft)
            # Aliens, Mísseis
            for nave_info in naves: janela.blit(alien_img, nave_info['rect'].topleft)
            for m in misseis_jogador: janela.blit(missil_img, m.topleft)
            for ma in misseis_alien: janela.blit(missil_alien_img, ma.topleft)
            # Bombas
            if bomba_img:
                for b in bombas_ativas: janela.blit(bomba_img, b.topleft)
            # Explosões
            if explosao_img:
                for exp in explosoes_ativas: janela.blit(explosao_img, exp['rect'].topleft)

            pygame.display.flip()

            # Sair do loop do jogo
            if game_over and not explosoes_ativas: rodando_jogo = False

        # Fim do loop do jogo atual
        if quit_solicitado: executando_programa = False; break
        if game_over: mostrar_game_over(janela, fundo, clock)

# --- Fim do Programa ---
print("Encerrando o jogo...")
pygame.quit()
sys.exit()