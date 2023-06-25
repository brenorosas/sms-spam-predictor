# sms-spam-predictor

Esse projeto tem como objetivo classificar mensagens SMS como spam (spam) ou não spam (ham), usando o algorítmo Naive Bayes.

## Dataset

Foi utilizado o Sms Spam Collection
https://archive.ics.uci.edu/dataset/228/sms+spam+collection

Esse dataset basicamente fornece textos SMS e diz se é spam ou não.

formato de cada linha:
spam/ham sms_text

## Pré processamento

O código foi pensado para pegar um dataset em que é fornecido apenas o texto do sms e dizendo se é spam ou não.
Para utilizar o dataset como treinamento no naive bayers precisamos pré processar esses textos de forma em que tenhamos um formato de tabelas
em que cada coluna é um atributo e cada linha seja referente a um SMS, sendo a última coluna a classe do mesmo.

Foi pensado os seguintes atributos:

#Comprimento do texto: Calcule o número de caracteres no SMS. Geralmente, mensagens de spam tendem a ser mais longas do que mensagens normais.

#Número de palavras: Conte o número de palavras presentes no SMS. Isso pode fornecer informações sobre a complexidade e conteúdo da mensagem.

#Frequência de palavras-chave: Crie um conjunto de palavras-chave relevantes, como "oferta", "grátis", "ganhe dinheiro" e conte quantas vezes essas palavras-chave aparecem no texto do SMS. Mensagens de spam geralmente contêm essas palavras-chave com mais frequência.

#Uso de letras maiúsculas: Determine a proporção de letras maiúsculas em relação ao total de letras no texto do SMS. Mensagens de spam tendem a usar letras maiúsculas excessivas para chamar a atenção.

#Presença de números de telefone: Verifique se o SMS contém números de telefone. Muitas mensagens de spam incluem números de telefone para contato ou para direcionar os usuários a ligarem para determinados serviços.

#Uso de símbolos ou caracteres especiais: Analise a quantidade de símbolos, caracteres especiais ou emojis presentes no texto do SMS. Mensagens de spam costumam usar esses elementos para atrair a atenção do destinatário.

#Análise de sentimentos: Realize a análise de sentimentos no texto do SMS para identificar se ele possui uma carga emocional positiva, negativa ou neutra. Isso pode ajudar a identificar padrões de linguagem comuns em mensagens de spam.

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
python3 main.py <dataset
```

Será necessário um arquivo chamado dataset na raiz do repositório, é esperado que esse arquivo esteja no formato em que cada linha siga o padrão:

classe texto_sms

Exemplos:
```
ham	So when do you wanna gym harri
ham	Quite late lar... Ard 12 anyway i wun b drivin...
spam	To review and KEEP the fantastic Nokia N-Gage game deck with Club Nokia, go 2 www.cnupdates.com/newsletter. unsubscribe from alerts reply with the word OUT
```
