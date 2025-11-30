from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import os
import db
import asyncio
from jinja2 import Template

app = FastAPI()

ADMIN_SECRET = os.getenv("ADMIN_SECRET", "secret")

INDEX_HTML = """
<!doctype html>
<html>
<head><meta charset="utf-8"><title>LoftCafe — Reviews admin</title></head>
<body>
<h2>Отзывы</h2>
<p><a href="/admin">Обновить</a></p>
<table border="1" cellpadding="8" cellspacing="0">
<tr><th>ID</th><th>Стол</th><th>Категория</th><th>Текст</th><th>Время</th><th>Действие</th></tr>
{% for r in reviews %}
<tr>
<td>{{ r[0] }}</td>
<td>{{ r[1] }}</td>
<td>{{ r[2] }}</td>
<td style="max-width:400px; word-wrap:break-word;">{{ r[3] }}</td>
<td>{{ r[4] }}</td>
<td>
<form method="post" action="/admin/delete/{{ r[0] }}">
<input type="hidden" name="secret" value="{{ secret }}">
<button type="submit">Удалить</button>
</form>
</td>
</tr>
{% endfor %}
</table>
</body>
</html>
"""

def check_secret(req: Request):
    # секрет можно передавать GET/POST параметром или заголовком X-ADMIN-SECRET
    q = req.query_params.get("secret") or req.headers.get("X-ADMIN-SECRET")
    if q != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.on_event("startup")
async def startup_event():
    await db.init_db()

@app.get("/admin", response_class=HTMLResponse)
async def admin_index(request: Request):
    check_secret(request)
    reviews = await db.fetch_all_reviews()
    tmpl = Template(INDEX_HTML)
    return tmpl.render(reviews=reviews, secret=ADMIN_SECRET)

@app.post("/admin/delete/{review_id}")
async def admin_delete(review_id: int, request: Request):
    form = await request.form()
    secret = form.get("secret")
    if secret != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    await db.delete_review(review_id)
    return RedirectResponse(url=f"/admin?secret={ADMIN_SECRET}", status_code=303)
