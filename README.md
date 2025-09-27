# Meta-Marketing-Campaigns
1. Даємо доступ до entrypoint.sh
* `chmod +x entrypoint.sh`

2. Запускаємо і білдимо додаток
* `docker compose up --build`

3. Накатуємо міграції
* `make upgrade`

4. Запускаємо пайплайн вигрузки даних з CSV, їх загрузки у Meta і збереження в бд. 
Ця команда на початку видаляє всі дані з Meta та БД для легшого тестування.
* `make initial-upload`

5. Створені таблиці можна буде подивитись в adminer.
* `localhost:8080`

6. Щоб отримати airflow юзерів з паролями
* `make airflow-password`

7. В airflow вмикнути meta_pipeline_test DAG