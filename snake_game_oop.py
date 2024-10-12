import pygame
import random


class snake_game:
    # Constructor oop
    def __init__(self):
        pygame.init()

        # Initialize colors
        self.white = (255, 255, 255)
        self.yellow = (255, 255, 102)
        self.black = (0, 0, 0)
        self.red = (213, 50, 80)
        self.green = (0, 255, 0)
        self.blue = (50, 153, 213)

        # Tentukan ukuran layar
        self.dis_width = 600
        self.dis_height = 400

        # Buat layar dengan ukuran yang telah ditentukan
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))

        # Beri judul pada layar
        pygame.display.set_caption("Snake Game")

        # Buat objek clock
        self.clock = pygame.time.Clock()

        # Tentukan ukuran blok snake dan kecepatan snake
        self.snake_block = 10
        self.snake_speed = 5

        # Tentukan font style yang akan digunakan
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 25)

        self.game_over = False
        self.game_close = False
        # x1 dan y1 adalah koordinat awal kepala ular.
        self.x1 = self.dis_width / 2
        self.y1 = self.dis_height / 2

        # variabel yang digunakan untuk mengubah posisi kepala ular.
        self.x1_change = 0
        self.y1_change = 0

        # daftar kosong yang akan digunakan untuk menyimpan koordinat tubuh ular.
        self.snake_List = []

        # panjang awal ular.
        self.Length_of_snake = 1

        # koordinat makanan yang harus dimakan oleh ular untuk tumbuh.
        self.foodx = (
            round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
        )
        self.foody = (
            round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
        )

    # Definisikan fungsi untuk menampilkan skor
    def Your_score(self, score):
        value = self.score_font.render("Your Score: " + str(score), True, self.yellow)
        self.dis.blit(value, [0, 0])

    # Definisikan fungsi untuk menggambar snake
    def our_snake(self, snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(
                self.dis, self.black, [x[0], x[1], snake_block, snake_block]
            )

    # Definisikan fungsi untuk menampilkan pesan
    def message(self, msg, color):
        mesg = self.font_style.render(msg, True, color)
        self.dis.blit(mesg, [self.dis_width / 6, self.dis_height / 3])

    def gameLoop(self):
        # Looping untuk tidak game over
        while not self.game_over:
            while self.game_close:
                self.dis.fill(self.blue)
                # Menampilkan pesan untuk kalah dalam permainan
                self.message("You Lost! Press C-Play Again or Q-Quit", self.red)
                # Menampilkan skor
                self.Your_score(self.Length_of_snake - 1)
                # Update tampilan
                pygame.display.update()

                # Memeriksa event
                for event in pygame.event.get():
                    # Jika pengguna menekan Q, permainan berakhir
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.game_over = True
                            self.game_close = False
                        # Jika pengguna menekan C, permainan dimulai ulang
                        if event.key == pygame.K_c:
                            self.__init__()
                            self.gameLoop()

            # Memeriksa event dengan looping
            for event in pygame.event.get():
                # Jika pengguna menutup jendela, permainan berakhir
                if event.type == pygame.QUIT:
                    self.game_over = True
                # Jika pengguna menekan tombol di keyboard,
                # ular bergerak sesuai dengan arah yang ditentukan
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.x1_change = -self.snake_block
                        self.y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        self.x1_change = self.snake_block
                        self.y1_change = 0
                    elif event.key == pygame.K_UP:
                        self.y1_change = -self.snake_block
                        self.x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        self.y1_change = self.snake_block
                        self.x1_change = 0

            # Memeriksa apakah ular menabrak dinding
            if (
                self.x1 >= self.dis_width
                or self.x1 < 0
                or self.y1 >= self.dis_height
                or self.y1 < 0
            ):
                self.game_close = True

            # Menggerakkan ular
            self.x1 += self.x1_change
            self.y1 += self.y1_change
            # Mengisi layar dengan warna biru
            self.dis.fill(self.blue)
            # Menggambar makanan
            pygame.draw.rect(
                self.dis,
                self.green,
                [self.foodx, self.foody, self.snake_block, self.snake_block],
            )
            # Menambahkan kepala ular ke dalam daftar ular
            snake_Head = [self.x1, self.y1]
            self.snake_List.append(snake_Head)
            # Jika panjang ular lebih besar dari panjang yang ditentukan, hapus ekor ular
            if len(self.snake_List) > self.Length_of_snake:
                del self.snake_List[0]

            # Memeriksa apakah ular menabrak dirinya sendiri
            for x in self.snake_List[:-1]:
                if x == snake_Head:
                    self.game_close = True

            # Menggambar ular
            self.our_snake(self.snake_block, self.snake_List)
            self.Your_score(self.Length_of_snake - 1)

            # Update tampilan
            pygame.display.update()

            # Jika ular memakan makanan, hasilkan makanan baru dan tambahkan panjang ular
            if self.x1 == self.foodx and self.y1 == self.foody:
                self.foodx = (
                    round(random.randrange(0, self.dis_width - self.snake_block) / 10.0)
                    * 10.0
                )
                self.foody = (
                    round(
                        random.randrange(0, self.dis_height - self.snake_block) / 10.0
                    )
                    * 10.0
                )
                self.Length_of_snake += 1

            # Menentukan kecepatan permainan
            self.clock.tick(self.snake_speed)

        pygame.quit()
        quit()


# jika file ini diimpor sebagai modul oleh file lain,
# blok kode file ini tidak akan dieksekusi.
if __name__ == "__main__":
    game = snake_game()
    game.gameLoop()
