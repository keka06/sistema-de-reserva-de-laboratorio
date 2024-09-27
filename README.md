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

Aplicativo desenvolvido em Python e banco de dados em MySQL, utilizando o painel do phpMyAdmin
