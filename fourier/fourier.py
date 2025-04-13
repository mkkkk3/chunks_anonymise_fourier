import numpy as np
import cv2
import matplotlib.pyplot as plt

def perform_fft_and_display(image_path, show_reconstructed=True):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Nie można wczytać obrazu: {image_path}")
        return

    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)

    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
    phase_spectrum = np.angle(fshift)

    if show_reconstructed:
        complex_reconstructed = np.abs(fshift) * np.exp(1j * phase_spectrum)
        f_ishift = np.fft.ifftshift(complex_reconstructed)
        img_reconstructed = np.fft.ifft2(f_ishift)
        img_reconstructed = np.abs(img_reconstructed)

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title(f'Oryginalny obraz: {image_path}')
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
        print("1. Pokaz odwrocona transformacja fouriera")
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
