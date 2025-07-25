create table plantas(
    id              int             primary key auto_increment,
    nome            varchar(100)    not  NULL,
    nome_cientifico varchar(150),
    descricao       text,
    caracteristicas text,
    uso             text,
    imagem_url      varchar(255) 
);

insert into plantas (nome, nome_cientifico, descricao, caracteristicas, uso) 
values
("Alecrim", "Rosmarinus officinalis", "Arbusto aromatico muito usado na culinaria e fitoterapia.", "Estimula a memoria, tem acao antioxidante e anti-inflamatoria.", "Melhora a concentracao, usado em oleos essenciais e chas."),
("Camomila","Matricaria chamomilla","Planta com flores pequenas, usada para chás calmantes.","Calmante, digestiva, anti-inflamatória.","Tratamento de insônia, ansiedade, cólicas e irritações leves."),
("Hortelã","Mentha piperita","Erva aromática comum em chás e remédios naturais.","Estimulante digestivo, alivia náuseas e tem efeito refrescante.","Usada em chás, xaropes e aromaterapia."),
("Erva-cidreira","Melissa officinalis","Planta de folhas aromáticas usada para relaxamento.","Calmante, ansiolítica, antiespasmódica.","Combate insônia, ansiedade, tensão e cólicas."),
("Boldo","Peumus boldus","Usado tradicionalmente para problemas digestivos e hepáticos.","Estimulante hepático, digestivo e levemente laxativo.","Utilizado em infusões para má digestão e problemas do fígado."),
("Arnica","Arnica montana","Usada externamente para contusões e dores musculares.","Anti-inflamatória, cicatrizante, analgésica.","Aplicação tópica em hematomas, torções e dores musculares."),
("Babosa (Aloe Vera)","Aloe vera","Planta suculenta com gel medicinal nas folhas.","Cicatrizante, hidratante, anti-inflamatória.","Tratamento de queimaduras, feridas e uso cosmético."),
("Guaco","Mikania glomerata","Planta trepadeira com folhas aromáticas.","Expectorante, broncodilatadora.","Utilizado no alívio da tosse e doenças respiratórias."),
("Gengibre","Zingiber officinale","Rizoma muito usado como tempero e remédio natural.","Antioxidante, anti-inflamatório, digestivo.","Combate náuseas, resfriados e problemas gastrointestinais."),
("Urtiga","Urtica dioica","Planta com folhas urticantes, rica em nutrientes.","Diurética, anti-inflamatória.","Usada no tratamento de artrite, anemia e problemas urinários.");

select * from plantas


