import requests as req
nomeArquivoCSV = input('Digite o nome do arquivo a ser usado como referência: ')
ondeSalvar = input('Digite onde salvar o arquivo: ')
arquivoCSV = open(nomeArquivoCSV, 'r')
errosNum = 0
for index, linha in enumerate(arquivoCSV):
    try:
        url, titulo = linha.split(',', 1)
        ext = url.rsplit('.', 1)[-1]
        foto = req.get(url, allow_redirects=True)  # possível incluir JWT entre outros headers
        tituloTratado = titulo.replace('\n', '').replace('"', '').replace(':', '').replace('/', '-').replace('\\', '').replace('*', '').replace('>', '').replace('<', '') + str(index)
        open(ondeSalvar+tituloTratado+'.'+ext, 'wb').write(foto.content)
    except Exception as e:
        errosNum += 1
        print(e)
        continue
    finally:
        print(index)

arquivoCSV.close()
print('Número de Erros: ', errosNum)