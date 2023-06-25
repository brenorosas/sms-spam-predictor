# sms-spam-predictor

Esse projeto tem como objetivo classificar mensagens SMS como spam (spam) ou não spam (ham), usando o algorítmo Naive Bayes.

## Dataset

Foi utilizado o Sms Spam Collection
https://archive.ics.uci.edu/dataset/228/sms+spam+collection

Esse dataset basicamente fornece textos SMS e diz se é spam ou não.

formato de cada linha:
spam/ham sms_text

## Instalando as dependências

Para instalar as dependências será necessário python3 e pip3 instalado em sua máquina.

É recomendado também que instale em um ambiente virtual que é facilmente criado com python3.

Na raiz do repositório rode os seguintes comandos em sequência:
```
python3 -m venv myenv
source myenv/bin/activate
pip3 install -r requirements.txt
```

Caso não queira rodar em um ambiente virtual use apenas o último comando.

## Executando o código

Para executar o código basta utilizar o comando:

```
python3 code.py <dataset
```

Será necessário um arquivo chamado dataset na raiz do repositório, é esperado que esse arquivo esteja no formato em que cada linha siga o padrão:

classe texto_sms

Exemplos:
```
ham	So when do you wanna gym harri
ham	Quite late lar... Ard 12 anyway i wun b drivin...
spam	To review and KEEP the fantastic Nokia N-Gage game deck with Club Nokia, go 2 www.cnupdates.com/newsletter. unsubscribe from alerts reply with the word OUT
```
