import numpy as np
import cv2
# wczytywanie obrazow
import matplotlib.pyplot as plt
# plotowanie

def perform_fft_and_display(image_path, show_reconstructed=True):
    # show_reconstructed - jesli ma pokazywac rekonstrukcje (w sensie odwrotna transformate fouriera)
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # imread - wczytywanie obrazu - jak? - sciezka, jak wczytac (czarno-bialy)
    if img is None:
        # gdy nie ma obrazu o danej sciezce
        print(f"Nie można wczytać obrazu: {image_path}")
        # zakoncz caly program
        return
      
    
    f = np.fft.fft2(img)
    # np.fft - to tak jakby folder w numpy, samo np.fft to nie funkcja tylko modul w numpy
    # fft2 - fast fourier transform 2D (dyskretna), f bedzie macierza zespolona CZESTOTLIWOSCI (wielkosci rozdzielczosci obrazu)
    # kazdy element tej macierzy to bedzie po prostu a + bi
    print(f)
    # wynik printa (np dla rotate1.png) to bedzie
#     [[ 380205.            +0.j         -361878.81301658-35641.95213923j
#    310403.70103366+61743.13501601j ... -235441.98242902+71420.54455178j
#    310403.70103366-61743.13501601j -361878.81301658+35641.95213923j]
#  [-208548.72093608-52238.73515906j  193599.43475263+69270.98539775j
#   -161778.28157548-76515.42868943j ...  138956.72913819 -6826.50635683j
#   -178744.83003219 -8781.17041206j  203393.57474738+30170.58676911j]
#  [ -32425.13150648-17331.59387488j   29237.48046997+19535.85987662j
#    -23657.69488948-19415.36843569j ...   23334.96170461 +4641.61247538j
#    -29286.79992839 -8884.05363175j   32486.94767522+13456.53432718j]
#  ...
#  [  46929.18905743-42534.13764657j  -48654.48621195+36084.62627768j
#     45220.82816753-27104.32132561j ...  -21070.97495485+35154.79787555j
#     31406.22287038-42346.38945289j  -40679.84254192+44883.28968462j]
#  [ -32425.13150648+17331.59387488j   32486.94767522-13456.53432718j
#    -29286.79992839 +8884.05363175j ...   16823.5698371 -16823.5698371j
#    -23657.69488948+19415.36843569j   29237.48046997-19535.85987662j]
#  [-208548.72093608+52238.73515906j  203393.57474738-30170.58676911j
#   -178744.83003219 +8781.17041206j ...  119330.90143073-71524.18979305j
#   -161778.28157548+76515.42868943j  193599.43475263-69270.98539775j]]
    # fshift = np.fft.fftshift(f)
    fshift = np.fft.fftshift(f)
    # przesuniecie danych CZESTOTLIWOSCI po transformacie fouriera, aby scrodek macierzy to bylo (0,0), a nie rogi
    # np.
    # [ 0  1  2  3 ]
    # [ 4  5  6  7 ]
    # [ 8  9 10 11 ]
    # [12 13 14 15 ]
    # 
    # po fftshift(f)
    # 
    # [10 11  8  9 ]
    # [14 15 12 13 ]
    # [ 2  3  0  1 ]
    # [ 6  7  4  5 ]
    # 
    # najlatwiej to mozna zobaczyc zamieniajac
    # fshift = np.fft.fftshift(f)
    # na:
    # fshift = f
    # Odpalic program -> wybrac opcje 1 -> wybrac vertical -> zobaczyc roznice

    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
    # np.abs(fshift) - dla kazdej liczby zespolonej liczy modul |z| = sqrt(a^2 + b^2)  - to jest sila danej czestotliwosc
    # + 1 zeby nie było log(0) - dzieki temu jest log(0 + 1) = log(1) = 0
    # np.log() - zmieni zakres z wykladniczego na logarytmiczny, bo wartosci moga byc bardzo rozstrzelone - dzieki temu niskie i wysokie czestotliwosci sa widoczne na wykresach
    # 20 * ln() to odpowiednik skali decybelowej
    # dB = 20 * log10(amplituda)
    # w skrocie przeliczanie amplitudy na decybele (widmo aplitudy bedzie czytelne)
    phase_spectrum = np.angle(fshift)
    # oblicza faze dla kazdego elementu macierzy fshift
    # kazda liczba zespolona moze byc przedstawiona jako
    # z = r * e^(jθ), gdzie:
    # r = |z| = sqrt(a^2 + b^2) - modul (magnitude)
    # θ = arg(z) - faza
    # 
    # 
    # 
    # np.angle(...)
    # np.angle(a + bj) = atan2(b, a)
    # oblicza kąt między wektorem z a osią rzeczywistą (oś x)
    # zwraca warosc z zakresu (-pi, pi], czyli od -180 do 180 stopni (w radianach)
    # Przyklad:
    # z = 1 + 1j
    # np.angle(z) ≈ 0.785 rad = 45°
    # 
    # 
    # w skrocie phase_spectrum to macierz faz (a faza informuje gdzie dana czestotliowsc wystepuje na obrazie)
    
    
    
    # magnitude - intensywnosc - ile danej czestotliwosci wystepuje
    # phase - gdzie wystepuje czestotliwosc - przesuniecie, lokalizacja

    if show_reconstructed:
        complex_reconstructed = np.abs(fshift) * np.exp(1j * phase_spectrum)
        # kazdy element widma to liczba zespolona
        # z = a + bi
        # mozna to tez zapisac jako (postac trygonometryczna)
        # z = r * e^(jθ), gdzie
        # r = |z| = sqrt(a^2 + b^2) - modul (magnitude)
        # θ = arg(z) - faza
        # 
        # np.abs(fshift) - obliczenie modulu
        # np.abs(3 + 4j) = sqrt(3² + 4²) = 5
        # 
        # np.exp(1j * phase_spectrum)
        # tworzy liczby zespolone w postaci wykladniczej
        # e^(jθ) = cos(θ) + isin(θ)
        # phase_spectrum to macierz faz (θ)
        # 1j * phase_spectrum - zmienia je w zespolone katy
        # np.exp(...) - tworzy jednostkowy wektor zespolony o danym kacie
        f_ishift = np.fft.ifftshift(complex_reconstructed)
        # przesyniecie widma z powrotem w rog
        img_reconstructed = np.fft.ifft2(f_ishift)
        # odwrocona transformata fouriera
        # zwraca macierz liczb zespoloncyh
        img_reconstructed = np.abs(img_reconstructed)
        # >>> z = 123.45 + 0.000000000001j
        # >>> np.abs(z) ≈ 123.45
        # czesc urojona jest bardzo, bardzo mala i trzeba jej sie pozbyc


    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title(f'Oryginalny obraz: {image_path}')
    # wylaczenie osie wspolrzednych
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.imshow(magnitude_spectrum, cmap='gray')
    plt.title('Magnitude spectrum')
    plt.axis('off')

    plt.subplot(2, 2, 3)
    plt.imshow(phase_spectrum, cmap='gray')
    plt.title('Phase spectrum')
    plt.axis('off')

    if show_reconstructed:
        plt.subplot(2, 2, 4)
        plt.imshow(img_reconstructed, cmap='gray')
        plt.title('Odtworzony obraz')
        plt.axis('off')

    # wybiera najlepsze rozmieszczenie
    plt.tight_layout()
    plt.show()

