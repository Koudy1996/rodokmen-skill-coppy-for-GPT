# Co se změnilo proti zdrojovému skillu

Vstupní verze: [sarsonj/rodokmen-skill](https://github.com/sarsonj/rodokmen-skill), říjen 2026, `0.5.0`. Tato adaptace je určená pro Codex, nikoli pro platformově specifický plugin původního agenta.

## Struktura a spouštění

- `skills/rodokmen` → `.agents/skills/rodokmen` (automatické rozpoznání v Codexu).
- Starší plugin manifesty se nepřenášejí; `SKILL.md` zachovává jméno `rodokmen` a doplňuje metadata `agents/openai.yaml`.
- Projektový instruktážní soubor přejmenován na `AGENTS.md` a změněn jeho obsah.
- Inicializátor nyní vytváří `.codex/config.toml` a role `.codex/agents/`, nepřidává žádné staré desktopové spouštěče.
- Skripty Python/Node, datové formáty a demonstrační web jsou v základu zachované.

## Modelová strategie

Hlavní `gpt-6.1-sol` (high). Úlohoví pomocníci: `gpt-6.1-terra` (medium) pro první čtení snímku, `gpt-6-astra` (high) pro nezávislé rozhodující ověření, `gpt-6.1-sol` (medium) pro archivní rešerše a `gpt-6-luna` (low) pro jednoduché indexy. Nastavení není benchmark a nedokazuje přesnost na historické češtině/kurentu. Když model není v Codexu dostupný, zvol alternativu; nelze garantovat automatický fallback konfiguračního souboru.

## Známá omezení

- Bez síťového přístupu nebo skutečného prohlížeče se některé archivní portály automaticky neotevřou. Uživatel může dodat snímky ručně.
- Žádný agent nesmí řešit CAPTCHA ani obcházet omezení archivů.
- Nepřenesen je jediný původní soubor bez doložené licence MIT: obsáhlý `playbook.md`; místo něho je v kopii odkaz s upozorněním.
- Velký demonstrační screenshot `docs/ukazka-web.png` není přenesen kvůli limitu dostupného přenosu obrázků; ostatní obrázky včetně výřezů, na nichž ukázkový projekt závisí, jsou zachované.
- Přepis rukopisu je důkazně náročný; shoda více modelů bez kontroly originálu není dostatečná.

## Testování

`python3 scripts/verify_codex.py` kontroluje závislosti mezi soubory, Python a JSON/TOML syntaxi a dvě inicializace. Nenahrazuje živé testy archivů ani úspěšné generování rodokmenu. Po `npm install` je třeba ve vytvořeném ukázkovém projektu provést `npm run nahled`. Uživatel má rozhodující slovo při sporné identifikaci a zveřejňování údajů.
