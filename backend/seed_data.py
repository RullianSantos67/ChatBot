"""
Execute: python seed_data.py
O servidor Flask deve estar rodando em http://localhost:5000
"""
import requests
import json
import time

DOCUMENTS = [
    # Categoria: Fundamentos de Cibersegurança e Ameaças
    {"id": "doc_001", "text": "Ransomware é um tipo de malware que emprega criptografia forte para sequestrar dados de uma organização, exigindo pagamento (geralmente em criptomoedas) para a liberação da chave de decodificação.", "metadata": {"source": "Relatório de Ameaças Globais", "categoria": "Ameaças Cibernéticas"}},
    {"id": "doc_002", "text": "Ataques de Phishing utilizam engenharia social para enganar usuários e obter credenciais. O Spear Phishing é uma variante altamente direcionada, focada em executivos específicos (Whaling) ou departamentos com acesso a fundos.", "metadata": {"source": "Manual de Conscientização", "categoria": "Ameaças Cibernéticas"}},
    {"id": "doc_003", "text": "Vulnerabilidades Zero-Day referem-se a falhas de segurança em softwares que ainda são desconhecidas pelos fabricantes. Ataques explorando essas falhas não possuem patches de correção disponíveis no momento da invasão.", "metadata": {"source": "Engenharia de Software Seguro", "categoria": "Ameaças Cibernéticas"}},
    {"id": "doc_004", "text": "Ataques DDoS (Distributed Denial of Service) visam sobrecarregar servidores ou redes com tráfego massivo gerado por botnets, tornando serviços web indisponíveis para usuários legítimos.", "metadata": {"source": "Arquitetura de Redes", "categoria": "Ameaças Cibernéticas"}},
    {"id": "doc_005", "text": "Injeção de SQL (SQLi) ocorre quando entradas de usuários não são sanitizadas, permitindo que invasores executem comandos arbitrários no banco de dados, resultando em extração ou destruição de dados sensíveis.", "metadata": {"source": "Desenvolvimento Web Seguro", "categoria": "Ameaças Cibernéticas"}},

    # Categoria: Criptografia e Proteção de Dados
    {"id": "doc_006", "text": "AES (Advanced Encryption Standard) é o padrão ouro para criptografia simétrica. A versão AES-256 é amplamente utilizada para proteger dados em repouso (Data at Rest) em bancos de dados corporativos.", "metadata": {"source": "Padrões Criptográficos", "categoria": "Criptografia"}},
    {"id": "doc_007", "text": "A criptografia assimétrica, como o RSA, utiliza um par de chaves (pública e privada). É fundamental para a troca segura de chaves de sessão e assinaturas digitais em ambientes web.", "metadata": {"source": "Infraestrutura de Chaves Públicas", "categoria": "Criptografia"}},
    {"id": "doc_008", "text": "Funções de Hash (como SHA-256) são processos matemáticos unidirecionais. Elas são usadas para armazenar senhas de forma segura, garantindo que o banco de dados não contenha as senhas em texto claro.", "metadata": {"source": "Autenticação e Identidade", "categoria": "Criptografia"}},
    {"id": "doc_009", "text": "O conceito de 'Salting' envolve adicionar uma string aleatória única a cada senha antes do processo de hashing, protegendo o sistema contra ataques de dicionário e tabelas Rainbow.", "metadata": {"source": "Autenticação e Identidade", "categoria": "Criptografia"}},
    {"id": "doc_010", "text": "O protocolo TLS (Transport Layer Security) é essencial para proteger dados em trânsito (Data in Transit), estabelecendo túneis criptografados entre clientes e servidores para impedir interceptações (Man-in-the-Middle).", "metadata": {"source": "Segurança de Redes", "categoria": "Criptografia"}},

    # Categoria: Segurança em Nuvem e Arquitetura
    {"id": "doc_011", "text": "A arquitetura Zero Trust (Confiança Zero) parte do princípio de que nenhuma entidade, interna ou externa à rede, deve ser confiável por padrão. Requer autenticação e autorização contínuas para cada acesso.", "metadata": {"source": "Arquitetura Corporativa", "categoria": "Segurança em Nuvem"}},
    {"id": "doc_012", "text": "O modelo de Responsabilidade Compartilhada na nuvem estabelece que provedores (AWS, Azure) protegem a infraestrutura (segurança DA nuvem), enquanto o cliente é responsável por seus dados e acessos (segurança NA nuvem).", "metadata": {"source": "Governança Cloud", "categoria": "Segurança em Nuvem"}},
    {"id": "doc_013", "text": "Firewalls de Aplicação Web (WAF) analisam o tráfego HTTP/HTTPS na camada 7 do modelo OSI, filtrando ataques específicos de aplicações web, como Cross-Site Scripting (XSS) e SQL Injection.", "metadata": {"source": "Segurança de Perímetro", "categoria": "Segurança em Nuvem"}},
    {"id": "doc_014", "text": "Sistemas IAM (Identity and Access Management) aplicam o Princípio do Menor Privilégio, garantindo que usuários e serviços tenham acesso estritamente aos recursos necessários para suas funções.", "metadata": {"source": "Gestão de Identidades", "categoria": "Segurança em Nuvem"}},
    {"id": "doc_015", "text": "A autenticação multifator (MFA) adiciona camadas de defesa ao exigir dois ou mais métodos de verificação (algo que você sabe, algo que você tem, algo que você é) para conceder acesso a sistemas críticos.", "metadata": {"source": "Controle de Acesso", "categoria": "Segurança em Nuvem"}},

    # Categoria: Governança, Compliance e LGPD
    {"id": "doc_016", "text": "A LGPD (Lei Geral de Proteção de Dados - Lei 13.709/2018) estabelece regras estritas sobre coleta, armazenamento e compartilhamento de dados pessoais em território brasileiro, prevendo multas de até 2% do faturamento.", "metadata": {"source": "Legislação Brasileira", "categoria": "LGPD"}},
    {"id": "doc_017", "text": "Dados Pessoais Sensíveis, segundo a LGPD, incluem informações sobre origem racial, convicção religiosa, saúde, genética ou biometria. O tratamento desses dados exige bases legais mais rigorosas do que dados comuns.", "metadata": {"source": "Classificação de Dados", "categoria": "LGPD"}},
    {"id": "doc_018", "text": "O DPO (Data Protection Officer), ou Encarregado de Dados, é o profissional nomeado pela empresa para atuar como canal de comunicação entre o controlador, os titulares dos dados e a ANPD (Autoridade Nacional).", "metadata": {"source": "Governança Corporativa", "categoria": "LGPD"}},
    {"id": "doc_019", "text": "A anonimização é uma técnica de processamento de dados que remove definitivamente a associação de informações a uma pessoa. Dados devidamente anonimizados não estão sujeitos às regras da LGPD.", "metadata": {"source": "Técnicas de Privacidade", "categoria": "LGPD"}},
    {"id": "doc_020", "text": "O Relatório de Impacto à Proteção de Dados Pessoais (RIPD) é um documento essencial em projetos de alto risco, detalhando os processos de tratamento e as medidas adotadas para mitigar violações de privacidade.", "metadata": {"source": "Compliance e Auditoria", "categoria": "LGPD"}},
    {"id": "doc_021", "text": "O consentimento, na LGPD, deve ser livre, informado e inequívoco. Contudo, não é a única base legal: o cumprimento de obrigação legal e o legítimo interesse também justificam o tratamento de dados em cenários específicos.", "metadata": {"source": "Bases Legais", "categoria": "LGPD"}},

    # Categoria: Resposta a Incidentes e Monitoramento
    {"id": "doc_022", "text": "SIEM (Security Information and Event Management) são sistemas que agregam e analisam logs de redes e servidores em tempo real, utilizando correlação de eventos para detectar possíveis invasões.", "metadata": {"source": "Monitoramento Contínuo", "categoria": "Operações de Segurança"}},
    {"id": "doc_023", "text": "Um SOC (Security Operations Center) é a central de comando composta por pessoas, processos e tecnologia, dedicada a monitorar a infraestrutura de TI 24/7 e responder ativamente a incidentes.", "metadata": {"source": "Estrutura de Defesa", "categoria": "Operações de Segurança"}},
    {"id": "doc_024", "text": "O Plano de Resposta a Incidentes (IRP) define etapas claras para conter violações: Preparação, Identificação, Contenção, Erradicação, Recuperação e Lições Aprendidas.", "metadata": {"source": "Gestão de Crises", "categoria": "Operações de Segurança"}},
    {"id": "doc_025", "text": "A Análise Forense Digital envolve a coleta e preservação de evidências de sistemas comprometidos, utilizando cópias bit a bit (imagens de disco) para não alterar o estado original do hardware invasado.", "metadata": {"source": "Investigação Cibernética", "categoria": "Operações de Segurança"}},
    {"id": "doc_026", "text": "Testes de Invasão (Pentests) simulam ataques cibernéticos reais sob contrato (White Hat). A abordagem 'Black Box' testa as defesas sem nenhum conhecimento prévio da infraestrutura do alvo.", "metadata": {"source": "Segurança Ofensiva", "categoria": "Operações de Segurança"}},

    # Categoria: DevSecOps e Segurança de Aplicações
    {"id": "doc_027", "text": "DevSecOps é a filosofia de integrar ferramentas e práticas de segurança desde as fases iniciais de planejamento e codificação (Shift-Left), em vez de apenas testar o produto final.", "metadata": {"source": "Engenharia de Software", "categoria": "DevSecOps"}},
    {"id": "doc_028", "text": "SAST (Static Application Security Testing) analisa o código-fonte em repouso durante o desenvolvimento, identificando vulnerabilidades como hardcoded secrets ou falhas de injeção antes da compilação.", "metadata": {"source": "Análise de Código", "categoria": "DevSecOps"}},
    {"id": "doc_029", "text": "DAST (Dynamic Application Security Testing) interage com a aplicação web em execução de fora para dentro, simulando ataques como um hacker real para encontrar falhas de autenticação ou configuração.", "metadata": {"source": "Testes Dinâmicos", "categoria": "DevSecOps"}},
    {"id": "doc_030", "text": "Gestão de Postura de Segurança em Nuvem (CSPM) automatiza a identificação e correção de erros de configuração em provedores de nuvem pública, evitando vazamentos causados por buckets de armazenamento mal configurados.", "metadata": {"source": "Automação de Segurança", "categoria": "DevSecOps"}}
]

def seed():
    print(f"Iniciando a inserção de {len(DOCUMENTS)} documentos...")
    sucesso = 0
    falhas = 0

    for i, doc in enumerate(DOCUMENTS):
        print(f"[{i+1:02d}/{len(DOCUMENTS)}] Enviando: {doc['id']}...", end=" ", flush=True)
        try:
            res = requests.post("http://localhost:5000/ingest", json={"documents": [doc]})
            
            if res.status_code == 200:
                print("OK!")
                sucesso += 1
            else:
                print(f"Erro {res.status_code}!")
                falhas += 1
                
        except Exception as e:
            print("Falha de conexão com o servidor.")
            falhas += 1

        if i < len(DOCUMENTS) - 1:
            time.sleep(4)

    print("\n" + "="*40)
    print(f"Finalizado! {sucesso} documentos inseridos com sucesso.")
    if falhas > 0:
        print(f"Houve {falhas} falhas. Verifique se o servidor Flask está rodando.")
    print("="*40)

if __name__ == "__main__":
    seed()