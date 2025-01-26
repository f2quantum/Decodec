CRON_JOB := "0 2 \* \* \* python3 $(shell pwd)/main.py"

add-cron:
	@echo "$(CRON_JOB)" > new_cron.tmp
	@echo "Add Crontab Successful"

install-deps:
	python3 -m pip install --upgrade pip
	pip install requests
	if [ -f requirements.txt ]; then pip install -r requirements.txt; fi


# 定义服务名称
SERVICE_NAME = flask_app.service

# 定义 Flask 应用的启动命令
FLASK_COMMAND = python3 server.py

# 定义工作目录
WORKING_DIR = $(shell pwd)

# 生成 systemd 服务文件
generate-service:
	@echo "[Unit]" > $(SERVICE_NAME)
	@echo "Description=Flask Application Service" >> $(SERVICE_NAME)
	@echo "After=network.target" >> $(SERVICE_NAME)
	@echo "" >> $(SERVICE_NAME)
	@echo "[Service]" >> $(SERVICE_NAME)
	@echo "User=$(USER)" >> $(SERVICE_NAME)
	@echo "WorkingDirectory=$(WORKING_DIR)" >> $(SERVICE_NAME)
	@echo "ExecStart=$(FLASK_COMMAND)" >> $(SERVICE_NAME)
	@echo "Restart=always" >> $(SERVICE_NAME)
	@echo "" >> $(SERVICE_NAME)
	@echo "[Install]" >> $(SERVICE_NAME)
	@echo "WantedBy=multi-user.target" >> $(SERVICE_NAME)
	@echo "Systemd 服务文件 $(SERVICE_NAME) 已生成。"

# 复制服务文件到 systemd 目录
copy-service: generate-service
	sudo cp $(SERVICE_NAME) /etc/systemd/system/
	@echo "服务文件 $(SERVICE_NAME) 已复制到 /etc/systemd/system/。"

# 重新加载 systemd 管理器配置
reload-systemd: copy-service
	sudo systemctl daemon-reload
	@echo "Systemd 管理器配置已重新加载。"

# 启动服务并设置开机自启
enable-service: reload-systemd
	sudo systemctl start $(SERVICE_NAME)
	sudo systemctl enable $(SERVICE_NAME)
	@echo "服务 $(SERVICE_NAME) 已启动并设置为开机自启。"

# 清理生成的服务文件
clean:
	rm -f $(SERVICE_NAME)
	@echo "生成的服务文件 $(SERVICE_NAME) 已清理。"
