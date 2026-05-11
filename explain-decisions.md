## Decisões iniciais (Stack):

- **Python**: Vou utilizar python para a construção de todo o pipeline, isso por que é a linguagem onde eu estou mais confortavél de utilizar, poderia utilizar Golang para realizar esse desafio e pensando em escalabilidade ele poderia ser um bom caminho devido a sua forma de trabalhar com concorrência, porem tendo em vista a volumetria presente no desafio o Python se adequa muito bem.

- **Pytest**: Vou estar usando o pytest para aplicar o modelo de TDD do fluxo, ou seja, a minha estrutura deve estar com testes contemplando a logica que irei executar.

- **Pydantic**: Estou utilizando essa lib para facilitar nas validações dos tipos de dados que o fluxo consome, com isso vou ter uma melhor qualidade dos registros no fluxo do pipeline, por que estou validando e garantindo que o tipo daquele dado será o que eu defini em seu schema.

## Possibilidades:

- Esse desafio poderia utilizar o pandas para realizar validações, leitura dos CSV, transformação e escrita dos dados, porem apliquei Python puro por se tratar de um desafio, então em um desenvolvimento eu optaria por usar o pandas nessa construção tendo em vista a facilidade de sua utilização para volumetris pequenas.

## Decisões:

- Eu tentei deixar o mais generico possivel, sei que o desafio se baseia somente nos arquivos customers e orders, porem imaginei a possibilidade de utilização do fluxo de forma mais generica possivel, fazendo com que seja necessario ajustar o schema de um novo fluxo e ajustar o pipeline.py para que um novo fluxo seja criado, ainda teria que ajustar o pipeline.py para que ele se torne ainda mais generico, passando somente uma config incial (podendo ser uma estrutura json) tendo em vista que no momento ele precisa que seja criado uma instancia para cada novo pipeline que queira ser implementado e o seu flow.
