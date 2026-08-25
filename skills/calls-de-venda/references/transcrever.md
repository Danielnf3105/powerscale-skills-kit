# Transcrever uma gravação

Só é preciso quando a ferramenta de reunião não deu transcrição. Antes de
instalar seja o que for, verificar se a call já tem transcrição no Fathom, no
Fireflies, no Meet (Notas do Gemini) ou no Teams. Poupa meia hora.

## O caminho mais simples (sem instalar nada)

Muitas ferramentas de reunião exportam a transcrição em `.txt`, `.vtt` ou
`.docx`. Basta pedir o ficheiro e ler.

## Transcrever localmente

Precisa de duas coisas: `ffmpeg` (para extrair o áudio) e um modelo de
transcrição.

**Windows (PowerShell, uma vez):**

```powershell
winget install Gyan.FFmpeg
winget install Python.Python.3.12
pip install faster-whisper
```

**Extrair o áudio antes de transcrever** (um vídeo de 1 hora passa de 2 GB para
30 MB, e transcreve mais depressa):

```powershell
ffmpeg -i call.mp4 -vn -ac 1 -ar 16000 -c:a aac -b:a 64k call.m4a
```

**Transcrever:**

```python
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8")
segmentos, info = m.transcribe(
    "call.m4a",
    language="pt",                      # forçar sempre, senão traduz
    initial_prompt="termos do nicho, nomes de marca, nomes próprios",
    vad_filter=True,
)
for s in segmentos:
    print(f"[{int(s.start//60):02d}:{int(s.start%60):02d}] {s.text.strip()}")
```

## Armadilhas

- **Modelo `small` inventa palavras** em português quando há termos técnicos.
  Usar `medium`.
- **Sem `language="pt"`** o modelo às vezes decide traduzir para inglês a meio.
- **`initial_prompt` é o que salva os nomes próprios** e o vocabulário do nicho.
  Escrever lá os termos que aparecem na call.
- **Uma de cada vez.** Duas transcrições em paralelo num portátil normal enchem
  a memória e rebentam as duas.
- Guardar a transcrição e apagar o vídeo. O que interessa é o texto.
