# Café Gourmet — versão 2 (MVC, Flask e SQLite)

## Tecnologias
- Interface: HTML, CSS e JavaScript
- Back-end: Python 3.10+ com Flask
- Banco de dados: SQLite
- Organização: padrão MVC (Model, View e Controller)

## Como executar no Windows
1. Extraia o arquivo ZIP.
2. Abra a pasta `cafe_gourmet_mvc`.
3. Execute `iniciar_windows.bat`.
4. Abra `http://127.0.0.1:5000` no navegador.
5. Para encerrar, pressione Ctrl+C na janela do servidor.

## Acesso administrativo demonstrativo
- Usuário: `admin`
- Senha: `cafe123`

O painel administrativo agora exige login. Para alterar as credenciais antes de uma publicação, configure as variáveis de ambiente `CAFE_ADMIN_USER`, `CAFE_ADMIN_PASSWORD` e `CAFE_SECRET_KEY`. As credenciais padrão são apenas para demonstração local e não devem ser usadas em produção.

## Melhorias desta versão
- Login para proteger as rotas de administração (cadastro, alteração e exclusão de produtos; consulta e atualização de pedidos).
- Confirmação visual após a finalização, com número do pedido.
- Consulta do andamento do pedido pelo número e telefone cadastrado.
- Carrinho e resumo de valores reorganizados para telas menores.
- Resumo dos itens, subtotal, taxa de entrega e total antes da confirmação.
- Campo para cadastrar um link de imagem para cada produto; quando não houver imagem, o sistema exibe o emoji cadastrado.
- Campo de busca na administração para localizar pedidos por número, nome ou status.
- Migração automática da coluna `image_url` em bancos criados pela versão anterior, preservando produtos e pedidos existentes.

## Estrutura MVC
- `models/`: acesso ao banco e regras de dados dos produtos e pedidos.
- `templates/`: interface HTML.
- `controllers/`: rotas e controle de acesso.
- `static/`: arquivos CSS e JavaScript.
- `app.py`: inicialização do Flask.

## Banco de dados
O arquivo `cafe_gourmet.db` é criado automaticamente ao iniciar o sistema. Ele contém as tabelas `products`, `orders` e `order_items`. Se for usada uma base da versão anterior, a coluna `image_url` será adicionada sem apagar os registros existentes.

## Limitações que permanecem
- O login é simples e destinado à demonstração acadêmica local; antes de uso real, é necessário reforçar a segurança, trocar as credenciais, configurar uma chave secreta própria e usar HTTPS.
- A consulta do pedido exige número e telefone, mas não envia notificações automáticas.
- Não há pagamento on-line, integração com entregadores, controle de estoque ou cadastro de contas de clientes.
- O servidor continua configurado para execução local. Para acesso público, será necessário hospedar a aplicação e ajustar a configuração de segurança.
- As imagens são adicionadas por endereço público informado no cadastro do produto; não há upload de arquivos.

Descrever no relatório apenas funcionalidades efetivamente testadas.