def compare_two_images(img1_path, img2_path):
    fig, axes = plt.subplots(2, 3, figsize=(9, 5))

    for i, image_path in enumerate([img1_path, img2_path]):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Nie można wczytać obrazu: {image_path}")
            return

        f = np.fft.fft2(img)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
        phase_spectrum = np.angle(fshift)

        axes[i, 0].imshow(img, cmap='gray')
        axes[i, 0].set_title(f'Oryginalny obraz: {image_path}')
        axes[i, 0].axis('off')

        axes[i, 1].imshow(magnitude_spectrum, cmap='gray')
        axes[i, 1].set_title('Magnitude spectrum')
        axes[i, 1].axis('off')

        axes[i, 2].imshow(phase_spectrum, cmap='gray')
        axes[i, 2].set_title('Phase spectrum')
        axes[i, 2].axis('off')

    plt.tight_layout()
    plt.show()

def menu():
    while True:
        print("\n=== MENU ===")
        print("1. Pokaz odwrocona transformate fouriera")
        print("2. Pokaz wplyw przesuniecia na wykresy")
        print("3. Pokaz wplyw obrotu na wykresy")
        print("4. Pokaz wykresy dla lini pionowych")
        print("5. Pokaz wykresy dla lini poziomych")
        print("6. Zakoncz program")

        choice = input("Wybierz opcję: ")

        if choice == '1':
            filename = input("Podaj nazwę pliku (np. indexed.png): ")
            perform_fft_and_display(filename)
        elif choice == '2':
            compare_two_images("dot1.png", "dot2.png")
        elif choice == '3':
            compare_two_images("rotate1.png", "rotate2.png")
        elif choice == '4':
            perform_fft_and_display("vertical.png")
        elif choice == '5':
            perform_fft_and_display("horizontal.png")
        elif choice == '6':
            print("Program zakończony.")
            break
        else:
            print("Niepoprawna opcja. Wybierz 1-6.")

if __name__ == "__main__":
    menu()
