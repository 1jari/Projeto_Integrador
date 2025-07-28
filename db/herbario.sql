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
("Camomila","Matricaria chamomilla","Planta com flores pequenas, usada para chas calmantes.","Calmante, digestiva, anti-inflamatoria.","Tratamento de insonia, ansiedade, colicas e irritacoes leves."),
("Hortela","Mentha piperita","Erva aromatica comum em chas e remedios naturais.","Estimulante digestivo, alivia nauseas e tem efeito refrescante.","Usada em chas, xaropes e aromaterapia."),
("Erva-cidreira","Melissa officinalis","Planta de folhas aromaticas usada para relaxamento.","Calmante, ansiolitica, antiespasmodica.","Combate insonia, ansiedade, tensao e colicas."),
("Boldo","Peumus boldus","Usado tradicionalmente para problemas digestivos e hepaticos.","Estimulante hepatico, digestivo e levemente laxativo.","Utilizado em infusoes para ma digestao e problemas do figado."),
("Arnica","Arnica montana","Usada externamente para contusoes e dores musculares.","Anti-inflamatoria, cicatrizante, analgesica.","Aplicacao topica em hematomas, torcoes e dores musculares."),
("Babosa (Aloe Vera)","Aloe vera","Planta suculenta com gel medicinal nas folhas.","Cicatrizante, hidratante, anti-inflamatoria.","Tratamento de queimaduras, feridas e uso cosmetico."),
("Guaco","Mikania glomerata","Planta trepadeira com folhas aromaticas.","Expectorante, broncodilatadora.","Utilizado no alivio da tosse e doencas respiratorias."),
("Gengibre","Zingiber officinale","Rizoma muito usado como tempero e remedio natural.","Antioxidante, anti-inflamatorio, digestivo.","Combate nauseas, resfriados e problemas gastrointestinais."),
("Urtiga","Urtica dioica","Planta com folhas urticantes, rica em nutrientes.","Diuretica, anti-inflamatoria.","Usada no tratamento de artrite, anemia e problemas urinarios.");

select * from plantas


