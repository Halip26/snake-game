import pygame
import random

# Inisialisasi pygame
pygame.init()

# Definisikan warna yang akan digunakan
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Tentukan ukuran layar
dis_width = 600
dis_height = 400

# Buat layar dengan ukuran yang telah ditentukan
dis = pygame.display.set_mode((dis_width, dis_height))

# Beri judul pada layar
pygame.display.set_caption("Snake Game")

# Buat objek clock
clock = pygame.time.Clock()

# Tentukan ukuran blok snake dan kecepatan snake
snake_block = 10
snake_speed = 5

# Tentukan font style yang akan digunakan
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


# Definisikan fungsi untuk menampilkan skor
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


# Definisikan fungsi untuk menggambar snake
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


# Definisikan fungsi untuk menampilkan pesan
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


# Fungsi utama game
def gameLoop():
    # memeriksa apakah game sudah berakhir atau belum.
    game_over = False
    game_close = False

    # x1 dan y1 adalah koordinat awal kepala ular.
    x1 = dis_width / 2
    y1 = dis_height / 2

    # variabel yang digunakan untuk mengubah posisi kepala ular.
    x1_change = 0
    y1_change = 0

    # daftar kosong yang akan digunakan untuk menyimpan koordinat tubuh ular.
    snake_List = []

    # panjang awal ular.
    Length_of_snake = 1

    # koordinat makanan yang harus dimakan oleh ular untuk tumbuh.
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    # Looping untuk tidak game over
    while not game_over:
        # Looping untuk game close
        while game_close == True:
            # Mengisi layar dengan warna biru
            dis.fill(blue)
            # Menampilkan pesan untuk kalah dalam permainan
            message("You Lost! Press C-Play Again or Q-Quit", red)
            # Menampilkan skor
            Your_score(Length_of_snake - 1)
            # Update tampilan
            pygame.display.update()

            # Memeriksa event
            for event in pygame.event.get():
                # Jika pengguna menekan Q, permainan berakhir
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    # Jika pengguna menekan C, permainan dimulai ulang
                    if event.key == pygame.K_c:
                        gameLoop()

        # Memeriksa event dengan looping
        for event in pygame.event.get():
            # Jika pengguna menutup jendela, permainan berakhir
            if event.type == pygame.QUIT:
                game_over = True
            # Jika pengguna menekan tombol di keyboard, ular bergerak sesuai dengan arah yang ditentukan
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Memeriksa apakah ular menabrak dinding
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        # Menggerakkan ular
        x1 += x1_change
        y1 += y1_change
        # Mengisi layar dengan warna biru
        dis.fill(blue)
        # Menggambar makanan
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        # Menambahkan kepala ular ke dalam daftar ular
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        # Jika panjang ular lebih besar dari panjang yang ditentukan, hapus ekor ular
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Memeriksa apakah ular menabrak dirinya sendiri
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
        # Menggambar ular
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
        # Update tampilan
        pygame.display.update()

        # Jika ular memakan makanan, hasilkan makanan baru dan tambahkan panjang ular
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        # Menentukan kecepatan permainan
        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
