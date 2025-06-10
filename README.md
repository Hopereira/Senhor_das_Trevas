# 👾 Senhor das Trevas 👾

Bem-vindo ao "Senhor das Trevas", um jogo de tiro espacial no estilo arcade clássico, desenvolvido em Python com a biblioteca Pygame. Prepare-se para defender a Terra de hordas intermináveis de invasores alienígenas!

![Placeholder para GIF do Jogo](https://placehold.co/800x400/000000/FFFFFF?text=Gameplay+Senhor+das+Trevas)


---

## 🎯 Sobre o Jogo

Em "Senhor das Trevas", você controla o último tanque de defesa da Terra. Sua missão é sobreviver ao maior número de ondas de ataque que conseguir, destruindo naves alienígenas que se tornam mais rápidas, numerosas e agressivas a cada nova onda.

## ✨ Funcionalidades

* **Jogabilidade Clássica:** Inspirado em grandes clássicos como Space Invaders, com uma jogabilidade simples e viciante.
* **Dificuldade Progressiva:** As ondas de inimigos aumentam em número e velocidade, e o intervalo entre os disparos diminui, garantindo um desafio crescente.
* **Movimento Dinâmico dos Inimigos:** Os alienígenas se movem em formação, seguindo um líder, tornando seu padrão de voo menos previsível.
* **Variedade de Ameaças:** Enfrente não apenas os mísseis rápidos dos aliens, mas também bombas lentas e poderosas que são introduzidas a partir da segunda onda.
* **Mecânicas de Sobrevivência:** Após ser atingido, o jogador recebe um curto período de invencibilidade para poder se reposicionar.
* **Sistema de HUD e Pontuação:** Acompanhe sua pontuação, número de vidas e a onda atual em tempo real.
* **Efeitos Sonoros e Música:** Efeitos de tiro, explosão e uma trilha sonora de fundo para uma imersão completa.

## 🕹️ Como Jogar

* **Seta Esquerda (`←`)**: Move o tanque para a esquerda.
* **Seta Direita (`→`)**: Move o tanque para a direita.
* **Barra de Espaço (`Espaço`)**: Dispara um míssil.
    * *Atenção:* Você pode disparar um número limitado de mísseis em sequência antes que a arma precise de um curto período para recarregar!

## 🚀 Instalação e Execução

Para rodar o jogo em sua máquina, siga os passos abaixo.

### 1. Pré-requisitos

* **Python 3:** Certifique-se de que você tem o Python 3 instalado. Você pode baixá-lo em [python.org](https://www.python.org/).
* **Pygame:** Você precisará da biblioteca Pygame. Instale-a usando pip:
    ```bash
    pip install pygame
    ```

### 2. Baixe o Projeto

Clone ou baixe este repositório para a sua máquina.

```bash
git clone [https://github.com/seu-usuario/senhor-das-trevas.git](https://github.com/seu-usuario/senhor-das-trevas.git)
cd senhor-das-trevas
```

### 3. Estrutura de Arquivos

O jogo espera que os arquivos de imagem e som estejam organizados em pastas específicas. Certifique-se de que sua estrutura de pastas seja a seguinte:

```
senhor-das-trevas/
├── main.py             # Seu arquivo de código do jogo
├── imagens/
│   ├── fundo.png
│   ├── tanque.png
│   ├── missil.png
│   ├── missil_alien.png
│   ├── alien.png
│   ├── bomba.png
│   └── explosao.png
└── sounds/
    ├── explosion.mp3
    ├── missil_tank.mp3
    ├── game_over.mp3
    └── fundo.mp3
```

### 4. Execute o Jogo

Com tudo configurado, execute o arquivo principal do jogo:

```bash
python main.py
```
*(Renomeie `main.py` para o nome real do seu arquivo, se for diferente).*

## 🛠️ Tecnologias Utilizadas

* **Python:** Linguagem principal do projeto.
* **Pygame:** Biblioteca para desenvolvimento de jogos 2D.

---
*Desenvolvido por Hebert Pereira.*
