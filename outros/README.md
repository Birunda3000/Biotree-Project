# Arvore
## Link esboço da base: https://lucid.app/lucidchart/c6febd3b-8bac-4e21-9aa1-630191df306d/edit?viewport_loc=-168%2C220%2C2685%2C1147%2C0_0&invitationId=inv_ddbc1622-f443-4c10-8a3c-e38073359c8c
Reunir material util para o projeto e decisões de implementação
## Ferramentas
* Javascript
  * Node js
    * express
    * sequelize
    * MVC no node
* My SQL
* HTML e CSS?
## Referencias
* 
## Biologica
* todo taxon descende de outro de mesmo nivel (toda ordem descende de outra ordem)?
* toda especie tem subespecie?
* a partir de toda divisão todos os descendentes tem um nome especifico (morpha, io...)?
* tags para cada taxon (faria sentido definir um reino como carnivoro ou uma especie ou um genero como vertebrado?)
* Ancestrais desconhecidos (por exemplo ancestral comum entre eukaria e archaea)
* pode existir um taxon maior sem taxon menores (genero sem especie)?, (especie sem sub-especie)
* pode existir por um tempo sem (homo surgiu em -1M mais a primeira especie homo conhecida é de 0.8M)
## Implementação
* Usar herança entre taxons inferiores?
* cria um vertice para taxon/ano (cada texon em cada ano vai gerar um vertice, e teremos grafos sobrepostos)?
* Adicionar nome cientifico, nome em portugues e em ingles não latinizado
* Como lidar com estimativas (de 100 a 200 mil anos atras)
* pode-se ter varios antepassados
* antepassado pode ser vazio?, se não como adicionar o primeiro
* buracos no registro
* linguas (so ingles, ingles e portugues?, um espaço para cada, obrigatorio preencher um ou outro)
