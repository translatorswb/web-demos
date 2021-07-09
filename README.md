# TWB Web demos

A static simple website to demonstrate TWB's language technology services:

- [Automatic speech recognition (ASR-API)](https://github.com/translatorswb/ASR-API)
- [Automatic speech recognition (MT-API)](https://github.com/translatorswb/TWB-MT-fastapi)

## Requirements

Required modules are listed in `requirements.txt`

## Installation & Usage

Clone repository and install required modules
```bash
$ git clone https://github.com/translatorswb/web-demos.git
$ cd web-demos
$ pip install -r requirements.txt
```

Edit the url endpoints of the APIs you want to use in `.env`

```bash
MT_API_URL=http://localhost:8001/api/v1/translate
ASR_API_URL=http://localhost:8010/transcribe/
```

Run the server

```bash
$ uvicorn app.main:app --reload --port 8080
```

Visit [http://127.0.0.1:8080/](http://127.0.0.1:8080/).

## Author

[Alp Öktem](https://alpoktem.github.io)

## Sources

Main site architecture by [Shinichi Okada](https://github.com/shinokada/fastapi-web-starter) 

Audio recording logic by [addpipe](https://github.com/addpipe/simple-web-audio-recorder-demo)

Kaldi-web interface by [dtreskunov](https://github.com/dtreskunov)

English model by [Alpha Cepei](https://alphacephei.com/vosk/models)

## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
