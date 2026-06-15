from flask import Flask, render_template, request
import mariadb
import settings

app = Flask(__name__)

def get_conn():
    return mariadb.connect(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name
    )

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 新規追加処理
        if "task" in request.form:
            conn = get_conn()
            cur = conn.cursor()
            task = request.form.get("task")
            member_name = request.form.get("member_name")
            limit_date = request.form.get("limit_date")
            note = request.form.get("note")
            
            if limit_date == "":
                limit_date = None

            TABLE = settings.tbl_name
            sql = f"INSERT INTO {TABLE} (task, member_name, limit_date, note) VALUES (%s, %s, %s, %s)"

            # print(sql, (task, member_name, limit_date, note))
            cur.execute(sql, (task, member_name, limit_date, note))
            conn.commit()
            cur.close()
            conn.close()

        # 編集処理
        if "update_id" in request.form:
            update_id = request.form.get("update_id")
            update_task = request.form.get("update_task")
            update_member = request.form.get("update_member_name")
            update_date = request.form.get("update_limit_date")
            update_note = request.form.get("update_note")
            updates = []
            params = []

            if update_task is not None:
                updates.append("task = %s")
                params.append(update_task)
            if update_member is not None:
                updates.append("member_name = %s")
                params.append(update_member)
            if update_date is not None:
                updates.append("limit_date = %s")
                params.append(update_date)
            if update_note is not None:
                updates.append("note = %s")
                params.append(update_note)

            if updates:
                conn = get_conn()
                cur = conn.cursor()
                TABLE = settings.tbl_name  
                sql = f"UPDATE {TABLE} SET {', '.join(updates)} WHERE id = %s"
                params.append(update_id)
                # print(sql, tuple(params))
                cur.execute(sql, tuple(params))
                conn.commit()
                cur.close()
                conn.close()

            # 削除処理
        if "delete_id" in request.form:
            delete_id = request.form.get("delete_id")
            conn = get_conn()
            cur = conn.cursor()
            
            TABLE = settings.tbl_name
            sql = f"DELETE FROM {TABLE} WHERE id = %s"

            # print(sql, (delete_id,))
            cur.execute(sql, (delete_id,))
            conn.commit()
            cur.close()
            conn.close()

    conn = get_conn()
    cur = conn.cursor()
    TABLE = settings.tbl_name
    sql = f"SELECT * FROM {TABLE};"
    # print(sql)
    cur.execute(sql)
    todo_data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template(
        "index.html",
        todo_data=todo_data
    )

if __name__ == '__main__':
    app.run(port=5001)