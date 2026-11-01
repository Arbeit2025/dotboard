"""お絵かきボード dotboard

16×16 のキャンバスにブラウザ上でドット絵を描くツール。
色パレット（12色）から選んでクリック／ドラッグで塗り、
PNG 画像として保存できる。描画はすべてブラウザ側で行い、
サーバーはページを返すだけ。単一ファイル Flask。
"""
import os

from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

COLORS = [
    "#000000", "#ffffff", "#e03131", "#f08c00",
    "#ffd43b", "#2f9e44", "#1971c2", "#74c0fc",
    "#9775fa", "#f783ac", "#a0522d", "#868e96",
]

PAGE = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>お絵かきボード</title>
<style>body{font-family:sans-serif;max-width:680px;margin:2em auto;padding:0 1em}
canvas{border:1px solid #999;image-rendering:pixelated;touch-action:none;background:#fff}
.swatch{width:28px;height:28px;border:2px solid #ccc;display:inline-block;cursor:pointer;padding:0}
.swatch.selected{border-color:#333}
button{margin:.3em .2em}</style>
</head><body>
<h1>お絵かきボード</h1>
<p>16×16 のドット絵ボードです。色を選んで、クリックやドラッグで描いてください。</p>
<div id="palette">
{% for c in colors %}<button type="button" class="swatch{% if loop.first %} selected{% endif %}" data-color="{{ c }}" style="background:{{ c }}" title="{{ c }}"></button>{% endfor %}
</div>
<canvas id="board" width="16" height="16" style="width:384px;height:384px"></canvas>
<div>
  <button type="button" id="clear">ぜんぶ消す</button>
  <button type="button" id="save">PNGで保存</button>
</div>
<script>
const canvas = document.getElementById('board');
const ctx = canvas.getContext('2d');
ctx.fillStyle = '#ffffff';
ctx.fillRect(0, 0, 16, 16);
let color = '{{ colors[0] }}';
let drawing = false;
document.getElementById('palette').addEventListener('click', (e) => {
  const btn = e.target.closest('.swatch');
  if (!btn) return;
  color = btn.dataset.color;
  document.querySelectorAll('.swatch').forEach(s => s.classList.toggle('selected', s === btn));
});
function pos(e) {
  const r = canvas.getBoundingClientRect();
  const x = Math.floor((e.clientX - r.left) / r.width * 16);
  const y = Math.floor((e.clientY - r.top) / r.height * 16);
  return [x, y];
}
function paint(e) {
  const [x, y] = pos(e);
  if (x < 0 || x > 15 || y < 0 || y > 15) return;
  ctx.fillStyle = color;
  ctx.fillRect(x, y, 1, 1);
}
canvas.addEventListener('mousedown', (e) => { drawing = true; paint(e); });
canvas.addEventListener('mousemove', (e) => { if (drawing) paint(e); });
window.addEventListener('mouseup', () => { drawing = false; });
canvas.addEventListener('touchstart', (e) => { e.preventDefault(); paint(e.touches[0]); }, {passive: false});
canvas.addEventListener('touchmove', (e) => { e.preventDefault(); paint(e.touches[0]); }, {passive: false});
document.getElementById('clear').addEventListener('click', () => {
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, 16, 16);
});
document.getElementById('save').addEventListener('click', () => {
  const out = document.createElement('canvas');
  out.width = 384; out.height = 384;
  const octx = out.getContext('2d');
  octx.imageSmoothingEnabled = false;
  octx.drawImage(canvas, 0, 0, 384, 384);
  const a = document.createElement('a');
  a.href = out.toDataURL('image/png');
  a.download = 'dotboard.png';
  a.click();
});
</script>
</body></html>"""


@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"})


@app.route("/")
def index():
    return render_template_string(PAGE, colors=COLORS)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
