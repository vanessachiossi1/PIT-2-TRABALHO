# Café Gourmet — versão MVC com Flask e SQLite

## Tecnologias
- Interface: HTML, CSS e JavaScript
- Back-end: Python 3.10+ com Flask
- Banco de dados: SQLite
- Organização: padrão MVC (Model, View e Controller)

## Como executar no Windows
1. Extraia o ZIP.
2. Abra a pasta do projeto.
3. Execute `iniciar_windows.bat`.
4. Abra `http://127.0.0.1:5000` no navegador.
5. Para encerrar, pressione Ctrl+C na janela do servidor.

## Estrutura MVC
- `models/`: acesso ao banco e regras de dados dos produtos e pedidos.
- `views/`: telas HTML armazenadas em `templates/`.
- `controllers/`: rotas que recebem as requisições e conectam a interface aos Models.
- `static/`: arquivos CSS e JavaScript do front-end.
- `app.py`: inicialização do Flask e registro das rotas.

## Banco de dados
O arquivo `cafe_gourmet.db` é criado automaticamente ao iniciar o sistema. Ele contém as tabelas `products`, `orders` e `order_items`.

## Funcionalidades implementadas
- Cardápio com busca e filtro por categoria.
- Carrinho de compras no navegador durante a sessão.
- Registro persistente dos pedidos no SQLite.
- Cadastro, ativação/desativação e exclusão de produtos.
- Consulta de pedidos e atualização de status.

## Limitações conhecidas
- O painel administrativo é demonstrativo e ainda não possui autenticação.
- Não há pagamento on-line, integração com entregas ou notificações.
- O servidor é local; para acesso público, será necessário hospedar a aplicação.
- O carrinho é mantido temporariamente no navegador; pedidos confirmados são gravados no SQLite.

Descrever no relatório apenas funcionalidades efetivamente testadas.
