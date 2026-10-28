# Projekt rodokmenu — instrukce pro OpenAI Codex

Tento projekt spravuje skill `rodokmen` (v Codexu jej můžeš vyvolat jako `$rodokmen`).

Při každém pokračování:
1. Načti `rodokmen` ze seznamu dostupných skills a ověř, zda odpovídá verze v `.skill_verze`.
2. Přečti `data/STAV.md` a poslední relevantní části `data/research_log.md`, pak stručně shrň rozpracované větve.
3. Pokračuj česky, srozumitelně pro nezkušeného uživatele. Zbytečné technické volby řeš samostatně.
4. Pro matriční nález vyžaduj odkaz na archiv, identifikaci knihy/snímku, přepis, snímek/výřez a explicitní jistotu.
5. Nepovyšuj odhady nebo data z cizích stromů na přímé doklady, neslučuj stejnojmenné osoby bez důkazů.
6. Podagenti mohou hledat a dělat první přepis, ale `data/` smí upravovat pouze hlavní agent po vlastní kontrole.
7. Zapisuj technické poznatky do `poznamky_pro_skill.md` bez osobních údajů; nic z projektu nesdílej automaticky.
8. Rodinné dokumenty a data žijících osob drž lokálně, ne v veřejném GitHubu. Zveřejnění webu jen se schválením.
9. V prostředí bez prohlížeče nebo s blokovanou sítí práci poctivě zastav na relevantním kroku, řekni co chybí a navrhni předání snímku.
10. Před větším vyhledáváním a vyšší spotřebou modelů vysvětli plán a nech si jej schválit.
