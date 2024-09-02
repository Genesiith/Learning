from transformers import AutoProcessor, BarkModel
import http.server
import socketserver
import json

processor = AutoProcessor.from_pretrained("suno/bark")
model = BarkModel.from_pretrained("suno/bark")

model = model.to('cuda')


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        audio_array = gen(data['text'], "v2/"+data["lang"]+"_speaker_" + data['model'])
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'audio_array': audio_array.tolist()}).encode())

def gen(text, voice_preset):
    inputs = processor(text, voice_preset=voice_preset)

    inputs = {k: v.to('cuda') for k, v in inputs.items()}

    audio_array = model.generate(**inputs)
    audio_array = audio_array.cpu().numpy().squeeze()
    return audio_array

handler_object = MyHttpRequestHandler
PORT = 8461

with socketserver.TCPServer(("", PORT), handler_object) as httpd:
    print("Server is listening at port", PORT)
    httpd.serve_forever()
