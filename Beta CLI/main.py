from tracking import *


def calculaDeslocamento(lista_centro_M, lista_centro_N):

	#print("vetor maximo de deslocamento: ", max(lista_deslocamento_vertical))

	diferenca = max(lista_deslocamento_vertical) - lista_deslocamento_vertical[1]

	#print("primeiro vetor de deslocamento vertical: ", lista_deslocamento_vertical[0])

	#print("Diferenca entre a posicao inicial e a posicao maxima atingida: ", diferenca)

	deslocamento = (diferenca * 10)/ meansure(lista_centro_M, lista_centro_N)


	#print("lista de deslocamento vertical: ", lista_deslocamento_vertical)

	return print("Distancia(salto): ", round(deslocamento, 2),"cm")


if __name__ == "__main__":

	opt_calib = eval(input(" ##### Menu ##### \n\n 1 - Calibrar \n 2 - Usar Foto existente do Calibrador \n \n Opção: "))

	if opt_calib == 1:
		nome = input("Digite o nome da imagem: ")
		abrir = nome+".png"
		image = cv2.imread(abrir)

		convertHSV(image)
		start_Pick_color(image)
		imageThreshould(image)
		contours(image)
		meansure(lista_centro_M, lista_centro_N)

	else:
		if opt_calib == 2:
			print("existente")

	# Ter atenção especial, pois o video ta rodando num framerate lento, e esta igualmente no raspberry
	# por isso quando faço a limiarização no video do raspberry ele fica lento daquele jeito

	# Retirei os arquivos do diretório corrente
	# para roda-lo, basta digitar a pasta e o arquivo, tipo:
	# "imagens/ca" ou "videos/vi" onde "ca" e "vi" são os nomes dos arquivos
	nome = input("Digite o nome da imagem: ")
	abrir = nome+".png"
	image = cv2.imread(abrir)

	convertHSV(image)
	start_Pick_color(image)
	imageThreshould(image)
	contours(image)
	meansure(lista_centro_M, lista_centro_N)

	#funções do tracking passo por aqui em diante

	nomeVideo = input("\n Digite o nome do video: ")
	abrirVideo = nomeVideo+".mp4"

	trackingVideo(abrirVideo)
	calculaDeslocamento(lista_centro_M, lista_centro_N)
