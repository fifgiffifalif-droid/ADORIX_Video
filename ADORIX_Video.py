import os
from flask import Flask, request, redirect, send_from_directory, render_template_string

app = Flask(__name__)
BD = os.path.dirname(os.path.abspath(__file__))
VD, SD = os.path.join(BD, 'v'), os.path.join(BD, 's')
for p in [VD, SD]: os.makedirs(p, exist_ok=True)

HT = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>ADORIX Hub</title>
<style>
    body { font-family: sans-serif; background: #0a0a0c; color: #fff; margin: 0; padding: 20px; }
    .box { max-width: 1100px; margin: 0 auto; display: flex; flex-direction: column; gap: 30px; }
    header { text-align: center; margin-bottom: 10px; }
    header h1 { font-size: 1.8rem; margin: 0 0 10px 0; color: #f43f5e; font-weight: bold; }
    header p { color: #a1a1aa; font-size: 0.95rem; line-height: 1.4; max-width: 600px; margin: 0 auto; }
    h2 { font-size: 1.3rem; border-left: 3px solid #f43f5e; padding-left: 8px; margin: 0; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
    .card { background: #18181b; border: 1px solid #27272a; border-radius: 12px; overflow: hidden; padding: 6px; }
    video { width: 100%; display: block; border-radius: 8px; background: #000; }
    .flex { display: flex; gap: 15px; overflow-x: auto; padding-bottom: 10px; }
    .scard { width: 200px; flex-shrink: 0; background: #18181b; border: 1px solid #27272a; border-radius: 12px; padding: 6px; }
    .scard video { height: 350px; object-fit: cover; }
    form { background: #111; border: 1px dashed #444; padding: 15px; border-radius: 12px; max-width: 400px; margin: 0 auto; display: flex; flex-direction: column; gap: 10px; }
    input, select, button { padding: 10px; border-radius: 6px; border: 1px solid #333; background: #222; color: #fff; }
    button { background: #f43f5e; font-weight: bold; cursor: pointer; border: none; }
</style></head><body><div class="box">
    <header>
        <h1>🏠 ADORIX VIDEO HUB</h1>
        <p>Most video hostings know everything about you: your account, phone number, or some even your passport, but we — we know that you love privacy.</p>
    </header>

    <form action="/u" method="POST" enctype="multipart/form-data">
        <input type="file" name="file" accept="video/*" required>
        <select name="t"><option value="v">🎬 Video</option><option value="s">📱 Shorts</option></select>
        <button type="submit">Upload</button>
    </form>
    <h2>Shorts Feed 📱</h2>
    <div class="flex">
        {% for s in shorts %}<div class="scard"><video loop controls class="bvd"><source src="/s/{{s}}"></video></div>{% endfor %}
    </div>
    <h2>All Videos 🎬</h2>
    <div class="grid">
        {% for v in videos %}<div class="card"><video controls class="bvd"><source src="/v/{{v}}"></video></div>{% endfor %}
    </div>
</div>
<script>
    document.addEventListener("play", e => {
        if (!e.target.classList.contains('bvd') || e.target.dataset.b) return;
        try {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const src = ctx.createMediaElementSource(e.target);
            const gain = ctx.createGain();
            gain.gain.value = 2.0; // 2x volume boost
            src.connect(gain); gain.connect(ctx.destination);
            e.target.dataset.b = "1";
        } catch(err) {}
    }, true);
</script></body></html>"""

@app.route('/')
def idx():
    v = [f for f in os.listdir(VD) if f.lower().endswith(('.mp4', '.mov', '.avi', '.webm'))]
    s = [f for f in os.listdir(SD) if f.lower().endswith(('.mp4', '.mov', '.avi', '.webm'))]
    return render_template_string(HT, videos=v, shorts=s)

@app.route('/v/<n>')
def get_v(n): return send_from_directory(VD, n)

@app.route('/s/<n>')
def get_s(n): return send_from_directory(SD, n)

@app.route('/u', methods=['POST'])
def upl():
    f = request.files.get('file')
    if f and f.filename: f.save(os.path.join(SD if request.form.get('t') == 's' else VD, f.filename))
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
