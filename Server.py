from flask import Flask, render_template, request, send_file
import pandas as pd
import os
import time

app = Flask(__name__)

# 初始读取 CSV 文件
csv_file_path = './data/Games_GetMoreFileList.csv'
df = pd.read_csv(csv_file_path)
# 记录文件的初始修改时间
last_modified_time = os.path.getmtime(csv_file_path)

def check_and_reload():
    global df, last_modified_time
    current_modified_time = os.path.getmtime(csv_file_path)
    if current_modified_time != last_modified_time:
        # 文件已更新，重新读取 CSV 文件
        df = pd.read_csv(csv_file_path)
        last_modified_time = current_modified_time

@app.route('/', methods=['GET', 'POST'])
def index():
    # 每次请求时检查文件是否更新
    check_and_reload()

    if request.method == 'POST':
        # 获取搜索关键字
        search_term = request.form.get('search_term')

        if search_term:
            # 对每一列进行前缀匹配筛选
            filtered_df = df[df.apply(lambda row: any(str(cell).startswith(search_term) for cell in row), axis=1)]
        else:
            filtered_df = df
    else:
        filtered_df = df

    # 获取 CSV 文件的表头
    headers = df.columns.tolist()
    # 获取筛选后的数据
    data = filtered_df.values.tolist()

    return render_template('index.html', headers=headers, data=data)

@app.route('/download_csv')
def download_csv():
    return send_file(csv_file_path, as_attachment=True)

@app.route('/download_excel')
def download_excel():
    excel_file_path = './data/Games_GetMoreFileList.xlsx'
    return send_file(excel_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
