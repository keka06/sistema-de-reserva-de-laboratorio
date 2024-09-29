# sistema-de-reserva-de-laboratorio
- aplicativo desenvolvido por estudantes como parte de um projeto acadêmico, afim de melhorar e aplicar seus conhecimentos de desenvolvimento de software

sistema que realiza reservas entre 2 laboratórios, na qual você pode escolher o horário demarcado entre 19:00 ás 21:30

Este é um aplicativo de gerenciamento de reservas de laboratórios, permitindo que usuários se cadastrem, façam login e gerenciem suas reservas em um banco de dados local. O sistema oferece funcionalidade para escolher entre dois laboratórios (Laboratório A e Laboratório B) e inclui permissões diferenciadas para usuários e administradores.

Funcionalidades:
- Cadastro de Usuários: Permite que novos usuários se cadastrem como Funcionários ou Administradores.
- Login: Usuários podem fazer login para acessar suas contas.
- Reservas: Usuários podem reservar laboratórios, visualizando suas reservas atuais.
- Visualização e Exclusão de Reservas: Usuários podem visualizar suas reservas e excluí-las quando necessário.

Regras de Agendamento:
- Não é permitido reservar o mesmo laboratório no mesmo dia.
- Um laboratório só pode ser reservado novamente após um intervalo de 15 dias.

Funcionário (Usuário):
- Pode agendar reservas nos laboratórios.
- Tem acesso limitado às suas próprias reservas.

Administrador:
- Pode visualizar todas as reservas feitas por todos os usuários.
- Tem a capacidade de excluir reservas de qualquer usuário.

Instruções para conectar ao banco de dados:

- Tenha o XAMPP instalado na sua máquina e inicialize os serviços 'Apache' e 'MySQL'.
- Abra o painel phpMyAdmin atráves do XAMPP clicando em 'Admin' na fileira do MySQL e crie um banco de dados chamado 'x5'.
- No banco de dados clique na aba 'SQL' e execute o comando abaixo:

CREATE TABLE Usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('admin', 'usuario') NOT NULL,
    usuario_name VARCHAR(50) NOT NULL
);
 
-- Tabela de Laboratórios
CREATE TABLE Laboratorio (
    id_laboratorio INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    localizacao VARCHAR(100) NOT NULL
);
 
-- Tabela de Reservas
CREATE TABLE Reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_laboratorio INT NOT NULL,
    data_reserva DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    status ENUM('confirmada', 'pendente', 'cancelada') NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_laboratorio) REFERENCES Laboratorio(id_laboratorio) ON DELETE CASCADE
);
 
-- Tabela de Disponibilidades
CREATE TABLE Disponibilidades (
    id_disponibilidade INT AUTO_INCREMENT PRIMARY KEY,
    id_laboratorio INT NOT NULL,
    data DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    nome varchar(30) NOT NULL,
    numero_paciente varchar(30) NOT NULL,
    FOREIGN KEY (id_laboratorio) REFERENCES Laboratorio(id_laboratorio) ON DELETE CASCADE
);

- Em seguida clique em 'Executar' e execute outro comando:

INSERT INTO laboratorio (id_laboratorio, nome) VALUES (1, 'Laboratório A'), (2, 'Laboratório B');

- Certifique-se que o XAMPP esteja rodando em segundo plano. O aplicativo está pronto para uso.


Aplicativo desenvolvido em Python e banco de dados em MySQL, utilizando o painel do phpMyAdmin
