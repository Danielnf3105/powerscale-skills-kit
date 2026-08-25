#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PowerScale Skills Kit: que ANUNCIO trouxe os melhores clientes.

Junta o que esta no GoHighLevel (contactos, oportunidades, valor ganho) com o
que esta no Facebook (nome do anuncio, gasto), e ordena por resultado real, nao
por leads.

  python3 ghl_meta.py --diagnostico     ve o que ha e diz se da para juntar
  python3 ghl_meta.py --relatorio       o quadro por nome de anuncio
  python3 ghl_meta.py --relatorio --dias 60 --csv relatorio.csv

Chaves, em ~/.config/chaves/secrets.env (uma por linha, NOME=valor):

  GHL_TOKEN=          Private Integration token da subconta (Settings ->
                      Private Integrations -> criar, com os scopes de leitura
                      de contacts e opportunities)
  GHL_LOCATION_ID=    o id da subconta (Settings -> Business Profile)
  META_TOKEN=         token de utilizador de sistema do Business Manager
  META_AD_ACCOUNT=    act_1234567890

O DIAGNOSTICO corre-se primeiro e sempre. Se os anuncios nao levarem as macros
no link, nao ha nada para juntar, e o relatorio sairia vazio sem dizer porque.
"""
import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

GHL_BASE = "https://services.leadconnectorhq.com"
GHL_VERSION = "2021-07-28"
GRAPH = "https://graph.facebook.com/v21.0"
COFRE = Path.home() / ".config" / "chaves" / "secrets.env"


# --------------------------------------------------------------- chaves

def chaves():
    v = {}
    if COFRE.exists():
        for linha in COFRE.read_text(encoding="utf-8-sig").splitlines():
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            k, _, val = linha.partition("=")
            v[k.strip()] = val.strip().strip('"').strip("'")
    for k in ("GHL_TOKEN", "GHL_LOCATION_ID", "META_TOKEN", "META_AD_ACCOUNT"):
        if os.environ.get(k):
            v[k] = os.environ[k]
    return v


def exigir(v, nomes):
    faltam = [n for n in nomes if not v.get(n)]
    if faltam:
        print("Faltam chaves no cofre (%s):" % COFRE)
        for f in faltam:
            print("  %s=" % f)
        print("\nAbre o ficheiro, cola os valores, e corre outra vez.")
        print("Nunca colar chaves no chat: uma chave que passa por ali fica queimada.")
        sys.exit(1)


# --------------------------------------------------------------- rede

def pedir(url, headers, tentativas=3):
    ultimo = None
    for _ in range(tentativas):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            corpo = e.read().decode("utf-8", "replace")[:300]
            raise SystemExit("Erro %s em %s\n%s" % (e.code, url.split("?")[0], corpo))
        except (urllib.error.URLError, OSError, json.JSONDecodeError) as e:
            ultimo = e
    raise SystemExit("Nao consegui falar com %s: %s" % (url.split("?")[0], ultimo))


def ghl(v, caminho, params):
    url = "%s%s?%s" % (GHL_BASE, caminho, urllib.parse.urlencode(params))
    return pedir(url, {
        "Authorization": "Bearer " + v["GHL_TOKEN"],
        "Version": GHL_VERSION,
        "Accept": "application/json",
    })


def meta(v, caminho, params):
    p = dict(params)
    p["access_token"] = v["META_TOKEN"]
    url = "%s%s?%s" % (GRAPH, caminho, urllib.parse.urlencode(p))
    return pedir(url, {"Accept": "application/json"})


# --------------------------------------------------------------- GHL

# A atribuicao no GHL vive em sitios diferentes conforme a versao da conta e
# conforme quem escreveu o formulario. Por isso procura-se em todos, em vez de
# assumir um.
CAMPOS_UTM = ("utmContent", "utm_content", "utmCampaign", "utm_campaign",
              "utmSource", "utm_source", "utmMedium", "utm_medium",
              "campaign", "campaignId", "fbclid", "sessionSource",
              "medium", "mediumId", "referrer", "url")


def atribuicao_de(contacto):
    """Devolve um dicionario plano com o que houver de atribuicao."""
    saida = {}
    for chave in ("lastAttributionSource", "attributionSource", "attributions"):
        bloco = contacto.get(chave)
        if isinstance(bloco, list):
            bloco = bloco[0] if bloco else None
        if isinstance(bloco, dict):
            for k, val in bloco.items():
                if val not in (None, "") and k not in saida:
                    saida[k] = val
    # Campos personalizados com cheiro a UTM (muita gente guarda-os assim).
    for cf in contacto.get("customFields") or []:
        nome = str(cf.get("key") or cf.get("id") or "").lower()
        val = cf.get("value") if cf.get("value") is not None else cf.get("field_value")
        if val in (None, ""):
            continue
        for alvo in ("utm_content", "utm_campaign", "utm_source", "utm_medium",
                     "ad_id", "adname", "ad_name", "fbclid"):
            if alvo in nome and alvo not in saida:
                saida[alvo] = val
    for k in CAMPOS_UTM:
        if k in contacto and contacto[k] not in (None, "") and k not in saida:
            saida[k] = contacto[k]
    return saida


def ler_contactos(v, maximo=5000):
    contactos, cursor = [], None
    while len(contactos) < maximo:
        params = {"locationId": v["GHL_LOCATION_ID"], "limit": "100"}
        if cursor:
            params["startAfterId"] = cursor
        pagina = ghl(v, "/contacts/", params)
        lista = pagina.get("contacts") or []
        if not lista:
            break
        contactos.extend(lista)
        novo = str(lista[-1].get("id") or "")
        if not novo or novo == cursor:
            break
        cursor = novo
        print("  ... %d contactos" % len(contactos), file=sys.stderr)
    return contactos[:maximo]


def ler_oportunidades(v, maximo=5000):
    tudo = []
    for pagina in range(1, 51):
        try:
            res = ghl(v, "/opportunities/search",
                      {"location_id": v["GHL_LOCATION_ID"], "limit": "100", "page": str(pagina)})
        except SystemExit:
            break
        lista = res.get("opportunities") or []
        if not lista:
            break
        tudo.extend(lista)
        if len(tudo) >= maximo:
            break
    return tudo[:maximo]


# --------------------------------------------------------------- Meta

def ler_anuncios(v, dias):
    campos = "ad_id,ad_name,adset_name,campaign_name,spend,impressions,clicks"
    res = meta(v, "/%s/insights" % v["META_AD_ACCOUNT"], {
        "level": "ad",
        "fields": campos,
        "date_preset": "maximum" if dias > 90 else "last_%dd" % dias,
        "time_increment": "all_days",
        "limit": "500",
    })
    return res.get("data") or []


def ler_links(v):
    """O link de cada anuncio, para ver se leva as macros de UTM."""
    res = meta(v, "/%s/ads" % v["META_AD_ACCOUNT"], {
        "fields": "id,name,creative{object_story_spec,asset_feed_spec,url_tags}",
        "limit": "300",
        "effective_status": '["ACTIVE","PAUSED"]',
    })
    links = {}
    for ad in res.get("data") or []:
        cr = ad.get("creative") or {}
        achados = []
        texto = json.dumps(cr, ensure_ascii=False)
        for pedaco in texto.split('"'):
            if pedaco.startswith("http") and len(pedaco) > 12:
                achados.append(pedaco)
        links[str(ad["id"])] = {"nome": ad.get("name", ""), "links": achados[:4]}
    return links


# --------------------------------------------------------------- juntar

def id_do_anuncio(atrib):
    """O ad_id vindo da atribuicao, se o anuncio levar a macro no link."""
    for chave in ("utm_content", "utmContent", "ad_id", "adId"):
        val = str(atrib.get(chave) or "").strip()
        if val.isdigit() and len(val) >= 10:
            return val
    for chave in ("url", "referrer"):
        val = str(atrib.get(chave) or "")
        if "utm_content=" in val:
            pedaco = val.split("utm_content=")[1].split("&")[0]
            if pedaco.isdigit() and len(pedaco) >= 10:
                return pedaco
    return ""


def nome_do_anuncio(atrib):
    """Plano B: o nome do anuncio escrito a mao nos UTM."""
    for chave in ("utm_content", "utmContent", "ad_name", "adname",
                  "utm_campaign", "utmCampaign", "campaign"):
        val = str(atrib.get(chave) or "").strip()
        if val and not val.isdigit():
            return val
    return ""


def euros(x):
    return "%8.2f" % float(x or 0)


# --------------------------------------------------------------- comandos

def diagnostico(v, dias):
    print("Diagnostico: da para saber que anuncio traz os melhores clientes?")
    print("=" * 66)

    print("\n1. GoHighLevel")
    contactos = ler_contactos(v, maximo=500)
    print("   %d contactos lidos (amostra)" % len(contactos))
    com_atrib = [c for c in contactos if atribuicao_de(c)]
    print("   %d com atribuicao registada" % len(com_atrib))
    com_id = [c for c in com_atrib if id_do_anuncio(atribuicao_de(c))]
    com_nome = [c for c in com_atrib if nome_do_anuncio(atribuicao_de(c))]
    print("   %d com o ID do anuncio (juncao exata)" % len(com_id))
    print("   %d so com texto nos UTM (juncao por nome, aproximada)" % len(com_nome))
    if com_atrib:
        exemplo = atribuicao_de(com_atrib[0])
        print("\n   O que o GHL guarda, num contacto real:")
        for k in sorted(exemplo)[:12]:
            print("     %-18s %s" % (k, str(exemplo[k])[:60]))

    print("\n2. Facebook")
    anuncios = ler_anuncios(v, dias)
    print("   %d anuncios com dados nos ultimos %d dias" % (len(anuncios), dias))
    links = ler_links(v)
    com_macro, sem_macro = [], []
    for ad_id, d in links.items():
        texto = " ".join(d["links"])
        (com_macro if "{{ad.id}}" in texto or "utm_content=" in texto else sem_macro).append(d["nome"])
    print("   %d anuncios com UTM no link" % len(com_macro))
    print("   %d anuncios SEM UTM nenhum no link" % len(sem_macro))

    print("\n3. Veredicto")
    if len(com_id) >= 5:
        print("   DA. Juncao exata pelo ID do anuncio. Corre --relatorio.")
    elif len(com_nome) >= 5:
        print("   DA, mas por NOME e aproximado. Dois anuncios com o mesmo nome")
        print("   ficam somados. Para ficar exato, ver o passo abaixo.")
    else:
        print("   NAO DA AINDA. Os anuncios nao estao a passar os UTM ao GHL,")
        print("   por isso nao ha nada para juntar. Nao e um problema do GHL nem")
        print("   do Facebook: e o link do anuncio que nao carrega a origem.")

    if sem_macro or len(com_id) < 5:
        print("\n   O que fazer, uma vez so, e passa a valer para sempre:")
        print("   poe isto no fim do link de destino de cada anuncio (a Meta")
        print("   substitui as chavetas sozinha na hora do clique):")
        print("")
        print("     ?utm_source=facebook&utm_medium=paid")
        print("      &utm_campaign={{campaign.name}}")
        print("      &utm_content={{ad.id}}")
        print("      &utm_term={{adset.name}}")
        print("")
        print("   O utm_content leva o ID e nao o nome de proposito: o nome muda")
        print("   quando se renomeia um anuncio, e o historico parte-se. O nome")
        print("   vem do Facebook na hora do relatorio.")
        if sem_macro:
            print("\n   Sem UTM nenhum (%d): %s" % (len(sem_macro), ", ".join(sem_macro[:6])))
    return 0


def relatorio(v, dias, ficheiro_csv):
    print("A ler o GoHighLevel...", file=sys.stderr)
    contactos = ler_contactos(v)
    oportunidades = ler_oportunidades(v)
    print("A ler o Facebook...", file=sys.stderr)
    anuncios = ler_anuncios(v, dias)

    por_id = {str(a.get("ad_id")): a for a in anuncios}
    nome_por_id = {i: a.get("ad_name", "") for i, a in por_id.items()}

    # Oportunidades por contacto, para saber o que virou dinheiro.
    opp_por_contacto = defaultdict(list)
    for o in oportunidades:
        cid = str((o.get("contact") or {}).get("id") or o.get("contactId") or "")
        if cid:
            opp_por_contacto[cid].append(o)

    linhas = defaultdict(lambda: {"leads": 0, "opp": 0, "ganhas": 0, "valor": 0.0,
                                  "gasto": 0.0, "ad_ids": set(), "exato": True})
    sem_origem = 0
    for c in contactos:
        atrib = atribuicao_de(c)
        ad_id = id_do_anuncio(atrib)
        if ad_id:
            chave = nome_por_id.get(ad_id) or ("ad %s (fora da janela)" % ad_id)
            exato = True
        else:
            chave = nome_do_anuncio(atrib)
            exato = False
            if not chave:
                sem_origem += 1
                continue
        l = linhas[chave]
        l["leads"] += 1
        l["exato"] = l["exato"] and exato
        if ad_id:
            l["ad_ids"].add(ad_id)
        for o in opp_por_contacto.get(str(c.get("id")), []):
            l["opp"] += 1
            estado = str(o.get("status") or "").lower()
            if estado == "won":
                l["ganhas"] += 1
                l["valor"] += float(o.get("monetaryValue") or 0)

    for chave, l in linhas.items():
        for ad_id in l["ad_ids"]:
            l["gasto"] += float(por_id.get(ad_id, {}).get("spend") or 0)

    ordenado = sorted(linhas.items(),
                      key=lambda kv: (kv[1]["valor"], kv[1]["ganhas"], kv[1]["leads"]),
                      reverse=True)

    print("")
    print("Que anuncio trouxe os melhores clientes, ultimos %d dias" % dias)
    print("=" * 96)
    print("%-34s %6s %6s %7s %10s %9s %9s" %
          ("ANUNCIO", "LEADS", "OPORT", "GANHAS", "VALOR", "GASTO", "CUSTO/LEAD"))
    print("-" * 96)
    for chave, l in ordenado[:30]:
        cpl = (l["gasto"] / l["leads"]) if l["leads"] and l["gasto"] else 0
        marca = "" if l["exato"] else " ~"
        print("%-34s %6d %6d %7d %10s %9s %9s%s" %
              (chave[:34], l["leads"], l["opp"], l["ganhas"],
               euros(l["valor"]), euros(l["gasto"]), euros(cpl), marca))
    print("-" * 96)
    print("%d contactos sem origem nenhuma (nao contam para o quadro)." % sem_origem)
    if any(not l["exato"] for _, l in ordenado):
        print("As linhas com ~ foram juntas por NOME e sao aproximadas.")
        print("Corre --diagnostico para ver como se passa a exato.")
    print("")
    print("Le por VALOR GANHO, nao por leads. O anuncio que traz mais leads e")
    print("quase nunca o que traz mais dinheiro, e e por isso que se corta o")
    print("anuncio errado.")

    if ficheiro_csv:
        with open(ficheiro_csv, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["anuncio", "leads", "oportunidades", "ganhas", "valor",
                        "gasto", "custo_por_lead", "juncao"])
            for chave, l in ordenado:
                cpl = (l["gasto"] / l["leads"]) if l["leads"] and l["gasto"] else 0
                w.writerow([chave, l["leads"], l["opp"], l["ganhas"],
                            round(l["valor"], 2), round(l["gasto"], 2), round(cpl, 2),
                            "exata" if l["exato"] else "por nome"])
        print("CSV: %s" % ficheiro_csv)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--diagnostico", action="store_true")
    ap.add_argument("--relatorio", action="store_true")
    ap.add_argument("--dias", type=int, default=30)
    ap.add_argument("--csv")
    a = ap.parse_args()

    v = chaves()
    exigir(v, ["GHL_TOKEN", "GHL_LOCATION_ID", "META_TOKEN", "META_AD_ACCOUNT"])

    if a.relatorio:
        return relatorio(v, a.dias, a.csv)
    return diagnostico(v, a.dias)


if __name__ == "__main__":
    sys.exit(main())
